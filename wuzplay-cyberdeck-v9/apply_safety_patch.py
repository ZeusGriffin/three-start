#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
path = root / "fw/application/src/mui/mui_input.c"
text = path.read_text()

old = '''        if (btn == INPUT_KEY_BACK) {
            if (current_id == MINI_APP_ID_DESKTOP) {
                cyber_shortcuts_feed(btn);
            } else if (current_id == MINI_APP_ID_GAME && game_view_is_running()) {
                game_view_request_exit();
            } else {
                cyber_shortcuts_reset();
                mini_app_launcher_exit(launcher);
            }
            break;
        }

        if (cyber_shortcuts_feed(btn)) break;
'''

new = '''        if (btn == INPUT_KEY_BACK) {
            /* Feed Back globally before navigation. This keeps the permanent
               25-press recovery sequence available from every screen. After
               press 25, cyber_shortcuts waits for Select=Yes or Back=No. */
            if (cyber_shortcuts_feed(btn)) break;

            if (current_id == MINI_APP_ID_DESKTOP) {
                /* Home consumes Back for shortcut and recovery sequences. */
            } else if (current_id == MINI_APP_ID_GAME && game_view_is_running()) {
                game_view_request_exit();
            } else {
                mini_app_launcher_exit(launcher);
            }
            break;
        }

        if (cyber_shortcuts_feed(btn)) break;
'''

if old not in text:
    raise SystemExit("Expected Back-button routing block was not found")

path.write_text(text.replace(old, new, 1))
print("Permanent 25-Back DFU safety routing with confirmation applied.")
