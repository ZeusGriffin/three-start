#include "cyber_breakout.h"

#include <stdbool.h>
#include <stdint.h>
#include <string.h>

#include "driver.h"

#define W 128
#define H 64
#define PADDLE_Y 58
#define PADDLE_W 24
#define BRICK_COLS 8
#define BRICK_ROWS 3

/* Breakout writes pages directly instead of using u8g2, so rotate its logical
   pixels here to match the main firmware's corrected 180-degree LCD layout. */
static void page_pixel(uint8_t *line, uint8_t page, int x, int y) {
    if (x < 0 || x >= W || y < 0 || y >= H) return;
    x = (W - 1) - x;
    y = (H - 1) - y;
    if ((y >> 3) != page) return;
    line[x] |= (uint8_t)(1u << (y & 7));
}

static void page_box(uint8_t *line, uint8_t page, int x, int y, int w, int h, bool fill) {
    for (int yy = 0; yy < h; yy++) {
        for (int xx = 0; xx < w; xx++) {
            if (fill || xx == 0 || yy == 0 || xx == w - 1 || yy == h - 1)
                page_pixel(line, page, x + xx, y + yy);
        }
    }
}

static const uint8_t digit_rows[10][5] = {
    {7,5,5,5,7}, {2,6,2,2,7}, {7,1,7,4,7}, {7,1,7,1,7}, {5,5,7,1,1},
    {7,4,7,1,7}, {7,4,7,5,7}, {7,1,1,1,1}, {7,5,7,5,7}, {7,5,7,1,7}
};

static void page_digit(uint8_t *line, uint8_t page, int x, int y, uint8_t digit) {
    if (digit > 9) digit = 0;
    for (uint8_t row = 0; row < 5; row++) {
        for (uint8_t col = 0; col < 3; col++) {
            if (digit_rows[digit][row] & (1u << (2 - col)))
                page_pixel(line, page, x + col, y + row);
        }
    }
}

static void page_score(uint8_t *line, uint8_t page, uint16_t score) {
    uint8_t digits[5];
    uint8_t count = 0;
    do {
        digits[count++] = (uint8_t)(score % 10);
        score /= 10;
    } while (score && count < 5);

    int x = 123 - (int)(count * 4);
    for (int i = count - 1; i >= 0; i--) {
        page_digit(line, page, x, 1, digits[i]);
        x += 4;
    }
}

static void render(int paddle_x, int ball_x, int ball_y, const uint8_t bricks[BRICK_ROWS], uint16_t score) {
    uint8_t line[W];
    for (uint8_t page = 0; page < 8; page++) {
        memset(line, 0, sizeof(line));

        for (int x = 0; x < W; x++) {
            page_pixel(line, page, x, 7);
            page_pixel(line, page, x, H - 1);
        }
        for (int y = 7; y < H; y++) {
            page_pixel(line, page, 0, y);
            page_pixel(line, page, W - 1, y);
        }

        page_score(line, page, score);

        for (uint8_t row = 0; row < BRICK_ROWS; row++) {
            for (uint8_t col = 0; col < BRICK_COLS; col++) {
                if (bricks[row] & (1u << col)) {
                    page_box(line, page, 4 + col * 15, 11 + row * 8, 13, 5, false);
                }
            }
        }

        page_box(line, page, paddle_x, PADDLE_Y, PADDLE_W, 3, true);
        page_box(line, page, ball_x, ball_y, 3, 3, true);

        JOY_OLED_data_start(page);
        for (uint8_t x = 0; x < W; x++) JOY_OLED_send(line[x]);
        JOY_OLED_end();
    }
}

static void reset_bricks(uint8_t bricks[BRICK_ROWS]) {
    for (uint8_t i = 0; i < BRICK_ROWS; i++) bricks[i] = 0xff;
}

int cyber_breakout_run(void) {
    int paddle_x = (W - PADDLE_W) / 2;
    int ball_x = 63;
    int ball_y = 46;
    int vx = 1;
    int vy = -1;
    uint16_t score = 0;
    uint8_t bricks[BRICK_ROWS];
    reset_bricks(bricks);

    while (!JOY_exit()) {
        if (JOY_left_pressed() && paddle_x > 2) paddle_x -= 2;
        if (JOY_right_pressed() && paddle_x < W - PADDLE_W - 2) paddle_x += 2;

        ball_x += vx;
        ball_y += vy;

        if (ball_x <= 2) { ball_x = 2; vx = 1; }
        if (ball_x >= W - 5) { ball_x = W - 5; vx = -1; }
        if (ball_y <= 9) { ball_y = 9; vy = 1; }

        if (vy > 0 && ball_y + 3 >= PADDLE_Y &&
            ball_x + 2 >= paddle_x && ball_x <= paddle_x + PADDLE_W) {
            ball_y = PADDLE_Y - 3;
            vy = -1;
            int hit = ball_x - paddle_x;
            if (hit < PADDLE_W / 3) vx = -1;
            else if (hit > (PADDLE_W * 2) / 3) vx = 1;
        }

        if (ball_y >= H - 4) {
            ball_x = 63;
            ball_y = 46;
            vx = (JOY_random() & 1) ? 1 : -1;
            vy = -1;
        }

        if (ball_y >= 10 && ball_y < 10 + BRICK_ROWS * 8) {
            int row = (ball_y - 10) / 8;
            int col = (ball_x - 3) / 15;
            if (row >= 0 && row < BRICK_ROWS && col >= 0 && col < BRICK_COLS) {
                uint8_t mask = (uint8_t)(1u << col);
                if (bricks[row] & mask) {
                    bricks[row] &= (uint8_t)~mask;
                    score++;
                    vy = -vy;
                }
            }
        }

        if ((bricks[0] | bricks[1] | bricks[2]) == 0) reset_bricks(bricks);

        render(paddle_x, ball_x, ball_y, bricks, score);
        for (uint8_t i = 0; i < 3; i++) {
            if (JOY_exit()) return 0;
            JOY_idle();
            DLY_ms(10);
        }
    }
    return 0;
}
