#ifndef CYBER_SHORTCUTS_H
#define CYBER_SHORTCUTS_H

#include <stdbool.h>
#include <stdint.h>

void cyber_shortcuts_init(void);
bool cyber_shortcuts_feed(uint8_t key);
void cyber_shortcuts_reset(void);

#endif
