#include "cyber_games.h"

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "../common/driver.h"

#define CG_W 128
#define CG_H 64

static uint8_t fb[CG_W * CG_H / 8];

static const uint8_t *cg_glyph(char c) {
    switch (c) {
    case ' ': { static const uint8_t g[5] = {0x0,0x0,0x0,0x0,0x0}; return g; }
    case '!': { static const uint8_t g[5] = {0x0,0x0,0x5f,0x0,0x0}; return g; }
    case '-': { static const uint8_t g[5] = {0x8,0x8,0x8,0x8,0x8}; return g; }
    case ':': { static const uint8_t g[5] = {0x0,0x36,0x36,0x0,0x0}; return g; }
    case '.': { static const uint8_t g[5] = {0x0,0x60,0x60,0x0,0x0}; return g; }
    case '/': { static const uint8_t g[5] = {0x20,0x10,0x8,0x4,0x2}; return g; }
    case '0': { static const uint8_t g[5] = {0x3e,0x51,0x49,0x45,0x3e}; return g; }
    case '1': { static const uint8_t g[5] = {0x0,0x42,0x7f,0x40,0x0}; return g; }
    case '2': { static const uint8_t g[5] = {0x42,0x61,0x51,0x49,0x46}; return g; }
    case '3': { static const uint8_t g[5] = {0x21,0x41,0x45,0x4b,0x31}; return g; }
    case '4': { static const uint8_t g[5] = {0x18,0x14,0x12,0x7f,0x10}; return g; }
    case '5': { static const uint8_t g[5] = {0x27,0x45,0x45,0x45,0x39}; return g; }
    case '6': { static const uint8_t g[5] = {0x3c,0x4a,0x49,0x49,0x30}; return g; }
    case '7': { static const uint8_t g[5] = {0x1,0x71,0x9,0x5,0x3}; return g; }
    case '8': { static const uint8_t g[5] = {0x36,0x49,0x49,0x49,0x36}; return g; }
    case '9': { static const uint8_t g[5] = {0x6,0x49,0x49,0x29,0x1e}; return g; }
    case 'A': { static const uint8_t g[5] = {0x7e,0x11,0x11,0x11,0x7e}; return g; }
    case 'B': { static const uint8_t g[5] = {0x7f,0x49,0x49,0x49,0x36}; return g; }
    case 'C': { static const uint8_t g[5] = {0x3e,0x41,0x41,0x41,0x22}; return g; }
    case 'D': { static const uint8_t g[5] = {0x7f,0x41,0x41,0x22,0x1c}; return g; }
    case 'E': { static const uint8_t g[5] = {0x7f,0x49,0x49,0x49,0x41}; return g; }
    case 'F': { static const uint8_t g[5] = {0x7f,0x9,0x9,0x9,0x1}; return g; }
    case 'G': { static const uint8_t g[5] = {0x3e,0x41,0x49,0x49,0x7a}; return g; }
    case 'H': { static const uint8_t g[5] = {0x7f,0x8,0x8,0x8,0x7f}; return g; }
    case 'I': { static const uint8_t g[5] = {0x0,0x41,0x7f,0x41,0x0}; return g; }
    case 'J': { static const uint8_t g[5] = {0x20,0x40,0x41,0x3f,0x1}; return g; }
    case 'K': { static const uint8_t g[5] = {0x7f,0x8,0x14,0x22,0x41}; return g; }
    case 'L': { static const uint8_t g[5] = {0x7f,0x40,0x40,0x40,0x40}; return g; }
    case 'M': { static const uint8_t g[5] = {0x7f,0x2,0xc,0x2,0x7f}; return g; }
    case 'N': { static const uint8_t g[5] = {0x7f,0x4,0x8,0x10,0x7f}; return g; }
    case 'O': { static const uint8_t g[5] = {0x3e,0x41,0x41,0x41,0x3e}; return g; }
    case 'P': { static const uint8_t g[5] = {0x7f,0x9,0x9,0x9,0x6}; return g; }
    case 'Q': { static const uint8_t g[5] = {0x3e,0x41,0x51,0x21,0x5e}; return g; }
    case 'R': { static const uint8_t g[5] = {0x7f,0x9,0x19,0x29,0x46}; return g; }
    case 'S': { static const uint8_t g[5] = {0x46,0x49,0x49,0x49,0x31}; return g; }
    case 'T': { static const uint8_t g[5] = {0x1,0x1,0x7f,0x1,0x1}; return g; }
    case 'U': { static const uint8_t g[5] = {0x3f,0x40,0x40,0x40,0x3f}; return g; }
    case 'V': { static const uint8_t g[5] = {0x1f,0x20,0x40,0x20,0x1f}; return g; }
    case 'W': { static const uint8_t g[5] = {0x3f,0x40,0x38,0x40,0x3f}; return g; }
    case 'X': { static const uint8_t g[5] = {0x63,0x14,0x8,0x14,0x63}; return g; }
    case 'Y': { static const uint8_t g[5] = {0x7,0x8,0x70,0x8,0x7}; return g; }
    case 'Z': { static const uint8_t g[5] = {0x61,0x51,0x49,0x45,0x43}; return g; }
    default: { static const uint8_t g[5] = {0,0,0,0,0}; return g; }
    }
}

static void cg_clear(void) { memset(fb, 0, sizeof(fb)); }

static void cg_pixel(int x, int y, bool on) {
    if (x < 0 || x >= CG_W || y < 0 || y >= CG_H) return;
    uint16_t i = (uint16_t)(y >> 3) * CG_W + (uint16_t)x;
    uint8_t bit = 1u << (y & 7);
    if (on) fb[i] |= bit;
    else fb[i] &= (uint8_t)~bit;
}

static void cg_box(int x, int y, int w, int h, bool fill) {
    for (int yy = 0; yy < h; yy++) {
        for (int xx = 0; xx < w; xx++) {
            if (fill || xx == 0 || yy == 0 || xx == w - 1 || yy == h - 1)
                cg_pixel(x + xx, y + yy, true);
        }
    }
}

static void cg_char(int x, int y, char c, int scale) {
    const uint8_t *g = cg_glyph(c);
    for (int col = 0; col < 5; col++) {
        for (int row = 0; row < 7; row++) {
            if (g[col] & (1u << row)) {
                for (int sx = 0; sx < scale; sx++)
                    for (int sy = 0; sy < scale; sy++)
                        cg_pixel(x + col * scale + sx, y + row * scale + sy, true);
            }
        }
    }
}

static void cg_text(int x, int y, const char *s, int scale) {
    while (*s) {
        cg_char(x, y, *s++, scale);
        x += 6 * scale;
    }
}

static void cg_text_center(int y, const char *s, int scale) {
    int w = (int)strlen(s) * 6 * scale;
    cg_text((CG_W - w) / 2, y, s, scale);
}

static void cg_present(void) {
    for (uint8_t page = 0; page < 8; page++) {
        JOY_OLED_data_start(page);
        for (uint8_t x = 0; x < CG_W; x++) {
            JOY_OLED_send(fb[(uint16_t)page * CG_W + x]);
        }
        JOY_OLED_end();
    }
}

static bool cg_exit(void) {
    return JOY_exit() || game_view_key_pressed(INPUT_KEY_BACK);
}

static void cg_wait_release(void) {
    while (JOY_act_pressed() && !cg_exit()) {
        JOY_idle();
        DLY_ms(10);
    }
}

static void cg_splash(const char *title, const char *line) {
    cg_clear();
    cg_box(1, 1, 126, 62, false);
    cg_text_center(12, title, 2);
    if (line) cg_text_center(43, line, 1);
    cg_present();
}

int cyber_snake_run(void) {
    int8_t sx[72], sy[72];
    uint8_t length = 5;
    int8_t dir = 0;
    int8_t food_x = 16, food_y = 5;
    uint16_t score = 0;
    bool prev_left = false, prev_right = false;

    cg_splash("SNAKE", "PRESS OK");
    while (!JOY_act_pressed()) {
        if (cg_exit()) return 0;
        JOY_idle();
    }
    cg_wait_release();

    for (uint8_t i = 0; i < length; i++) {
        sx[i] = 8 - i;
        sy[i] = 5;
    }

    while (!cg_exit()) {
        bool l = JOY_left_pressed();
        bool r = JOY_right_pressed();
        if (l && !prev_left) dir = (dir + 3) & 3;
        if (r && !prev_right) dir = (dir + 1) & 3;
        prev_left = l;
        prev_right = r;

        for (int i = length - 1; i > 0; i--) {
            sx[i] = sx[i - 1];
            sy[i] = sy[i - 1];
        }
        if (dir == 0) sx[0]++;
        if (dir == 1) sy[0]++;
        if (dir == 2) sx[0]--;
        if (dir == 3) sy[0]--;

        bool dead = sx[0] < 0 || sx[0] >= 24 || sy[0] < 0 || sy[0] >= 10;
        for (uint8_t i = 1; i < length; i++)
            if (sx[0] == sx[i] && sy[0] == sy[i]) dead = true;

        if (dead) {
            char score_text[20];
            snprintf(score_text, sizeof(score_text), "SCORE %u", score);
            cg_splash("GAME OVER", score_text);
            while (!JOY_act_pressed()) {
                if (cg_exit()) return 0;
                JOY_idle();
            }
            return 0;
        }

        if (sx[0] == food_x && sy[0] == food_y) {
            if (length < 71) length++;
            score++;
            food_x = JOY_random() % 24;
            food_y = JOY_random() % 10;
        }

        cg_clear();
        cg_box(2, 8, 122, 52, false);
        for (uint8_t i = 0; i < length; i++)
            cg_box(4 + sx[i] * 5, 10 + sy[i] * 5, 4, 4, true);
        cg_box(4 + food_x * 5, 10 + food_y * 5, 4, 4, false);
        cg_text(3, 0, "SNAKE", 1);
        cg_present();

        for (int t = 0; t < 12; t++) {
            if (cg_exit()) return 0;
            JOY_idle();
            DLY_ms(10);
        }
    }
    return 0;
}

int cyber_pong_run(void) {
    int py = 24, ay = 24;
    int bx = 64, by = 32, vx = -1, vy = 1;
    uint8_t player = 0, cpu = 0;

    cg_splash("PONG", "LEFT UP RIGHT DOWN");
    DLY_ms(700);

    while (!cg_exit()) {
        if (JOY_left_pressed() && py > 8) py -= 2;
        if (JOY_right_pressed() && py < 48) py += 2;

        if (ay + 6 < by && ay < 48) ay++;
        if (ay + 6 > by && ay > 8) ay--;

        bx += vx;
        by += vy;
        if (by <= 9 || by >= 61) vy = -vy;

        if (bx <= 7 && by >= py && by <= py + 14) {
            bx = 7; vx = 1;
            vy += (by - (py + 7)) / 4;
            if (vy > 2) vy = 2;
            if (vy < -2) vy = -2;
            if (vy == 0) vy = 1;
        }
        if (bx >= 120 && by >= ay && by <= ay + 14) {
            bx = 120; vx = -1;
        }

        if (bx < 0) { cpu++; bx = 64; by = 32; vx = 1; }
        if (bx > 127) { player++; bx = 64; by = 32; vx = -1; }

        cg_clear();
        cg_text(45, 0, "PONG", 1);
        for (int y = 9; y < 64; y += 5) cg_pixel(64, y, true);
        cg_box(3, py, 3, 15, true);
        cg_box(122, ay, 3, 15, true);
        cg_box(bx, by, 2, 2, true);
        char s[16];
        snprintf(s, sizeof(s), "%u-%u", player, cpu);
        cg_text(3, 0, s, 1);
        cg_present();

        for (int t = 0; t < 2; t++) {
            if (cg_exit()) return 0;
            JOY_idle();
            DLY_ms(10);
        }
    }
    return 0;
}

int cyber_dodge_run(void) {
    int lane = 1;
    int obs_lane[3] = {0, 2, 1};
    int obs_y[3] = {-10, -34, -58};
    uint16_t score = 0;
    bool prev_left = false, prev_right = false;
    const int lane_x[3] = {28, 62, 96};

    cg_splash("DODGE", "LEFT RIGHT");
    DLY_ms(700);

    while (!cg_exit()) {
        bool l = JOY_left_pressed();
        bool r = JOY_right_pressed();
        if (l && !prev_left && lane > 0) lane--;
        if (r && !prev_right && lane < 2) lane++;
        prev_left = l;
        prev_right = r;

        for (int i = 0; i < 3; i++) {
            obs_y[i] += 2;
            if (obs_y[i] > 64) {
                obs_y[i] = -18 - (JOY_random() % 30);
                obs_lane[i] = JOY_random() % 3;
                score++;
            }
            if (obs_lane[i] == lane && obs_y[i] + 8 >= 52 && obs_y[i] <= 61) {
                char s[20];
                snprintf(s, sizeof(s), "SCORE %u", score);
                cg_splash("CRASH", s);
                DLY_ms(1200);
                return 0;
            }
        }

        cg_clear();
        cg_text(3, 0, "DODGE", 1);
        cg_pixel(45, 8, true); cg_pixel(80, 8, true);
        for (int y = 8; y < 64; y += 4) {
            cg_pixel(45, y, true); cg_pixel(80, y, true);
        }
        cg_box(lane_x[lane], 52, 8, 9, true);
        for (int i = 0; i < 3; i++)
            cg_box(lane_x[obs_lane[i]], obs_y[i], 8, 8, false);
        cg_present();

        for (int t = 0; t < 5; t++) {
            if (cg_exit()) return 0;
            JOY_idle();
            DLY_ms(10);
        }
    }
    return 0;
}

int cyber_reaction_run(void) {
    uint16_t wait_steps = 30 + (JOY_random() % 50);
    cg_splash("REACTION", "WAIT");

    for (uint16_t i = 0; i < wait_steps; i++) {
        if (cg_exit()) return 0;
        if (JOY_act_pressed()) {
            cg_splash("TOO SOON", "TRY AGAIN");
            DLY_ms(1000);
            return 0;
        }
        JOY_idle();
        DLY_ms(50);
    }

    cg_splash("GO", "PRESS OK");
    uint16_t ticks = 0;
    while (!JOY_act_pressed()) {
        if (cg_exit()) return 0;
        JOY_idle();
        DLY_ms(10);
        ticks++;
    }

    char result[22];
    snprintf(result, sizeof(result), "%u MS", ticks * 10);
    cg_splash("REACTION", result);
    DLY_ms(1400);
    return 0;
}

int cyber_nba_soon_run(void) {
    int bx = 8, by = 22, vx = 2, vy = 1;
    for (uint16_t frame = 0; frame < 750; frame++) {
        if (cg_exit() || JOY_act_pressed()) return 0;
        bx += vx;
        by += vy;
        if (bx < 4 || bx > 118) vx = -vx;
        if (by < 18 || by > 55) vy = -vy;

        cg_clear();
        cg_text_center(1, "NBA 2K", 2);
        cg_text_center(31, "COMING SOON", 1);
        cg_text_center(43, "2 KB RAM", 1);
        cg_text_center(53, "NO MICROTX", 1);
        cg_box(bx, by, 6, 6, false);
        cg_pixel(bx + 1, by + 3, true);
        cg_pixel(bx + 4, by + 3, true);
        cg_present();

        JOY_idle();
        DLY_ms(20);
    }
    return 0;
}
