# Wuzplay Firmware Safety Rules

These rules are mandatory for every custom Wuzplay firmware build in this project.

## Permanent emergency DFU escape

- Fifteen consecutive presses of the physical **Back** button must force the device into Nordic DFU mode.
- The counter must work from every responsive screen, not only the Home menu.
- Any different button resets the count.
- A pause longer than the configured multi-press window resets the count.
- The emergency check must run before desktop-only shortcut gating and before normal Back navigation.
- Other Back-button shortcuts must not erase the emergency counter. In particular, Back ×5 may prepare Govee, but continuing to Back ×15 must still enter DFU.
- The CI firmware build must fail when the 15-Back escape, its `enter_dfu()` call, or its global input routing is missing.

## Release packaging

Every release artifact must state:

> Press Back 15 times consecutively to enter Nordic DFU recovery mode.

Do not label a firmware build verified unless the source compiles, the Nordic DFU ZIP passes manifest/integrity checks, and the build-time safety assertions pass.
