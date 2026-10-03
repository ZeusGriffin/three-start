#include "cyber_games.h"

#include <stdbool.h>
#include <stdint.h>
#include <string.h>

#include "../common/driver.h"
#include "mui_core.h"
#include "u8g2.h"

#define CG_W 128
#define CG_H 64

extern const uint8_t u8g2_font_likeminecraft_te[];

static u8g2_t *cg_u8(void) { return &(mui()->u8g2); }

static void cg_clear(void) {
    u8g2_ClearBuffer(cg_u8());
    u8g2_SetDrawColor(cg_u8(), 1);
}

static void cg_pixel(int x, int y, bool on) {
    if (x < 0 || x >= CG_W || y < 0 || y >= CG_H) return;
    u8g2_SetDrawColor(cg_u8(), on ? 1 : 0);
    u8g2_DrawPixel(cg_u8(), x, y);
    u8g2_SetDrawColor(cg_u8(), 1);
}

static void cg_box(int x, int y, int w, int h, bool fill) {
    if (fill) u8g2_DrawBox(cg_u8(), x, y, w, h);
    else u8g2_DrawFrame(cg_u8(), x, y, w, h);
}

static void cg_text(int x, int y, const char *s, int scale) {
    (void)scale;
    u8g2_SetFont(cg_u8(), u8g2_font_likeminecraft_te);
    u8g2_DrawStr(cg_u8(), x, y + 8, s);
}

static void cg_text_center(int y, const char *s, int scale) {
    (void)scale;
    u8g2_SetFont(cg_u8(), u8g2_font_likeminecraft_te);
    int w = u8g2_GetStrWidth(cg_u8(), s);
    u8g2_DrawStr(cg_u8(), (CG_W - w) / 2, y + 8, s);
}

static void cg_present(void) { u8g2_SendBuffer(cg_u8()); }
static bool cg_exit(void) { return JOY_exit(); }

static void cg_wait_release(void) {
    while (JOY_act_pressed() && !cg_exit()) {
        JOY_idle();
        DLY_ms(10);
    }
}

static void cg_u16(char *out, uint16_t value) {
    char rev[6];
    uint8_t n = 0;
    do {
        rev[n++] = (char)('0' + value % 10);
        value /= 10;
    } while (value && n < sizeof(rev));
    for (uint8_t i = 0; i < n; i++) out[i] = rev[n - i - 1];
    out[n] = 0;
}

static void cg_label_value(char *out, const char *label, uint16_t value, const char *suffix) {
    uint8_t p = 0;
    while (*label && p < 20) out[p++] = *label++;
    cg_u16(out + p, value);
    p = (uint8_t)strlen(out);
    while (suffix && *suffix && p < 23) out[p++] = *suffix++;
    out[p] = 0;
}

static void cg_score_pair(char *out, uint16_t left, uint16_t right) {
    cg_u16(out, left);
    uint8_t p = (uint8_t)strlen(out);
    if (p < 22) out[p++] = ':';
    out[p] = 0;
    cg_u16(out + p, right);
}

static void cg_splash(const char *title, const char *line) {
    cg_clear();
    cg_box(1, 1, 126, 62, false);
    cg_text_center(13, title, 1);
    if (line) cg_text_center(42, line, 1);
    cg_present();
}

int cyber_snake_run(void) {
    int8_t sx[72], sy[72];
    uint8_t length = 5;
    int8_t dir = 0;
    int8_t food_x = 16, food_y = 5;
    uint16_t score = 0;
    bool prev_left = false, prev_right = false;

    cg_splash("SNAKE", "PRESS OK");
    while (!JOY_act_pressed()) {
        if (cg_exit()) return 0;
        JOY_idle();
    }
    cg_wait_release();

    for (uint8_t i = 0; i < length; i++) {
        sx[i] = 8 - i;
        sy[i] = 5;
    }

    while (!cg_exit()) {
        bool l = JOY_left_pressed();
        bool r = JOY_right_pressed();
        if (l && !prev_left) dir = (dir + 3) & 3;
        if (r && !prev_right) dir = (dir + 1) & 3;
        prev_left = l;
        prev_right = r;

        for (int i = length - 1; i > 0; i--) {
            sx[i] = sx[i - 1];
            sy[i] = sy[i - 1];
        }
        if (dir == 0) sx[0]++;
        if (dir == 1) sy[0]++;
        if (dir == 2) sx[0]--;
        if (dir == 3) sy[0]--;

        bool dead = sx[0] < 0 || sx[0] >= 24 || sy[0] < 0 || sy[0] >= 10;
        for (uint8_t i = 1; i < length; i++)
            if (sx[0] == sx[i] && sy[0] == sy[i]) dead = true;

        if (dead) {
            char score_text[24] = {0};
            cg_label_value(score_text, "SCORE ", score, NULL);
            cg_splash("GAME OVER", score_text);
            while (!JOY_act_pressed()) {
                if (cg_exit()) return 0;
                JOY_idle();
            }
            return 0;
        }

        if (sx[0] == food_x && sy[0] == food_y) {
            if (length < 71) length++;
            score++;
            food_x = JOY_random() % 24;
            food_y = JOY_random() % 10;
        }

        char score_text[24] = {0};
        cg_label_value(score_text, "S ", score, NULL);
        cg_clear();
        cg_box(2, 8, 122, 52, false);
        for (uint8_t i = 0; i < length; i++)
            cg_box(4 + sx[i] * 5, 10 + sy[i] * 5, 4, 4, true);
        cg_box(4 + food_x * 5, 10 + food_y * 5, 4, 4, false);
        cg_text(3, 0, "SNAKE", 1);
        cg_text(86, 0, score_text, 1);
        cg_present();

        for (int t = 0; t < 12; t++) {
            if (cg_exit()) return 0;
            JOY_idle();
            DLY_ms(10);
        }
    }
    return 0;
}

int cyber_pong_run(void) {
    int py = 24, ay = 24;
    int bx = 64, by = 32, vx = -1, vy = 1;
    uint16_t player_score = 0, cpu_score = 0;

    cg_splash("PONG", "LEFT UP RIGHT DOWN");
    DLY_ms(700);

    while (!cg_exit()) {
        if (JOY_left_pressed() && py > 8) py -= 2;
        if (JOY_right_pressed() && py < 48) py += 2;
        if (ay + 6 < by && ay < 48) ay++;
        if (ay + 6 > by && ay > 8) ay--;

        bx += vx;
        by += vy;
        if (by <= 9 || by >= 61) vy = -vy;

        if (bx <= 7 && by >= py && by <= py + 14) {
            bx = 7;
            vx = 1;
            vy += (by - (py + 7)) / 4;
            if (vy > 2) vy = 2;
            if (vy < -2) vy = -2;
            if (vy == 0) vy = 1;
        }
        if (bx >= 120 && by >= ay && by <= ay + 14) {
            bx = 120;
            vx = -1;
        }

        if (bx < 0) {
            cpu_score++;
            bx = 64;
            by = 32;
            vx = 1;
            vy = (JOY_random() & 1) ? 1 : -1;
        } else if (bx > 127) {
            player_score++;
            bx = 64;
            by = 32;
            vx = -1;
            vy = (JOY_random() & 1) ? 1 : -1;
        }

        char score_text[24] = {0};
        cg_score_pair(score_text, player_score, cpu_score);
        cg_clear();
        cg_text(3, 0, "PONG", 1);
        cg_text_center(0, score_text, 1);
        for (int y = 9; y < 64; y += 5) cg_pixel(64, y, true);
        cg_box(3, py, 3, 15, true);
        cg_box(122, ay, 3, 15, true);
        cg_box(bx, by, 2, 2, true);
        cg_present();

        for (int t = 0; t < 2; t++) {
            if (cg_exit()) return 0;
            JOY_idle();
            DLY_ms(10);
        }
    }
    return 0;
}

int cyber_dodge_run(void) {
    int lane = 1;
    int obs_lane[3] = {0, 2, 1};
    int obs_y[3] = {-10, -34, -58};
    uint16_t score = 0;
    bool prev_left = false, prev_right = false;
    const int lane_x[3] = {28, 62, 96};

    cg_splash("DODGE", "LEFT RIGHT");
    DLY_ms(700);

    while (!cg_exit()) {
        bool l = JOY_left_pressed();
        bool r = JOY_right_pressed();
        if (l && !prev_left && lane > 0) lane--;
        if (r && !prev_right && lane < 2) lane++;
        prev_left = l;
        prev_right = r;

        for (int i = 0; i < 3; i++) {
            obs_y[i] += 2;
            if (obs_y[i] > 64) {
                obs_y[i] = -18 - (JOY_random() % 30);
                obs_lane[i] = JOY_random() % 3;
                score++;
            }
            if (obs_lane[i] == lane && obs_y[i] + 8 >= 52 && obs_y[i] <= 61) {
                char result[24] = {0};
                cg_label_value(result, "SCORE ", score, NULL);
                cg_splash("CRASH", result);
                DLY_ms(1200);
                return 0;
            }
        }

        char score_text[24] = {0};
        cg_label_value(score_text, "S ", score, NULL);
        cg_clear();
        cg_text(3, 0, "DODGE", 1);
        cg_text(86, 0, score_text, 1);
        for (int y = 8; y < 64; y += 4) {
            cg_pixel(45, y, true);
            cg_pixel(80, y, true);
        }
        cg_box(lane_x[lane], 52, 8, 9, true);
        for (int i = 0; i < 3; i++) cg_box(lane_x[obs_lane[i]], obs_y[i], 8, 8, false);
        cg_present();

        for (int t = 0; t < 5; t++) {
            if (cg_exit()) return 0;
            JOY_idle();
            DLY_ms(10);
        }
    }
    return 0;
}

int cyber_reaction_run(void) {
    uint16_t wait_steps = 30 + (JOY_random() % 50);
    cg_splash("REACTION", "WAIT");

    for (uint16_t i = 0; i < wait_steps; i++) {
        if (cg_exit()) return 0;
        if (JOY_act_pressed()) {
            cg_splash("TOO SOON", "TRY AGAIN");
            DLY_ms(1000);
            return 0;
        }
        JOY_idle();
        DLY_ms(50);
    }

    cg_splash("GO", "PRESS OK");
    uint16_t ticks = 0;
    while (!JOY_act_pressed()) {
        if (cg_exit()) return 0;
        JOY_idle();
        DLY_ms(10);
        ticks++;
    }

    char result[24] = {0};
    cg_label_value(result, "", (uint16_t)(ticks * 10), " MS");
    cg_splash("REACTION", result);
    DLY_ms(1400);
    return 0;
}

int cyber_nba_soon_run(void) {
    int bx = 8, by = 22, vx = 2, vy = 1;
    for (uint16_t frame = 0; frame < 750; frame++) {
        if (cg_exit() || JOY_act_pressed()) return 0;
        bx += vx;
        by += vy;
        if (bx < 4 || bx > 118) vx = -vx;
        if (by < 18 || by > 55) vy = -vy;

        cg_clear();
        cg_text_center(1, "NBA 2K", 1);
        cg_text_center(28, "COMING SOON", 1);
        cg_text_center(40, "2 KB RAM", 1);
        cg_text_center(51, "NO MICROTX", 1);
        cg_box(bx, by, 6, 6, false);
        cg_pixel(bx + 1, by + 3, true);
        cg_pixel(bx + 4, by + 3, true);
        cg_present();

        JOY_idle();
        DLY_ms(20);
    }
    return 0;
}
