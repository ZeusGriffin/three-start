# Wuzplay Firmware Safety Rules

These rules are mandatory for every custom Wuzplay firmware build in this project.

## Permanent emergency DFU escape

- Twenty-five consecutive presses of the physical **Back** button must open a DFU confirmation prompt from any responsive screen.
- The prompt must say **ENTER DFU?** and require a deliberate second action.
- **Select = Yes** enters Nordic DFU mode.
- **Back = No** cancels and returns to normal use.
- Left or Right while the confirmation is open must not enter DFU.
- The 25-press counter must work from every responsive screen, not only the Home menu.
- Any different button before press 25 resets the count.
- A pause longer than the configured multi-press window before press 25 resets the count.
- The emergency check must run before desktop-only shortcut gating and before normal Back navigation.
- Other Back-button shortcuts must not erase the emergency counter. In particular, Back ×5 may prepare Govee, but continuing to Back ×25 must still reach the DFU confirmation prompt.
- The CI firmware build must fail when the 25-Back escape, confirmation state, Select-to-confirm `enter_dfu()` call, or global input routing is missing.

## Release packaging

Every release artifact must state:

> Press Back 25 times consecutively. When asked `ENTER DFU?`, press Select for Yes or Back for No.

Do not label a firmware build verified unless the source compiles, the Nordic DFU ZIP passes manifest/integrity checks, and the build-time safety assertions pass.
