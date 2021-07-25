import curses
from curses import KEY_UP, KEY_DOWN

curses.initscr()
width = 60
height = 20
win = curses.newwin(height, width, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

score = 0
bat = [[width-2, height-6], [width-2, height-5], [width-2, height-4], [width-2, height-3], [width-2, height-2]]

key = 1

def print_char(string, mid_height, mid_width):
    string_len = len(string)
    mid_char = int((string_len + 1) / 2)
    for ind in range(string_len):
        win.addch(mid_height, mid_width - (mid_char - ind), string[ind])

def remove_char(string, mid_height, mid_width):
    string_len = len(string)
    mid_char = int((string_len + 1) / 2)
    for ind in range(string_len):
        win.addch(mid_height, mid_width - (mid_char - ind), " ")

# Draw the center line
mid_width = int((width - 1) / 2)
for ind in range(height):
    win.addch(ind, mid_width, '.')

# Draw initial bat
for ind in range(len(bat)):
    win.addch(bat[ind][1], bat[ind][0], '#')

# Pong Ball details
pong_ball = [[30, 5], [32, 13], [34, 15]]
index = 0
slope_x = 1
slope_y = 1
in_x = pong_ball[0][0]
in_y = pong_ball[0][1]


def get_pong_coords(in_x, in_y, slope_x, slope_y):
    clear_prev_pixel = True
    out_x = in_x + slope_x
    out_y = in_y + slope_y
    if [out_x, out_y] in bat:
        slope_x = -1
        slope_y = -bat.index([out_x, out_y])
        clear_prev_pixel = False
    if out_x <= int((width - 1) / 2):
        out_x = int((width - 1) / 2)
        slope_x = -slope_x
        # clear_prev_pixel = False
    if out_x >= width - 1:
        out_x = pong_ball[0][0]
        out_y = pong_ball[0][1]
        slope_x = 1
        slope_y = 1
        return out_x, out_y, slope_x, slope_y, True, clear_prev_pixel
    if (out_y > height - 1) or (out_y < 1):
        clear_prev_pixel = False
        if (out_y < 1):
            clear_prev_pixel = True
        out_y = in_y - slope_y
        slope_y = -slope_y
    return out_x, out_y, slope_x, slope_y, False, clear_prev_pixel


while key != 27:
    """Game will end when user presses ESC key
    """
    win.border(0)
    title_string = " Score: {:04d} {:>19} {:<23}".format(score%10000, "SOLO PONG", " ")
    win.addstr(0, 2, title_string)
    help_string = "{} {}".format(" Controls: UP DOWN ───", "SPACE - PAUSE/RESUME ")
    win.addstr(height - 1, 9, help_string)

    tmp_x = in_x
    tmp_y = in_y
    in_x, in_y, slope_x, slope_y, out, clear_prev_pixel = get_pong_coords(in_x, in_y, slope_x, slope_y)
    if clear_prev_pixel:
        win.addch(tmp_y, tmp_x, " ")
    if out:
        score -= 1
    win.addch(in_y, in_x, "*")
    win.timeout(230)
    index += 1
    key = win.getch()

    """Space will pause until another space is pressed
    """
    if key == ord(' '):
        key = -1
        mid_width = int(width / 2)
        mid_height = int((height - 1) / 2)
        print_char("PAUSE", mid_height, mid_width)
        while key != ord(' '):
            key = win.getch()
        remove_char("PAUSE", mid_height, mid_width)
        win.addch(mid_height, int((width - 1) / 2), '.')
        continue

    if key not in [KEY_UP, KEY_DOWN, 27]:
        pass

    if key == KEY_UP and not bat[0][1] == 1:
        win.addch(bat[0][1] - 1, bat[0][0], '#')
        win.addch(bat[-1][1], bat[-1][0], ' ')
        for ind in range(len(bat)):
            bat[ind][1] -= 1
    elif key == KEY_DOWN and not bat[-1][1] == height - 2:
        win.addch(bat[0][1], bat[0][0], ' ')
        win.addch(bat[-1][1] + 1, bat[-1][0], '#')
        for ind in range(len(bat)):
            bat[ind][1] += 1

curses.endwin()
print("\nScore - " + str(score))
