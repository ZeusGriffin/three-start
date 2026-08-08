WUZPLAY CYBERDECK v9.1 — CUSTOM FIRMWARE BUILD

Target:
- LCD Wuzplay/Pixl.js hardware
- Source base: solosky/pixl.js commit 5cc2b49
- Version value: 901

Included firmware changes:
- LCD rotated 180 degrees to match the physical Wuzplay case orientation
- Four-button map: Left, Select, Right, Back
- Back input on GPIO 8 for the Wuzplay four-button shell
- Animated game menu enabled
- Snake with visible live score and final score
- Pong with player : CPU scoring for the full session
- Breakout with visible score that increases for every brick
- Dodge with visible live score and crash score
- Reaction with reaction time used as the score
- NBA 2K — Coming Soon joke screen
- Home-screen shortcut sequences:
  Back x5 = prepare Govee On NFC action
  Back, Right, Back, Back = prepare Meditation Cyber NFC action
  Right x6 = prepare Flashlight NFC action
  Left x5 = prepare Find My Car NFC action

PERMANENT SAFETY ESCAPE:
- Press the physical Back button 25 times consecutively.
- The Wuzplay does NOT enter DFU immediately.
- It asks: ENTER DFU?
- Press Select for YES.
- Press Back for NO / cancel.
- Left or Right cannot confirm DFU.
- This is designed to work from every responsive screen, not only Home.
- Keep tapping after Back x5 prepares Govee; the emergency count continues to 25.
- A different button or a pause longer than about 1.2 seconds before press 25 resets the count.

IMPORTANT:
The phone-action button sequences prepare the matching NFC action. When the screen says
TAP PHONE, touch the Wuzplay to the top of the iPhone. The Wuzplay cannot remotely open
an iPhone app without the final NFC tap.

Install:
Keep 01_INSTALL_WUZPLAY_CYBERDECK_V9_1_ROT180_SCORE_DFU_KEEP_ZIPPED.zip zipped and select it in
Wuzplay Firmware Upgrade.

Recovery:
If normal Firmware Upgrade cannot be reached, press Back 25 times consecutively. When
ENTER DFU? appears, press Select to confirm. Wait for the device named pixl dfu to appear,
then select it in the DFU app and upload the zipped installer. Press Back at the prompt to cancel.
