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

while key != 27:
    win.border(0)
    title_string = " Score: {:04d} {:>19} {:<23}".format(score%10000, "SOLO PONG", " ")
    win.addstr(0, 2, title_string)
    help_string = "{} {}".format(" Controls: UP DOWN ───", "SPACE - PAUSE/RESUME ")
    win.addstr(height - 1, 9, help_string)
    # win.timeout(1)

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
