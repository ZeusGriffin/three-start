#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
ASSETS = Path(__file__).resolve().parent / "src"

def read(rel):
    return (ROOT / rel).read_text()

def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)

def replace_once(rel, old, new):
    text = read(rel)
    if old not in text:
        raise RuntimeError(f"Expected text not found in {rel}: {old[:100]!r}")
    text = text.replace(old, new, 1)
    write(rel, text)

for name in ["cyber_shortcuts.c", "cyber_shortcuts.h"]:
    shutil.copy2(ASSETS / name, ROOT / "fw/application/src/mod" / name)
for name in ["cyber_games.c", "cyber_games.h"]:
    shutil.copy2(ASSETS / name, ROOT / "fw/application/src/app/game/port/common" / name)

board = "fw/application/src/boards/board_lcd.h"
replace_once(board, "#define BUTTONS_NUMBER 3", "#define BUTTONS_NUMBER 4")
replace_once(board, "#define BUTTON_3       7\n#define BUTTON_STOP    7",
             "#define BUTTON_3       7\n#define BUTTON_4       8\n#define BUTTON_STOP    8")
replace_once(board, "#define BUTTONS_LIST { BUTTON_1, BUTTON_2, BUTTON_3}",
             "#define BUTTONS_LIST { BUTTON_1, BUTTON_2, BUTTON_3, BUTTON_4}")
replace_once(board, "#define BSP_BUTTON_2   BUTTON_3",
             "#define BSP_BUTTON_2   BUTTON_3\n#define BSP_BUTTON_3   BUTTON_4")
replace_once(board, "// #define APP_GAME_ENABLE", "#define APP_GAME_ENABLE")

bsp = "fw/application/src/mod/bsp_btn.c"
replace_once(
    bsp,
    "    {BSP_BUTTON_2, false, BUTTON_PULL, bsp_button_event_handler},\n};",
    "    {BSP_BUTTON_2, false, BUTTON_PULL, bsp_button_event_handler},\n"
    "    {BSP_BUTTON_3, false, BUTTON_PULL, bsp_button_event_handler},\n};"
)

mui_h = "fw/application/src/mui/mui_input.h"
replace_once(
    mui_h,
    "    INPUT_KEY_RIGHT\n} input_key_t;",
    "    INPUT_KEY_RIGHT,\n    INPUT_KEY_BACK\n} input_key_t;"
)

mui_c = "fw/application/src/mui/mui_input.c"
replace_once(
    mui_c,
    '#include "cache.h"\n',
    '#include "cache.h"\n'
    '#include "cyber_shortcuts.h"\n'
    '#include "mini_app_launcher.h"\n'
    '#include "mini_app_registry.h"\n'
    '#include "game_view.h"\n'
)
replace_once(
    mui_c,
    '    case BSP_BTN_EVENT_SHORT: {\n'
    '        NRF_LOG_DEBUG("Key %d short push", btn);\n'
    '        mui_input_event_t input_event = {.key = btn,\n'
    '                                         .type = INPUT_TYPE_SHORT};\n'
    '        mui_input_post_event(&input_event);\n'
    '        break;\n'
    '    }',
    '    case BSP_BTN_EVENT_SHORT: {\n'
    '        NRF_LOG_DEBUG("Key %d short push", btn);\n'
    '\n'
    '        mini_app_launcher_t *launcher = mini_app_launcher();\n'
    '        uint32_t current_id = launcher->p_main_app_inst && launcher->p_main_app_inst->p_app\n'
    '                                  ? launcher->p_main_app_inst->p_app->id\n'
    '                                  : MINI_APP_ID_DESKTOP;\n'
    '\n'
    '        if (btn == INPUT_KEY_BACK) {\n'
    '            if (current_id == MINI_APP_ID_DESKTOP) {\n'
    '                cyber_shortcuts_feed(btn);\n'
    '            } else if (current_id == MINI_APP_ID_GAME && game_view_is_running()) {\n'
    '                game_view_request_exit();\n'
    '            } else {\n'
    '                cyber_shortcuts_reset();\n'
    '                mini_app_launcher_exit(launcher);\n'
    '            }\n'
    '            break;\n'
    '        }\n'
    '\n'
    '        if (cyber_shortcuts_feed(btn)) break;\n'
    '\n'
    '        mui_input_event_t input_event = {.key = btn,\n'
    '                                         .type = INPUT_TYPE_SHORT};\n'
    '        mui_input_post_event(&input_event);\n'
    '        break;\n'
    '    }'
)
replace_once(
    mui_c,
    "void mui_input_init() {\n    bsp_btn_init(mui_input_on_bsp_btn_event);",
    "void mui_input_init() {\n    cyber_shortcuts_init();\n    bsp_btn_init(mui_input_on_bsp_btn_event);"
)

game_view_h = "fw/application/src/app/game/view/game_view.h"
replace_once(
    game_view_h,
    "uint8_t game_view_center_key_repeat_cnt();",
    "uint8_t game_view_center_key_repeat_cnt();\n"
    "uint8_t game_view_is_running(void);\n"
    "void game_view_request_exit(void);\n"
    "uint8_t game_view_exit_requested(void);"
)
game_view_c = "fw/application/src/app/game/view/game_view.c"
replace_once(game_view_c, "uint8_t key_state[3] = {0};",
             "uint8_t key_state[4] = {0};\n"
             "static uint8_t g_game_running = 0;\n"
             "static uint8_t g_game_exit_requested = 0;")
replace_once(
    game_view_c,
    "uint8_t game_view_center_key_repeat_cnt(){\n    return key_repeat_cnt;\n}\n",
    "uint8_t game_view_center_key_repeat_cnt(){\n"
    "    return key_repeat_cnt;\n"
    "}\n"
    "\n"
    "uint8_t game_view_is_running(void) { return g_game_running; }\n"
    "void game_view_request_exit(void) { g_game_exit_requested = 1; }\n"
    "uint8_t game_view_exit_requested(void) { return g_game_exit_requested; }\n"
)
replace_once(
    game_view_c,
    "        p_game_view->running = 1;\n        mui_set_auto_update(mui(), 0);",
    "        p_game_view->running = 1;\n"
    "        g_game_running = 1;\n"
    "        g_game_exit_requested = 0;\n"
    "        mui_set_auto_update(mui(), 0);"
)
replace_once(
    game_view_c,
    "        p_game_view->running = 0;\n        key_repeat_cnt = 0;",
    "        p_game_view->running = 0;\n"
    "        g_game_running = 0;\n"
    "        g_game_exit_requested = 0;\n"
    "        key_repeat_cnt = 0;"
)

driver_c = "fw/application/src/app/game/port/common/driver.c"
replace_once(
    driver_c,
    "uint8_t JOY_exit() {\n    return game_view_center_key_repeat_cnt() > 10; // about 3 sec\n}",
    "uint8_t JOY_exit() {\n"
    "    return game_view_exit_requested() || game_view_center_key_repeat_cnt() > 10;\n"
    "}"
)

game_list = "fw/application/src/app/game/scene/game_scene_game_list.c"
replace_once(
    game_list,
    '#include "tiny_tris.h"\n',
    '#include "tiny_tris.h"\n#include "cyber_games.h"\n'
)
old_list = (
    "    mui_list_view_add_item(app->p_list_view, ICON_HOME, _T(MAIN_MENU), (void *)-1);\n"
    "    mui_list_view_add_item(app->p_list_view, ICON_FILE, _T(APP_GAME_TINY_LANDER), tiny_lander_run);\n"
    "    mui_list_view_add_item(app->p_list_view, ICON_FILE, _T(APP_GAME_TINY_INVADERS) , tiny_invaders_run);\n"
    "    mui_list_view_add_item(app->p_list_view, ICON_FILE, _T(APP_GAME_TINY_ARKANOID), tiny_arkanoid_run);\n"
    "    mui_list_view_add_item(app->p_list_view, ICON_FILE, _T(APP_GAME_TINY_TRIS), tiny_tris_run);\n"
)
new_list = (
    "    mui_list_view_add_item(app->p_list_view, ICON_HOME, _T(MAIN_MENU), (void *)-1);\n"
    "    mui_list_view_add_item(app->p_list_view, ICON_FILE, \"SNAKE\", cyber_snake_run);\n"
    "    mui_list_view_add_item(app->p_list_view, ICON_FILE, \"PONG\", cyber_pong_run);\n"
    "    mui_list_view_add_item(app->p_list_view, ICON_FILE, \"BREAKOUT\", tiny_arkanoid_run);\n"
    "    mui_list_view_add_item(app->p_list_view, ICON_FILE, \"DODGE\", cyber_dodge_run);\n"
    "    mui_list_view_add_item(app->p_list_view, ICON_FILE, \"REACTION\", cyber_reaction_run);\n"
    "    mui_list_view_add_item(app->p_list_view, ICON_FILE, \"SPACE RAID\", tiny_invaders_run);\n"
    "    mui_list_view_add_item(app->p_list_view, ICON_FILE, \"LANDER\", tiny_lander_run);\n"
    "    mui_list_view_add_item(app->p_list_view, ICON_FILE, \"BLOCKS\", tiny_tris_run);\n"
    "    mui_list_view_add_item(app->p_list_view, ICON_FILE, \"NBA 2K - SOON\", cyber_nba_soon_run);\n"
)
replace_once(game_list, old_list, new_list)

makefile = "fw/application/Makefile"
replace_once(
    makefile,
    "  $(PROJ_DIR)/mod/bsp_btn.c \\\n",
    "  $(PROJ_DIR)/mod/bsp_btn.c \\\n"
    "  $(PROJ_DIR)/mod/cyber_shortcuts.c \\\n"
)
replace_once(
    makefile,
    "  $(PROJ_DIR)/app/game/port/common/driver.c \\\n",
    "  $(PROJ_DIR)/app/game/port/common/driver.c \\\n"
    "  $(PROJ_DIR)/app/game/port/common/cyber_games.c \\\n"
)

print("Wuzplay Cyberdeck v9 patch applied.")
