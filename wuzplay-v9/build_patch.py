#!/usr/bin/env python3
from pathlib import Path
import argparse, textwrap

ROOT = Path(__file__).resolve().parent

EMBEDDED_CARDS_B64 = {'meditation_data': 'BE0XTk9QUYgASAAA4RA+AANl0QFhVQBodHRwczovL3Jhdy5naXRoYWNrLmNvbS9aZXVzR3JpZmZpbi90aHJlZS1zdGFydC93dXpwbGF5LWN5YmVyZGVjay12OS9tZWRpdGF0aW9uLWN5YmVyL2luZGV4Lmh0bWz+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'govee_data': 'BFyyYtLbe77MSAAA4RA+AAMt0QEpVQBzaG9ydGN1dHM6Ly9ydW4tc2hvcnRjdXQ/bmFtZT1Hb3ZlZSUyME9u/gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL0EAAD/AAUAAAAAAAAAAAAA', 'flashlight_data': 'BMv4v7uM2bxSSAAA4RA+AAMt0QEpVQBzaG9ydGN1dHM6Ly9ydW4tc2hvcnRjdXQ/bmFtZT1GbGFzaGxpZ2h0/gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL0EAAD/AAUAAAAAAAAAAAAA', 'find_car_data': 'BKJlSwG+XJ98SAAA4RA+AAMy0QEuVQBzaG9ydGN1dHM6Ly9ydW4tc2hvcnRjdXQ/bmFtZT1GaW5kJTIwTXklMjBDYXL+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL0EAAD/AAUAAAAAAAAAAAAA'}

CYBER_GAMES_C = '#include "cyber_games.h"\n#include "../common/driver.h"\n#include <stdint.h>\n#include <stdbool.h>\n#include <string.h>\n\n#define SW 128\n#define SH 64\nstatic uint8_t fb[SW * SH / 8];\n\nstatic void fb_clear(void){ memset(fb,0,sizeof(fb)); }\nstatic void px(int x,int y){\n    if(x<0||x>=SW||y<0||y>=SH)return;\n    fb[x+(y>>3)*SW] |= (uint8_t)(1u<<(y&7));\n}\nstatic void box(int x,int y,int w,int h){\n    for(int yy=y;yy<y+h;yy++) for(int xx=x;xx<x+w;xx++) px(xx,yy);\n}\nstatic void frame(void){\n    for(uint8_t page=0;page<8;page++){\n        JOY_OLED_data_start(page);\n        for(uint8_t x=0;x<128;x++) JOY_OLED_send(fb[x+page*128]);\n        JOY_OLED_end();\n    }\n}\nstatic void glyph(char c, uint8_t out[5]){\n    memset(out,0,5);\n    switch(c){\n    case \'A\':{uint8_t a[5]={0x7e,0x11,0x11,0x11,0x7e};memcpy(out,a,5);}break;\n    case \'B\':{uint8_t a[5]={0x7f,0x49,0x49,0x49,0x36};memcpy(out,a,5);}break;\n    case \'C\':{uint8_t a[5]={0x3e,0x41,0x41,0x41,0x22};memcpy(out,a,5);}break;\n    case \'D\':{uint8_t a[5]={0x7f,0x41,0x41,0x22,0x1c};memcpy(out,a,5);}break;\n    case \'E\':{uint8_t a[5]={0x7f,0x49,0x49,0x49,0x41};memcpy(out,a,5);}break;\n    case \'F\':{uint8_t a[5]={0x7f,0x09,0x09,0x09,0x01};memcpy(out,a,5);}break;\n    case \'G\':{uint8_t a[5]={0x3e,0x41,0x49,0x49,0x7a};memcpy(out,a,5);}break;\n    case \'H\':{uint8_t a[5]={0x7f,0x08,0x08,0x08,0x7f};memcpy(out,a,5);}break;\n    case \'I\':{uint8_t a[5]={0x00,0x41,0x7f,0x41,0x00};memcpy(out,a,5);}break;\n    case \'J\':{uint8_t a[5]={0x20,0x40,0x41,0x3f,0x01};memcpy(out,a,5);}break;\n    case \'K\':{uint8_t a[5]={0x7f,0x08,0x14,0x22,0x41};memcpy(out,a,5);}break;\n    case \'L\':{uint8_t a[5]={0x7f,0x40,0x40,0x40,0x40};memcpy(out,a,5);}break;\n    case \'M\':{uint8_t a[5]={0x7f,0x02,0x0c,0x02,0x7f};memcpy(out,a,5);}break;\n    case \'N\':{uint8_t a[5]={0x7f,0x04,0x08,0x10,0x7f};memcpy(out,a,5);}break;\n    case \'O\':{uint8_t a[5]={0x3e,0x41,0x41,0x41,0x3e};memcpy(out,a,5);}break;\n    case \'P\':{uint8_t a[5]={0x7f,0x09,0x09,0x09,0x06};memcpy(out,a,5);}break;\n    case \'Q\':{uint8_t a[5]={0x3e,0x41,0x51,0x21,0x5e};memcpy(out,a,5);}break;\n    case \'R\':{uint8_t a[5]={0x7f,0x09,0x19,0x29,0x46};memcpy(out,a,5);}break;\n    case \'S\':{uint8_t a[5]={0x46,0x49,0x49,0x49,0x31};memcpy(out,a,5);}break;\n    case \'T\':{uint8_t a[5]={0x01,0x01,0x7f,0x01,0x01};memcpy(out,a,5);}break;\n    case \'U\':{uint8_t a[5]={0x3f,0x40,0x40,0x40,0x3f};memcpy(out,a,5);}break;\n    case \'V\':{uint8_t a[5]={0x1f,0x20,0x40,0x20,0x1f};memcpy(out,a,5);}break;\n    case \'W\':{uint8_t a[5]={0x3f,0x40,0x38,0x40,0x3f};memcpy(out,a,5);}break;\n    case \'X\':{uint8_t a[5]={0x63,0x14,0x08,0x14,0x63};memcpy(out,a,5);}break;\n    case \'Y\':{uint8_t a[5]={0x07,0x08,0x70,0x08,0x07};memcpy(out,a,5);}break;\n    case \'Z\':{uint8_t a[5]={0x61,0x51,0x49,0x45,0x43};memcpy(out,a,5);}break;\n    case \'0\':{uint8_t a[5]={0x3e,0x51,0x49,0x45,0x3e};memcpy(out,a,5);}break;\n    case \'1\':{uint8_t a[5]={0x00,0x42,0x7f,0x40,0x00};memcpy(out,a,5);}break;\n    case \'2\':{uint8_t a[5]={0x42,0x61,0x51,0x49,0x46};memcpy(out,a,5);}break;\n    case \'3\':{uint8_t a[5]={0x21,0x41,0x45,0x4b,0x31};memcpy(out,a,5);}break;\n    case \'4\':{uint8_t a[5]={0x18,0x14,0x12,0x7f,0x10};memcpy(out,a,5);}break;\n    case \'5\':{uint8_t a[5]={0x27,0x45,0x45,0x45,0x39};memcpy(out,a,5);}break;\n    case \'6\':{uint8_t a[5]={0x3c,0x4a,0x49,0x49,0x30};memcpy(out,a,5);}break;\n    case \'7\':{uint8_t a[5]={0x01,0x71,0x09,0x05,0x03};memcpy(out,a,5);}break;\n    case \'8\':{uint8_t a[5]={0x36,0x49,0x49,0x49,0x36};memcpy(out,a,5);}break;\n    case \'9\':{uint8_t a[5]={0x06,0x49,0x49,0x29,0x1e};memcpy(out,a,5);}break;\n    case \':\':{uint8_t a[5]={0,0x36,0x36,0,0};memcpy(out,a,5);}break;\n    case \'-\':{uint8_t a[5]={0x08,0x08,0x08,0x08,0x08};memcpy(out,a,5);}break;\n    default:break;\n    }\n}\nstatic void text(int x,int y,const char* s){\n    uint8_t g[5];\n    while(*s){\n        glyph(*s++,g);\n        for(int cx=0;cx<5;cx++) for(int cy=0;cy<7;cy++) if(g[cx]&(1u<<cy)) px(x+cx,y+cy);\n        x+=6;\n    }\n}\nstatic bool hit(int x,int y,int ox,int oy,int ow,int oh){\n    return x>=ox && x<ox+ow && y>=oy && y<oy+oh;\n}\nstatic void wait_release(void){ while(JOY_act_pressed()){JOY_idle();DLY_ms(10);} }\n\nint cyber_snake_run(void){\n    JOY_init();\n    int8_t sx[64],sy[64]; int len=5,dir=0,fx=25,fy=12,score=0;\n    for(int i=0;i<len;i++){sx[i]=12-i;sy[i]=12;}\n    uint16_t tick=0;\n    while(1){\n        if(JOY_exit())break;\n        if(JOY_left_pressed()){dir=(dir+3)&3;DLY_ms(100);}\n        if(JOY_right_pressed()){dir=(dir+1)&3;DLY_ms(100);}\n        if(++tick>=11){\n            tick=0;\n            for(int i=len-1;i>0;i--){sx[i]=sx[i-1];sy[i]=sy[i-1];}\n            if(dir==0)sx[0]++; else if(dir==1)sy[0]++; else if(dir==2)sx[0]--; else sy[0]--;\n            if(sx[0]<0)sx[0]=31;if(sx[0]>31)sx[0]=0;if(sy[0]<1)sy[0]=14;if(sy[0]>14)sy[0]=1;\n            for(int i=1;i<len;i++)if(sx[0]==sx[i]&&sy[0]==sy[i]){len=5;score=0;}\n            if(sx[0]==fx&&sy[0]==fy){if(len<63)len++;score++;fx=JOY_random()%32;fy=1+JOY_random()%14;}\n        }\n        fb_clear();text(2,1,"SNAKE");box(fx*4,fy*4,3,3);\n        for(int i=0;i<len;i++)box(sx[i]*4,sy[i]*4,3,3);\n        frame();JOY_idle();DLY_ms(10);\n    }return score;\n}\nint cyber_pong_run(void){\n    JOY_init();int py=24,ay=24,bx=64,by=32,vx=-2,vy=1,score=0;\n    while(1){\n        if(JOY_exit())break;\n        if(JOY_left_pressed()&&py>10)py-=2;\n        if(JOY_right_pressed()&&py<50)py+=2;\n        bx+=vx;by+=vy;if(by<9||by>61)vy=-vy;\n        if(by>ay+5)ay++;else if(by<ay+5)ay--;\n        if(bx<=6&&by>=py&&by<=py+12){vx=2;score++;}\n        if(bx>=121&&by>=ay&&by<=ay+12)vx=-2;\n        if(bx<0){bx=64;by=32;score=0;vx=-2;}\n        if(bx>127){bx=64;by=32;vx=-2;}\n        fb_clear();text(2,1,"PONG");box(3,py,3,13);box(122,ay,3,13);box(bx,by,3,3);\n        for(int y=10;y<64;y+=8)box(63,y,1,4);\n        frame();JOY_idle();DLY_ms(24);\n    }return score;\n}\nint cyber_dodge_run(void){\n    JOY_init();int lane=1,oy=-10,olane=0,score=0,scroll=0;bool l=false,r=false;\n    while(1){\n        if(JOY_exit())break;\n        bool nl=JOY_left_pressed(),nr=JOY_right_pressed();\n        if(nl&&!l&&lane>0)lane--;if(nr&&!r&&lane<2)lane++;l=nl;r=nr;\n        oy+=2;scroll=(scroll+2)&7;\n        if(oy>64){oy=-8;olane=JOY_random()%3;score++;}\n        if(oy>47&&olane==lane){oy=-8;score=0;}\n        fb_clear();text(2,1,"DODGE");\n        for(int y=10+scroll;y<64;y+=8){box(42,y,1,4);box(85,y,1,4);}\n        box(14+lane*43,52,8,10);box(14+olane*43,oy,8,8);\n        frame();JOY_idle();DLY_ms(55);\n    }return score;\n}\nint cyber_reaction_run(void){\n    JOY_init();uint16_t delay=900+(JOY_random()%2200),elapsed=0;bool early=false;\n    fb_clear();text(39,25,"WAIT");frame();wait_release();\n    while(elapsed<delay){\n        if(JOY_exit())return 0;\n        if(JOY_act_pressed()){early=true;break;}\n        JOY_idle();DLY_ms(10);elapsed+=10;\n    }\n    if(early){fb_clear();text(31,25,"TOO SOON");frame();DLY_ms(900);wait_release();return 0;}\n    fb_clear();text(49,25,"GO");frame();elapsed=0;\n    while(!JOY_act_pressed()&&elapsed<5000){if(JOY_exit())return 0;JOY_idle();DLY_ms(10);elapsed+=10;}\n    fb_clear();text(24,18,"REACTION");char n[6];n[0]=\'0\'+((elapsed/1000)%10);n[1]=\'0\'+((elapsed/100)%10);n[2]=\'0\'+((elapsed/10)%10);n[3]=\'0\';text(50,34,n);text(72,34,"MS");frame();DLY_ms(1500);wait_release();return elapsed;\n}\nint cyber_nba2k_run(void){\n    JOY_init();int x=16,y=42,vx=2,vy=-4,phase=0;\n    while(1){\n        if(JOY_exit())break;\n        vy++;x+=vx;y+=vy;\n        if(x<8||x>118)vx=-vx;\n        if(y>54){y=54;vy=-7;}if(y<18)vy=1;\n        fb_clear();text(42,3,"NBA 2K");text(24,15,"COMING SOON");text(17,26,"SALARY CAP: 2KB");text(21,37,"NO MICROTX");\n        box(104,45,2,14);box(96,45,10,2);box(x,y,5,5);\n        for(int i=0;i<5;i++)px(x+i,y+2);for(int i=0;i<5;i++)px(x+2,y+i);\n        frame();JOY_idle();DLY_ms(55);phase++;\n    }return 0;\n}\n'
CYBER_GAMES_H = '#ifndef CYBER_GAMES_H\n#define CYBER_GAMES_H\nint cyber_snake_run(void);\nint cyber_pong_run(void);\nint cyber_dodge_run(void);\nint cyber_reaction_run(void);\nint cyber_nba2k_run(void);\n#endif\n'

def c_array(name: str, data: bytes) -> str:
    rows=[]
    for i in range(0,len(data),16):
        rows.append('    '+', '.join(f'0x{b:02x}' for b in data[i:i+16])+',')
    return f'static const uint8_t {name}[540] = {{\n'+'\n'.join(rows)+'\n};\n'

def build_shortcuts_source():
    import base64
    cards={k:base64.b64decode(v) for k,v in EMBEDDED_CARDS_B64.items()}
    arrays='\n'.join(c_array(k,data) for k,data in cards.items())
    return r'''#include "cyber_shortcuts.h"
#include "app_timer.h"
#include "app_error.h"
#include "ntag_emu.h"
#include "ntag_def.h"
#include "boards.h"
#include "nrf_delay.h"
#include "nrf_gpio.h"
#include <string.h>

#define CYBER_SEQ_TIMEOUT_MS 520
#define CYBER_LEFT_TIMEOUT_MS 650
APP_TIMER_DEF(m_cyber_seq_timer);
APP_TIMER_DEF(m_cyber_left_timer);

static cyber_replay_cb_t m_replay;
static mui_input_event_t m_seq[8];
static uint8_t m_seq_len;
static uint8_t m_left_count;
static ntag_t m_action_tag;

''' + arrays + r'''
static void blink_confirm(uint8_t count) {
#ifdef LCD_BL_PIN
    for (uint8_t i=0;i<count;i++) {
        nrf_gpio_pin_write(LCD_BL_PIN, 0);
        nrf_delay_ms(55);
        nrf_gpio_pin_write(LCD_BL_PIN, 1);
        nrf_delay_ms(55);
    }
#else
    (void)count;
#endif
}

static void load_action(const uint8_t *data, const char *details, uint8_t blinks) {
    memset(&m_action_tag, 0, sizeof(m_action_tag));
    memcpy(m_action_tag.data, data, NTAG_DATA_SIZE);
    strncpy((char*)m_action_tag.notes, details, sizeof(m_action_tag.notes)-1);
    m_action_tag.read_only = true;
    m_action_tag.type = NTAG_215;
    ntag_emu_set_tag(&m_action_tag);
    blink_confirm(blinks);
}

static bool all_key(input_key_t key) {
    for (uint8_t i=0;i<m_seq_len;i++) if (m_seq[i].key != key) return false;
    return true;
}

static void replay_one(mui_input_event_t e) {
    if (!m_replay) return;
    if (e.key == INPUT_KEY_BACK) {
        mui_input_event_t back = {.key=INPUT_KEY_CENTER,.type=INPUT_TYPE_LONG};
        m_replay(&back);
    } else {
        m_replay(&e);
    }
}

static void clear_seq(void) {
    m_seq_len=0;
    app_timer_stop(m_cyber_seq_timer);
}

static void seq_timeout(void *ctx) {
    (void)ctx;
    if (m_seq_len==5 && all_key(INPUT_KEY_BACK)) {
        load_action(govee_data, "Tap iPhone. Govee On.", 5);
    } else {
        for (uint8_t i=0;i<m_seq_len;i++) replay_one(m_seq[i]);
    }
    clear_seq();
}

static void left_timeout(void *ctx) { (void)ctx; m_left_count=0; }

void cyber_shortcuts_init(cyber_replay_cb_t replay_cb) {
    m_replay=replay_cb;
    m_seq_len=0;
    m_left_count=0;
    ret_code_t e=app_timer_create(&m_cyber_seq_timer, APP_TIMER_MODE_SINGLE_SHOT, seq_timeout);
    APP_ERROR_CHECK(e);
    e=app_timer_create(&m_cyber_left_timer, APP_TIMER_MODE_SINGLE_SHOT, left_timeout);
    APP_ERROR_CHECK(e);
}

bool cyber_shortcuts_handle(mui_input_event_t *e) {
    if (e->type != INPUT_TYPE_SHORT) return false;

    /* Left x5: Find My Car. Normal left movement remains responsive. */
    if (e->key == INPUT_KEY_LEFT && m_seq_len==0) {
        m_left_count++;
        app_timer_stop(m_cyber_left_timer);
        app_timer_start(m_cyber_left_timer, APP_TIMER_TICKS(CYBER_LEFT_TIMEOUT_MS), NULL);
        if (m_left_count >= 5) {
            m_left_count=0;
            app_timer_stop(m_cyber_left_timer);
            load_action(find_car_data, "Tap iPhone. Find My Car.", 3);
            return true;
        }
        return false;
    }

    /* Back begins a buffered gesture. Right is buffered only after Back. */
    if (m_seq_len==0 && e->key != INPUT_KEY_BACK) return false;
    if (m_seq_len>0 && e->key != INPUT_KEY_BACK && e->key != INPUT_KEY_RIGHT) {
        for (uint8_t i=0;i<m_seq_len;i++) replay_one(m_seq[i]);
        clear_seq();
        return false;
    }

    if (m_seq_len < 8) m_seq[m_seq_len++] = *e;
    app_timer_stop(m_cyber_seq_timer);

    /* Back, Right, Back, Back: Meditation Cyber. */
    if (m_seq_len==4 &&
        m_seq[0].key==INPUT_KEY_BACK && m_seq[1].key==INPUT_KEY_RIGHT &&
        m_seq[2].key==INPUT_KEY_BACK && m_seq[3].key==INPUT_KEY_BACK) {
        load_action(meditation_data, "Tap iPhone. 15-sec Stoic mist.", 2);
        clear_seq();
        return true;
    }

    /* Back x6: Flashlight. Back x5 waits for timeout and becomes Govee. */
    if (m_seq_len==6 && all_key(INPUT_KEY_BACK)) {
        load_action(flashlight_data, "Tap iPhone. Flashlight.", 6);
        clear_seq();
        return true;
    }

    /* If no target can still match, replay immediately. */
    bool prefix=true;
    if (m_seq[0].key!=INPUT_KEY_BACK) prefix=false;
    if (m_seq_len>=2 && m_seq[1].key!=INPUT_KEY_BACK && m_seq[1].key!=INPUT_KEY_RIGHT) prefix=false;
    if (m_seq_len>=3 && m_seq[1].key==INPUT_KEY_RIGHT && m_seq[2].key!=INPUT_KEY_BACK) prefix=false;
    if (m_seq_len>=5 && m_seq[1].key==INPUT_KEY_RIGHT) prefix=false;
    if (!prefix || m_seq_len>6) {
        for (uint8_t i=0;i<m_seq_len;i++) replay_one(m_seq[i]);
        clear_seq();
        return true;
    }

    app_timer_start(m_cyber_seq_timer, APP_TIMER_TICKS(CYBER_SEQ_TIMEOUT_MS), NULL);
    return true;
}
'''

SHORTCUTS_H = r'''#ifndef CYBER_SHORTCUTS_H
#define CYBER_SHORTCUTS_H
#include <stdbool.h>
#include "mui_input.h"
typedef void (*cyber_replay_cb_t)(mui_input_event_t *event);
void cyber_shortcuts_init(cyber_replay_cb_t replay_cb);
bool cyber_shortcuts_handle(mui_input_event_t *event);
#endif
'''

def must_replace(path: Path, old: str, new: str):
    txt=path.read_text()
    if old not in txt:
        raise SystemExit(f'Patch target not found in {path}: {old[:80]!r}')
    path.write_text(txt.replace(old,new,1))

def patch(repo: Path):
    src=repo/'fw/application/src'
    board=src/'boards/board_lcd.h'
    must_replace(board, '#define BUTTONS_NUMBER 3', '#define BUTTONS_NUMBER 4')
    must_replace(board, '#define BUTTON_3       7\n#define BUTTON_STOP    7',
                 '#define BUTTON_3       7\n#define BUTTON_4       8  // Wuzplay fourth/back key\n#define BUTTON_STOP    8')
    must_replace(board, '#define BUTTONS_LIST { BUTTON_1, BUTTON_2, BUTTON_3}',
                 '#define BUTTONS_LIST { BUTTON_1, BUTTON_2, BUTTON_3, BUTTON_4}')
    must_replace(board, '#define BSP_BUTTON_2   BUTTON_3',
                 '#define BSP_BUTTON_2   BUTTON_3\n#define BSP_BUTTON_3   BUTTON_4')
    must_replace(board, '// #define APP_GAME_ENABLE', '#define APP_GAME_ENABLE')

    bsp=src/'mod/bsp_btn.c'
    must_replace(bsp,
        '    {BSP_BUTTON_2, false, BUTTON_PULL, bsp_button_event_handler},\n};',
        '    {BSP_BUTTON_2, false, BUTTON_PULL, bsp_button_event_handler},\n    {BSP_BUTTON_3, false, BUTTON_PULL, bsp_button_event_handler},\n};')

    inp_h=src/'mui/mui_input.h'
    must_replace(inp_h,
        '    INPUT_KEY_LEFT,\n    INPUT_KEY_CENTER,\n    INPUT_KEY_RIGHT\n',
        '    INPUT_KEY_LEFT,\n    INPUT_KEY_CENTER,\n    INPUT_KEY_RIGHT,\n    INPUT_KEY_BACK\n')

    inp=src/'mui/mui_input.c'
    must_replace(inp, '#include "cache.h"', '#include "cache.h"\n#include "cyber_shortcuts.h"')
    must_replace(inp,
'''    case BSP_BTN_EVENT_SHORT: {
        NRF_LOG_DEBUG("Key %d short push", btn);
        mui_input_event_t input_event = {.key = btn,
                                         .type = INPUT_TYPE_SHORT};
        mui_input_post_event(&input_event);
        break;
    }''',
'''    case BSP_BTN_EVENT_SHORT: {
        NRF_LOG_DEBUG("Key %d short push", btn);
        mui_input_event_t input_event = {.key = btn,
                                         .type = INPUT_TYPE_SHORT};
        if (!cyber_shortcuts_handle(&input_event)) {
            mui_input_post_event(&input_event);
        }
        break;
    }''')
    must_replace(inp,
'''void mui_input_init() {
    bsp_btn_init(mui_input_on_bsp_btn_event);
    
}''',
'''void mui_input_init() {
    cyber_shortcuts_init(mui_input_post_event);
    bsp_btn_init(mui_input_on_bsp_btn_event);
}''')

    # Game sources and list.
    game_dir=src/'app/game/port/cyber_games'
    game_dir.mkdir(parents=True,exist_ok=True)
    (game_dir/'cyber_games.c').write_text(CYBER_GAMES_C)
    (game_dir/'cyber_games.h').write_text(CYBER_GAMES_H)
    (src/'mod/cyber_shortcuts.c').write_text(build_shortcuts_source())
    (src/'mod/cyber_shortcuts.h').write_text(SHORTCUTS_H)

    gl=src/'app/game/scene/game_scene_game_list.c'
    must_replace(gl, '#include "tiny_tris.h"', '#include "tiny_tris.h"\n#include "../port/cyber_games/cyber_games.h"')
    must_replace(gl,
'''    mui_list_view_add_item(app->p_list_view, ICON_FILE, _T(APP_GAME_TINY_TRIS), tiny_tris_run);
}''',
'''    mui_list_view_add_item(app->p_list_view, ICON_FILE, "Snake", cyber_snake_run);
    mui_list_view_add_item(app->p_list_view, ICON_FILE, "Pong", cyber_pong_run);
    mui_list_view_add_item(app->p_list_view, ICON_FILE, "Breakout", tiny_arkanoid_run);
    mui_list_view_add_item(app->p_list_view, ICON_FILE, "Dodge", cyber_dodge_run);
    mui_list_view_add_item(app->p_list_view, ICON_FILE, "Reaction", cyber_reaction_run);
    mui_list_view_add_item(app->p_list_view, ICON_FILE, "NBA 2K - Coming Soon", cyber_nba2k_run);
    mui_list_view_add_item(app->p_list_view, ICON_FILE, _T(APP_GAME_TINY_LANDER), tiny_lander_run);
    mui_list_view_add_item(app->p_list_view, ICON_FILE, _T(APP_GAME_TINY_INVADERS), tiny_invaders_run);
    mui_list_view_add_item(app->p_list_view, ICON_FILE, _T(APP_GAME_TINY_TRIS), tiny_tris_run);
}''')
    # Long-select from game list exits to previous app page.
    must_replace(gl,
'''        } else {
            mini_app_launcher_kill(mini_app_launcher(), MINI_APP_ID_GAME);
        }
    } else {
    }''',
'''        } else {
            mini_app_launcher_kill(mini_app_launcher(), MINI_APP_ID_GAME);
        }
    } else if (event == MUI_LIST_VIEW_EVENT_LONG_SELECTED) {
        mini_app_launcher_kill(mini_app_launcher(), MINI_APP_ID_GAME);
    }''')

    mf=repo/'fw/application/Makefile'
    must_replace(mf,
        '  $(PROJ_DIR)/mod/bsp_btn.c \\\n',
        '  $(PROJ_DIR)/mod/bsp_btn.c \\\n  $(PROJ_DIR)/mod/cyber_shortcuts.c \\\n')
    must_replace(mf,
        '  $(PROJ_DIR)/app/game/port/common/driver.c \\\n',
        '  $(PROJ_DIR)/app/game/port/common/driver.c \\\n  $(PROJ_DIR)/app/game/port/cyber_games/cyber_games.c \\\n')

    print('Wuzplay Cyberdeck v9 patches applied')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('upstream',type=Path)
    args=ap.parse_args()
    patch(args.upstream.resolve())
