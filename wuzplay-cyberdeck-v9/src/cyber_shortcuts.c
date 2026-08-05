#include "cyber_shortcuts.h"

#include <string.h>

#include "app_error.h"
#include "app_timer.h"
#include "mini_app_launcher.h"
#include "mini_app_registry.h"
#include "mui_include.h"
#include "mui_toast_view.h"
#include "ntag_emu.h"
#include "utils2.h"

#define SHORTCUT_WINDOW_MS 1200
#define SHORTCUT_BUFFER_SIZE 8
#define DFU_BACK_PRESS_COUNT 15
#define TOAST_VIEW_ID 0

static uint8_t m_keys[SHORTCUT_BUFFER_SIZE];
static uint8_t m_key_count = 0;
static uint8_t m_dfu_back_count = 0;
static bool m_initialized = false;
static mui_toast_view_t *m_toast = NULL;
static mui_view_dispatcher_t *m_toast_dispatcher = NULL;

APP_TIMER_DEF(m_shortcut_reset_timer);

static const uint8_t k_ntag_header[16] = {
    0x04, 0x5c, 0xb2, 0x62, 0xd2, 0xdb, 0x7b, 0xbe,
    0xcc, 0x48, 0x00, 0x00, 0xe1, 0x10, 0x3e, 0x00
};

static void reset_shortcut_pattern(void) {
    memset(m_keys, 0, sizeof(m_keys));
    m_key_count = 0;
}

static void shortcut_timer_handler(void *context) {
    (void)context;
    cyber_shortcuts_reset();
}

void cyber_shortcuts_reset(void) {
    reset_shortcut_pattern();
    m_dfu_back_count = 0;
}

static bool suffix_matches(const uint8_t *pattern, uint8_t pattern_len) {
    if (m_key_count < pattern_len) return false;
    uint8_t start = m_key_count - pattern_len;
    for (uint8_t i = 0; i < pattern_len; i++) {
        if (m_keys[start + i] != pattern[i]) return false;
    }
    return true;
}

static void set_uri_tag(const char *label, const char *url) {
    size_t url_len = strlen(url);
    if (url_len > 240) url_len = 240;

    /* Reuse the emulator's existing tag buffer instead of allocating another
       2 KB NTAG structure in RAM. */
    ntag_t *tag = ntag_emu_get_current_tag();
    if (!tag) return;

    memset(tag->data, 0, NTAG_DATA_SIZE);
    memset(tag->notes, 0, sizeof(tag->notes));
    memcpy(tag->data, k_ntag_header, sizeof(k_ntag_header));

    /* NFC Forum Type 2 TLV containing one URI NDEF record. */
    size_t p = 16;
    tag->data[p++] = 0x03;
    tag->data[p++] = (uint8_t)(url_len + 5);
    tag->data[p++] = 0xd1;
    tag->data[p++] = 0x01;
    tag->data[p++] = (uint8_t)(url_len + 1);
    tag->data[p++] = 0x55;
    tag->data[p++] = 0x00;
    memcpy(&tag->data[p], url, url_len);
    p += url_len;
    tag->data[p] = 0xfe;

    strncpy((char *)tag->notes, label, sizeof(tag->notes) - 1);
    tag->read_only = false;
    tag->type = NTAG_215;
    ntag_emu_set_tag(tag);

    if (m_toast) mui_toast_view_show(m_toast, label);
}

static bool current_app_is_desktop(void) {
    mini_app_launcher_t *launcher = mini_app_launcher();
    if (!launcher || !launcher->p_main_app_inst || !launcher->p_main_app_inst->p_app) return false;
    return launcher->p_main_app_inst->p_app->id == MINI_APP_ID_DESKTOP;
}

void cyber_shortcuts_init(void) {
    if (m_initialized) return;

    ret_code_t err = app_timer_create(
        &m_shortcut_reset_timer,
        APP_TIMER_MODE_SINGLE_SHOT,
        shortcut_timer_handler
    );
    APP_ERROR_CHECK(err);

    m_toast_dispatcher = mui_view_dispatcher_create();
    m_toast = mui_toast_view_create();
    mui_view_dispatcher_add_view(
        m_toast_dispatcher,
        TOAST_VIEW_ID,
        mui_toast_view_get_view(m_toast)
    );
    mui_view_dispatcher_attach(m_toast_dispatcher, MUI_LAYER_TOAST);
    mui_view_dispatcher_switch_to_view(m_toast_dispatcher, TOAST_VIEW_ID);

    m_initialized = true;
}

bool cyber_shortcuts_feed(uint8_t key) {
    if (!m_initialized) cyber_shortcuts_init();

    /* Permanent recovery escape: fifteen consecutive Back presses are counted
       globally, even while an app or game is open. Any different key or a pause
       longer than the shortcut window resets the count. */
    if (key == INPUT_KEY_BACK) {
        if (m_dfu_back_count < DFU_BACK_PRESS_COUNT) m_dfu_back_count++;
    } else {
        m_dfu_back_count = 0;
    }

    app_timer_stop(m_shortcut_reset_timer);
    ret_code_t err = app_timer_start(
        m_shortcut_reset_timer,
        APP_TIMER_TICKS(SHORTCUT_WINDOW_MS),
        NULL
    );
    APP_ERROR_CHECK(err);

    if (m_dfu_back_count >= DFU_BACK_PRESS_COUNT) {
        /* enter_dfu writes the Nordic bootloader flag and resets immediately. */
        enter_dfu();
        return true;
    }

    /* Phone-action patterns only run from Home so normal app controls remain safe. */
    if (!current_app_is_desktop()) {
        reset_shortcut_pattern();
        return false;
    }

    if (m_key_count >= SHORTCUT_BUFFER_SIZE) {
        memmove(m_keys, m_keys + 1, SHORTCUT_BUFFER_SIZE - 1);
        m_key_count = SHORTCUT_BUFFER_SIZE - 1;
    }
    m_keys[m_key_count++] = key;

    static const uint8_t meditation[] = {
        INPUT_KEY_BACK, INPUT_KEY_RIGHT, INPUT_KEY_BACK, INPUT_KEY_BACK
    };
    static const uint8_t govee[] = {
        INPUT_KEY_BACK, INPUT_KEY_BACK, INPUT_KEY_BACK, INPUT_KEY_BACK, INPUT_KEY_BACK
    };
    static const uint8_t find_car[] = {
        INPUT_KEY_LEFT, INPUT_KEY_LEFT, INPUT_KEY_LEFT, INPUT_KEY_LEFT, INPUT_KEY_LEFT
    };
    static const uint8_t flashlight[] = {
        INPUT_KEY_RIGHT, INPUT_KEY_RIGHT, INPUT_KEY_RIGHT,
        INPUT_KEY_RIGHT, INPUT_KEY_RIGHT, INPUT_KEY_RIGHT
    };

    if (suffix_matches(meditation, sizeof(meditation))) {
        set_uri_tag(
            "MEDITATION READY\nTAP PHONE",
            "scriptable:///run/Meditation%20Cyber"
        );
        reset_shortcut_pattern();
        return true;
    }

    if (suffix_matches(govee, sizeof(govee))) {
        set_uri_tag(
            "GOVEE READY\nTAP PHONE",
            "shortcuts://run-shortcut?name=Govee%20On"
        );
        /* Preserve the emergency Back count so continuing to 15 still enters DFU. */
        reset_shortcut_pattern();
        return true;
    }

    if (suffix_matches(find_car, sizeof(find_car))) {
        set_uri_tag(
            "FIND CAR READY\nTAP PHONE",
            "shortcuts://run-shortcut?name=Find%20My%20Car"
        );
        reset_shortcut_pattern();
        return true;
    }

    if (suffix_matches(flashlight, sizeof(flashlight))) {
        set_uri_tag(
            "FLASHLIGHT READY\nTAP PHONE",
            "shortcuts://run-shortcut?name=Flashlight"
        );
        reset_shortcut_pattern();
        return true;
    }

    return false;
}
