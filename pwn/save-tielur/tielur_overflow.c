#define _POSIX_C_SOURCE 200809L
#include <ctype.h>
#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/select.h>
#include <termios.h>
#include <time.h>
#include <unistd.h>

#define START_HP 4026579840u
#define TICK_DAMAGE 268435456u
#define CRITICAL_HP 268483456u
#define UINT32_MAX_VALUE 4294967295u
#define INVENTORY_COUNT 20
#define BAR_WIDTH 42
#define MAX_LINE 512
#define DEATH_STEPS 3

#define C_RESET    "\033[0m"
#define C_BOLD     "\033[1m"
#define C_DIM      "\033[2m"
#define C_TITLE    "\033[38;2;188;247;119m"
#define C_FRAME    "\033[38;2;223;53;117m"
#define C_PROMPT   "\033[38;2;142;219;235m"
#define C_TEXT     "\033[38;2;237;227;231m"
#define C_HEALTHY  "\033[38;2;107;226;89m"
#define C_CRIT     "\033[38;2;249;242;78m"
#define C_DEATH    "\033[38;2;238;49;87m"
#define C_SUCCESS  "\033[38;2;86;240;156m"
#define C_BOSS     "\033[38;2;255;92;92m"
#define C_PANEL_BG "\033[48;2;44;20;38m"
#define C_BG_TINT  "\033[48;2;21;9;15m"

static const char *inventory_names[INVENTORY_COUNT] = {
    "Gravy", "McFlurry", "Footlong Sub", "Chicken",
    "Fried Chicken", "Big Mac", "Meatballs", "Salt Water",
    "Popcorn Chicken", "Filet-O-Fish", "Squid", "Nemo",
    "Mashed Potatos", "Nuggets", "Chipotle", "Refined Sugar",
    "Biscuit", "Soup", "Six-Inch Combo", "Cheese"
};

static const uint32_t inventory_heals[INVENTORY_COUNT] = {
    536864881u, 536865136u, 536864882u, 536865392u, 536864884u,
    536865904u, 536866928u, 536864888u, 536868976u, 536864896u,
    536873072u, 536881264u, 536864912u, 536897648u, 536930416u,
    536864944u, 536995952u, 537127024u, 536865008u, 537389168u
};

typedef enum {
    STATE_PREP = 0,
    STATE_RUNNING,
    STATE_RESOLUTION,
    STATE_FINAL_STRIKE,
    STATE_DYING,
    STATE_FAIL,
    STATE_SUCCESS
} FightState;

typedef struct {
    struct termios orig;
    int enabled;
    int is_tty;
} TerminalState;

static TerminalState term_state = {{0}, 0, 0};

static void disable_raw_mode(void) {
    if (term_state.enabled) {
        tcsetattr(STDIN_FILENO, TCSAFLUSH, &term_state.orig);
        term_state.enabled = 0;
    }
}

static void enable_raw_mode_if_tty(void) {
    term_state.is_tty = isatty(STDIN_FILENO);
    if (!term_state.is_tty) return;
    if (tcgetattr(STDIN_FILENO, &term_state.orig) == -1) return;

    struct termios raw = term_state.orig;
    raw.c_iflag &= ~(ICRNL | IXON);
    raw.c_lflag &= ~(ECHO | ICANON);
    raw.c_cc[VMIN] = 0;
    raw.c_cc[VTIME] = 0;

    if (tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw) == 0) {
        term_state.enabled = 1;
        atexit(disable_raw_mode);
    }
}

static uint64_t now_usec(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000ull + (uint64_t)ts.tv_nsec / 1000ull;
}

static void clear_screen(void) {
    fputs("\033[2J\033[H", stdout);
}

static double display_percent(uint32_t hp) {
    if (hp == UINT32_MAX_VALUE) return 100.0;
    if (hp == 0) return 0.0;
    return (100.0 * (double)hp) / (double)START_HP;
}

static const char *hp_color(uint32_t hp) {
    if (hp == 0) return C_DEATH;
    if (hp <= CRITICAL_HP) return C_CRIT;
    if (hp >= START_HP / 2) return C_HEALTHY;
    return C_PROMPT;
}

static void build_bar(uint32_t hp, char *out, size_t out_sz) {
    int filled;

    if (hp == UINT32_MAX_VALUE) {
        filled = BAR_WIDTH;
    } else {
        filled = (int)(((double)hp / (double)START_HP) * BAR_WIDTH + 0.5);
        if (filled < 0) filled = 0;
        if (filled > BAR_WIDTH) filled = BAR_WIDTH;
    }

    if (out_sz < (size_t)BAR_WIDTH + 3) return;

    size_t pos = 0;
    out[pos++] = '[';
    for (int i = 0; i < BAR_WIDTH; i++) out[pos++] = (i < filled ? '#' : '-');
    out[pos++] = ']';
    out[pos] = '\0';
}

static void show_inventory_table(int panel_mode) {
    if (panel_mode == 0) return;

    printf(C_PANEL_BG C_TITLE C_BOLD " Inventory " C_RESET "\n");
    for (int i = 0; i < INVENTORY_COUNT; i++) {
        printf(C_TEXT "  %2d. " C_PROMPT "%-20s " C_TITLE "%" PRIu32 "\n" C_RESET,
               i + 1, inventory_names[i], inventory_heals[i]);
    }
}

static void read_flag(char *buf, size_t sz) {
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        snprintf(buf, sz, "flag.txt missing");
        return;
    }

    if (!fgets(buf, (int)sz, f)) snprintf(buf, sz, "flag read failed");
    fclose(f);

    size_t n = strlen(buf);
    while (n && (buf[n - 1] == '\n' || buf[n - 1] == '\r')) buf[--n] = '\0';
}

static uint32_t parse_prepare(char *line, int *ok, char *chosen, size_t chosen_sz) {
    uint32_t total = 0;
    unsigned mask = 0;
    int count = 0;

    chosen[0] = '\0';

    char *tok = strtok(line, " \t\r\n");
    tok = strtok(NULL, " \t\r\n");

    while (tok) {
        char *end = NULL;
        long idx = strtol(tok, &end, 10);

        if (*tok == '\0' || *end != '\0' || idx < 1 || idx > INVENTORY_COUNT) {
            *ok = 0;
            return 0;
        }

        unsigned bit = 1u << (idx - 1);
        if (mask & bit) {
            *ok = 0;
            return 0;
        }

        mask |= bit;
        total += inventory_heals[idx - 1];

        if (count > 0) strncat(chosen, " ", chosen_sz - strlen(chosen) - 1);
        strncat(chosen, tok, chosen_sz - strlen(chosen) - 1);

        count++;
        tok = strtok(NULL, " \t\r\n");
    }

    *ok = count > 0;
    return *ok ? total : 0;
}

static uint32_t death_chunk(uint32_t hp, int steps_left) {
    if (hp == 0) return 0;
    if (steps_left <= 1) return hp;

    uint32_t chunk = hp / (uint32_t)steps_left;
    if (hp % (uint32_t)steps_left) chunk++;
    if (chunk == 0) chunk = 1;
    if (chunk > hp) chunk = hp;

    return chunk;
}

static void print_status(const char *message) {
    if (strstr(message, "SUCCESS:")) {
        printf(C_SUCCESS C_BOLD "Status: %s\n" C_RESET, message);
    } else if (strstr(message, "fully dies") ||
               strstr(message, "collapsing") ||
               strstr(message, "wrong value")) {
        printf(C_DEATH C_BOLD "Status: %s\n" C_RESET, message);
    } else {
        printf(C_TEXT "Status: %s\n" C_RESET, message);
    }
}

static const char *phase_label(FightState state) {
    switch (state) {
        case STATE_PREP:         return "PREP";
        case STATE_RUNNING:      return "RUNNING";
        case STATE_RESOLUTION:   return "RESOLUTION";
        case STATE_FINAL_STRIKE: return "FINAL STRIKE";
        case STATE_DYING:        return "DYING";
        case STATE_FAIL:         return "FAIL";
        case STATE_SUCCESS:      return "SUCCESS";
        default:                 return "UNKNOWN";
    }
}

static int state_uses_timer(FightState state) {
    return state == STATE_RUNNING ||
           state == STATE_RESOLUTION ||
           state == STATE_FINAL_STRIKE ||
           state == STATE_DYING;
}

static void draw_ui(uint32_t hp,
                    const char *message,
                    const char *plan_text,
                    uint32_t plan_total,
                    int plan_locked,
                    int tick_no,
                    int panel_mode,
                    const char *input_buf,
                    FightState state) {
    char bar[BAR_WIDTH + 3];
    const char *hpcol = hp_color(hp);

    build_bar(hp, bar, sizeof(bar));
    clear_screen();

    printf(C_BG_TINT);
    printf(C_FRAME "==============================================\n" C_RESET);
    printf(C_PANEL_BG C_TITLE C_BOLD "         SAVE TIELUR         " C_RESET "\n");
    printf(C_FRAME "==============================================\n" C_RESET);
    printf(C_BOSS "             .-\"\"\"-.\n" C_RESET);
    printf(C_BOSS "            / .===. \\\n" C_RESET);
    printf(C_BOSS "            \\/ o o  \\\n" C_RESET);
    printf(C_BOSS "            (   ^   )\n" C_RESET);
    printf(C_BOSS "          ___) '-' (___\n" C_RESET);
    printf(C_BOSS "         /___  /_\\  ___\\\n" C_RESET);
    printf(C_BOSS "             \\/   \\\n" C_RESET);
    printf(C_PANEL_BG C_TEXT C_BOLD "           RR LEADER: TIELUR         " C_RESET "\n\n");

    printf(C_TEXT " HP: " C_RESET "%s%" PRIu32 C_RESET C_TEXT " / %" PRIu32 "  (%.4f%%)\n" C_RESET,
           hpcol, hp, START_HP, display_percent(hp));
    printf(" %s%s" C_RESET "\n", hpcol, bar);
    printf(C_DEATH " Tick damage: -%u HP every 0.4s\n" C_RESET, TICK_DAMAGE);
    printf(C_FRAME " Last health loss: Up to 99.99999997671708%% of Maximum (ULTIMATE MOVE)\n" C_RESET);
    printf(C_PROMPT " Tick count: %d\n" C_RESET, tick_no);
    printf(C_PROMPT " Phase: %s\n" C_RESET, phase_label(state));

    if (plan_locked) {
        printf(C_TITLE " Locked heal plan: %s  (total %" PRIu32 ")\n" C_RESET, plan_text, plan_total);
    } else {
        printf(C_DIM " Locked heal plan: none\n" C_RESET);
    }

    puts("");

    if (panel_mode == 0) {
        printf(C_DIM "Inventory hidden. Type 'inventory' to open it.\n" C_RESET);
    } else {
        show_inventory_table(panel_mode);
    }

    puts("");

    printf(C_FRAME "Commands: " C_PROMPT "heal <0 1 2 3...>" C_FRAME " | " C_PROMPT "inventory\n" C_RESET);

    if (message && *message) print_status(message);

    printf(C_PROMPT C_BOLD "input: " C_RESET "%s", input_buf ? input_buf : "");
    fflush(stdout);
}

static void trim_command(char *line) {
    size_t n = strlen(line);
    while (n > 0 && isspace((unsigned char)line[n - 1])) line[--n] = '\0';

    size_t start = 0;
    while (line[start] && isspace((unsigned char)line[start])) start++;

    if (start > 0) memmove(line, line + start, strlen(line + start) + 1);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    enable_raw_mode_if_tty();

    uint32_t hp = START_HP;
    uint32_t plan_total = 0;
    int tick_no = 0;
    int plan_locked = 0;
    int panel_mode = 0;
    int death_steps_left = 0;

    FightState state = STATE_PREP;

    char plan_text[128] = "";
    char status[256] = "Choose a heal plan. Combat begins only after a valid heal selection";
    char flagbuf[128] = "";
    char input_buf[MAX_LINE] = "";

    size_t input_len = 0;
    int esc_state = 0;
    char csi_buf[32] = "";
    size_t csi_len = 0;

    uint64_t next_tick = 0;

    draw_ui(hp, status, plan_text, plan_total, plan_locked, tick_no,
            panel_mode, input_buf, state);

    while (state != STATE_FAIL && state != STATE_SUCCESS) {
        if (state_uses_timer(state)) {
            uint64_t now = now_usec();

            while (now >= next_tick &&
                   state != STATE_FAIL &&
                   state != STATE_SUCCESS) {
                if (state == STATE_RUNNING) {
                    if (hp <= TICK_DAMAGE) {
                        hp = 0;
                        tick_no++;
                        snprintf(status, sizeof(status), "TIELUR Died...");
                        state = STATE_FAIL;
                    } else {
                        hp -= TICK_DAMAGE;
                        tick_no++;

                        if (hp == CRITICAL_HP) {
                            if (!plan_locked) {
                                death_steps_left = DEATH_STEPS;
                                snprintf(status, sizeof(status),
                                         "Critical window opened at %u HP, but no healing plan was prepared. TIELUR is going to die.",
                                         CRITICAL_HP);
                                state = STATE_DYING;
                            } else {
                                hp += plan_total;
                                snprintf(status, sizeof(status),
                                         "Critical window opened. Prepared healing burst triggered.");
                                state = STATE_RESOLUTION;
                            }
                        } else {
                            snprintf(status, sizeof(status), "TIELUR loses %u HP.", TICK_DAMAGE);
                        }
                    }
                } else if (state == STATE_RESOLUTION) {
                    hp -= TICK_DAMAGE;
                    tick_no++;

                    if (hp == UINT32_MAX_VALUE) {
                        snprintf(status, sizeof(status),
                                 "Perfect underflow achieved. Final strike sequence engaged.");
                        state = STATE_FINAL_STRIKE;
                    } else {
                        death_steps_left = DEATH_STEPS;
                        snprintf(status, sizeof(status),
                                 "Health landed on the wrong value (%" PRIu32 "). TIELUR starts dying.",
                                 hp);
                        state = STATE_DYING;
                    }
                } else if (state == STATE_FINAL_STRIKE) {
                    hp -= (UINT32_MAX_VALUE - 1u);
                    read_flag(flagbuf, sizeof(flagbuf));
                    snprintf(status, sizeof(status),
                             "SUCCESS: TIELUR survives the ULTIMATE MOVE with 1 HP left. %s",
                             flagbuf);
                    state = STATE_SUCCESS;
                } else if (state == STATE_DYING) {
                    uint32_t chunk = death_chunk(hp, death_steps_left);
                    hp -= chunk;
                    tick_no++;
                    death_steps_left--;

                    if (hp == 0 || death_steps_left <= 0) {
                        hp = 0;
                        snprintf(status, sizeof(status), "TIELUR is dead. You failed miserably.");
                        state = STATE_FAIL;
                    } else {
                        snprintf(status, sizeof(status),
                                 "TIELUR is dying: -%" PRIu32 " HP",
                                 chunk);
                    }
                }

                next_tick += 400000ull;
                now = now_usec();

                draw_ui(hp, status, plan_text, plan_total, plan_locked, tick_no,
                        panel_mode, input_buf, state);
            }
        }

        struct timeval tv;
        struct timeval *tv_ptr = NULL;

        if (state_uses_timer(state)) {
            uint64_t now2 = now_usec();
            uint64_t remaining = next_tick > now2 ? next_tick - now2 : 0;
            tv.tv_sec = (time_t)(remaining / 1000000ull);
            tv.tv_usec = (suseconds_t)(remaining % 1000000ull);
            tv_ptr = &tv;
        }

        fd_set rfds;
        FD_ZERO(&rfds);
        FD_SET(STDIN_FILENO, &rfds);

        int r = select(STDIN_FILENO + 1, &rfds, NULL, NULL, tv_ptr);
        if (r < 0) {
            if (errno == EINTR) continue;
            perror("select");
            return 1;
        }
        if (r == 0) continue;

        char ch;
        ssize_t n = read(STDIN_FILENO, &ch, 1);
        if (n <= 0) {
            if (!term_state.is_tty) break;
            continue;
        }

        if (esc_state == 1) {
            if (ch == '[') {
                esc_state = 2;
                csi_len = 0;
                csi_buf[0] = '\0';
            } else {
                esc_state = 0;
            }
            continue;
        }

        if (esc_state == 2) {
            if (csi_len + 1 < sizeof(csi_buf)) {
                csi_buf[csi_len++] = ch;
                csi_buf[csi_len] = '\0';
            }
            if ((unsigned char)ch >= '@' && (unsigned char)ch <= '~') {
                esc_state = 0;
                csi_len = 0;
                csi_buf[0] = '\0';
                draw_ui(hp, status, plan_text, plan_total, plan_locked, tick_no,
                        panel_mode, input_buf, state);
            }
            continue;
        }

        if (ch == 27) {
            esc_state = 1;
            continue;
        }

        if (ch == '\r' || ch == '\n') {
            char line[MAX_LINE];
            memcpy(line, input_buf, input_len);
            line[input_len] = '\0';
            trim_command(line);

            input_buf[0] = '\0';
            input_len = 0;

            if (strncmp(line, "inventory", 9) == 0 &&
                (line[9] == '\0' || isspace((unsigned char)line[9]))) {
                panel_mode = 1;
                snprintf(status, sizeof(status),
                         state == STATE_PREP
                             ? "Showing inventory panel. Time is frozen until you lock a heal plan."
                             : "Showing inventory panel.");
            } else if (strncmp(line, "heal", 4) == 0 &&
                       (line[4] == '\0' || isspace((unsigned char)line[4]))) {
                if (plan_locked) {
                    snprintf(status, sizeof(status), "Healing plan already locked: %s", plan_text);
                } else {
                    char work[MAX_LINE], chosen[128];
                    int ok = 0;

                    strncpy(work, line, sizeof(work) - 1);
                    work[sizeof(work) - 1] = '\0';

                    uint32_t total = parse_prepare(work, &ok, chosen, sizeof(chosen));
                    if (!ok) {
                        snprintf(status, sizeof(status), "Usage: heal <0 1 2 3...>");
                    } else {
                        plan_total = total;
                        strncpy(plan_text, chosen, sizeof(plan_text) - 1);
                        plan_text[sizeof(plan_text) - 1] = '\0';
                        plan_locked = 1;

                        if (state == STATE_PREP) {
                            state = STATE_RUNNING;
                            next_tick = now_usec() + 400000ull;
                            snprintf(status, sizeof(status),
                                     "Healing burst locked: %s. Combat begins now.",
                                     plan_text);
                        } else {
                            snprintf(status, sizeof(status),
                                     "Healing burst locked: %s",
                                     plan_text);
                        }
                    }
                }
            } else if (line[0] != '\0') {
                snprintf(status, sizeof(status), "Unknown command.");
            }

            draw_ui(hp, status, plan_text, plan_total, plan_locked, tick_no,
                    panel_mode, input_buf, state);
        } else if (ch == 127 || ch == '\b') {
            if (input_len > 0) {
                input_buf[--input_len] = '\0';
                draw_ui(hp, status, plan_text, plan_total, plan_locked, tick_no,
                        panel_mode, input_buf, state);
            }
        } else if (isprint((unsigned char)ch)) {
            if (input_len + 1 < sizeof(input_buf)) {
                input_buf[input_len++] = ch;
                input_buf[input_len] = '\0';
                draw_ui(hp, status, plan_text, plan_total, plan_locked, tick_no,
                        panel_mode, input_buf, state);
            }
        }
    }

    draw_ui(hp, status, plan_text, plan_total, plan_locked, tick_no,
            panel_mode, input_buf, state);
    puts("");

    return (state == STATE_SUCCESS) ? 0 : 1;
}