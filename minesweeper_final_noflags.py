########################
## Minesweeper Solver ##
### Created by Jadon ###
########################

# Setup: Google Minesweeper, Easy Mode

# Libraries
import win32api as wa
import win32gui as wg
import pyautogui as pg
import keyboard
import time


# Board Data Setup
data = []
for y in range(8): data.append(['?' for x in range(10)])

def clear_data():
    data = []
    for y in range(8): data.append(['?' for x in range(10)])

def print_board():
    for i in data:
        print(i)

# Returns the Value of an Individual Box
def find(x, y):
    color = wg.GetPixel(wg.GetDC(wg.GetActiveWindow()), x, y)
    if color == 13792793: return '1'  # Blue, 1
    if color == 3968568: return '2'  # Dark Green, 2
    if color == 3092435: return '3'  # Red, 3
    if color == 10624891: return '4'  # Does not work due to location, 4
    if color == 5363626 or color == 4837794: return "?"  # Light and Medium Greens, ?
    if color == 10470117 or color == 10074327: return " "  # Light Browns, -
    else: print("Error!"); return "E"  # Other, E


# Updates the Data List from the Minesweeper Website
def update(move_cursor=False):
    y_pos = 232
    for y in range(8):
        x_pos = 31
        for x in range(10):
            if data[y][x] != "!": data[y][x] = find(round(x_pos), round(y_pos))
            if move_cursor: wa.SetCursorPos((round(x_pos), round(y_pos)))
            x_pos += 56.3
        y_pos += 56.3


# Begins Game
def start(corner=False):
    if corner:
        wa.SetCursorPos((1, 205))
        pg.hotkey('alt','tab')
        pg.hotkey('ctrl','r')
        pg.leftClick()
    else:
        wa.SetCursorPos((283, 430))
        pg.hotkey('alt','tab')
        pg.hotkey('ctrl','r')
        pg.leftClick()


# Converts time.sleep to a wait Function
def wait(s): time.sleep(s)

# Moves the Mouse to a Tile
def move(y, x): wa.SetCursorPos((31 + round(56.3*x), 232 + round(56.3*y)))


# Check for Possible Mines
def check_mines():
    for y in range(len(data)):
        for x in range(len(data[0])):
            unknown = 0
            try: n = int(data[y][x])
            except: continue
            if n >= 1 and n <= 8:
                for a in [-1, 0, 1]:
                    for b in [-1, 0, 1]:
                        if y+a >= 0 and y+a < 8 and x+b >= 0 and x+b < 10:
                            if data[y+a][x+b] == "?" or data[y+a][x+b] == "!":
                                unknown += 1
            if unknown == n:
                for a in [-1, 0, 1]:
                    for b in [-1, 0, 1]:
                        if y+a >= 0 and y+a < 8 and x+b >= 0 and x+b < 10:
                            if data[y+a][x+b] == "?" and data[y+a][x+b] != "!":
                                data[y+a][x+b] = "!"


# Clear Safe Tiles
def check_safe():
    for y in range(len(data)):
        for x in range(len(data[0])):
            flagged = 0
            try: n = int(data[y][x])
            except: continue
            if n >= 1 and n <= 8:
                for a in [-1, 0, 1]:
                    for b in [-1, 0, 1]:
                        if y+a >= 0 and y+a < 8 and x+b >= 0 and x+b < 10:
                            if data[y+a][x+b] == "!":
                                flagged += 1
            if flagged == n:
                for a in [-1, 0, 1]:
                    for b in [-1, 0, 1]:
                        if y+a >= 0 and y+a < 8 and x+b >= 0 and x+b < 10:
                            if data[y+a][x+b] == "?" and data[y+a][x+b] != "!":
                                data[y+a][x+b] = "?"
                                move(y+a, x+b)
                                pg.leftClick()


# Checks Total Mines Found
def discovered():
    mines = 0
    for i in data:
        for j in i:
            if j == "!": mines += 1
    return mines


# Removes Tiles when All Mines are Found
def finish():
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == "?": move(i, j); pg.leftClick()


# Main Script
clear_data()
start()
wait(1)
update(False)
print_board()
while discovered() < 10:
    check_mines()
    check_safe()
    update(False)
finish()
exit()