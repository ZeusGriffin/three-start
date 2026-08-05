WUZPLAY CYBERDECK v9 — CUSTOM FIRMWARE BUILD

Target:
- LCD Wuzplay/Pixl.js hardware
- Source base: solosky/pixl.js commit 5cc2b49
- Version value: 900

Included firmware changes:
- Four-button map: Left, Select, Right, Back
- Back input on GPIO 8 for the Wuzplay four-button shell
- Animated game menu enabled
- Snake
- Pong
- Breakout
- Dodge
- Reaction
- NBA 2K — Coming Soon joke screen
- Home-screen shortcut sequences:
  Back x5 = prepare Govee On NFC action
  Back, Right, Back, Back = prepare Meditation Cyber NFC action
  Right x6 = prepare Flashlight NFC action
  Left x5 = prepare Find My Car NFC action

PERMANENT SAFETY ESCAPE:
- Press the physical Back button 15 times consecutively.
- The Wuzplay immediately restarts in Nordic DFU mode.
- This is designed to work from every responsive screen, not only Home.
- Keep tapping after Back x5 prepares Govee; the emergency count continues to 15.
- A different button or a pause longer than about 1.2 seconds resets the count.

IMPORTANT:
The phone-action button sequences prepare the matching NFC action. When the screen says
TAP PHONE, touch the Wuzplay to the top of the iPhone. The Wuzplay cannot remotely open
an iPhone app without the final NFC tap.

Install:
Keep 01_INSTALL_WUZPLAY_CYBERDECK_V9_DFU_KEEP_ZIPPED.zip zipped and select it in
Wuzplay Firmware Upgrade.

Recovery:
If normal Firmware Upgrade cannot be reached, press Back 15 times consecutively, wait
for the device named pixl dfu to appear, then select it in the DFU app and upload the
zipped installer.
