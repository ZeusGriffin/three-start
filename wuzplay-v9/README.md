# Wuzplay Cyberdeck v9

Custom LCD firmware build based on `solosky/pixl.js` commit `5cc2b49`.

## Included in the custom build

- Four-button map: Left, Select, Right, Back
- Back button replayed as the firmware's existing long-center back action
- Gesture shortcuts:
  - Back x5, then pause: select Govee On NFC action
  - Back x6: select Flashlight NFC action
  - Back, Right, Back, Back: select Meditation Cyber NFC action
  - Left x5: select Find My Car NFC action
- Games: Snake, Pong, Breakout, Dodge, Reaction, NBA 2K Coming Soon, plus selected original tiny games
- Meditation Cyber portrait page

## Important hardware note

The public LCD board definition at commit `5cc2b49` exposes three buttons on GPIO 5, 6, and 7. This custom build assigns the fourth Back button to GPIO 8. The resulting OTA package can be structurally verified in CI, but the fourth-button pin must be confirmed on the physical Wuzplay before the build can be called hardware-verified.

## Phone actions

Button gestures select the matching NFC action on Wuzplay. Tap the Wuzplay to the top of the iPhone to run the selected URL or Apple Shortcut. iOS does not allow this firmware alone to silently launch arbitrary Shortcuts over Bluetooth in the background.
