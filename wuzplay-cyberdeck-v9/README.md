# Wuzplay Cyberdeck v9 build recipe

This folder builds a custom LCD DFU package from the Pixl.js source commit shown on the user's Wuzplay version screen (`5cc2b49`).

The workflow produces a verified Nordic DFU ZIP, application HEX, full factory HEX, and a verification report.

The multi-press actions prepare NFC URIs and show a `TAP PHONE` toast. They do not claim that the Wuzplay can remotely run an iPhone Shortcut without an NFC tap.
