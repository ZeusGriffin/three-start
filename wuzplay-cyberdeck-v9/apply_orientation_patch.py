#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
path = root / "fw/application/src/mui/mui_u8g2.c"
text = path.read_text()

old = "u8g2_Setup_st7567_enh_dg128064_f(p_u8g2, U8G2_R0, u8x8_HW_com_spi_nrf52832, u8g2_nrf_gpio_and_delay_spi_cb);"
new = "u8g2_Setup_st7567_enh_dg128064_f(p_u8g2, U8G2_R2, u8x8_HW_com_spi_nrf52832, u8g2_nrf_gpio_and_delay_spi_cb);"

if old not in text:
    raise SystemExit("Expected LCD U8G2_R0 setup was not found")

path.write_text(text.replace(old, new, 1))
print("PASS: LCD framebuffer rotation changed from U8G2_R0 to U8G2_R2 (180 degrees).")
