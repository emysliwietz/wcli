#!/bin/python3

"""Curses frontend."""

import time
import urllib.request
import traceback
import csv
import os
import glob
import sys
import curses
from inspect import getmembers, isfunction
from net.client import init_client, send_data, close_client


curr_view = "chat"

prompt = ""
c_prompt = ""
last_completion_num = -1
prompt_history = []
stdscr = None
screen = None
out_win = None


def p(s):
    """Print to cli screen."""
    global screen
    (y, _) = screen.getyx()
    screen.move(y, 0)
    screen.clrtoeol()
    screen.addstr(str(s))
    screen.refresh()


def t(s):
    """Print as title."""
    global stdscr
    stdscr.move(0, 0)
    stdscr.clrtoeol()
    stdscr.addstr(str(s))
    stdscr.refresh()


def o(s, append=True):
    """Print to output screen."""
    global out_win, curr_view
    (y, _) = out_win.getyx() if append else (0, 0)
    if y == curses.LINES - 3:
        out_win.clear()
        y = 0
    try:
        out_win.move(y + 1, 1)
        out_win.clrtoeol()
        out_win.addstr(str(s))
        out_win.box()
        v(curr_view)
    except:
        pass


def v(s):
    """Print current view as title of output screen."""
    global out_win, curr_view
    curr_view = str(s)
    (y, x) = out_win.getyx()
    out_win.move(0, int(curses.COLS / 4) - int(len(curr_view) / 2))
    out_win.box()
    out_win.addstr(curr_view)
    out_win.move(y, x)
    out_win.refresh()


def clear_screen():
    """Clear the output screen."""
    global out_win
    out_win.clear()
    out_win.refresh()
    v(curr_view)


def clear_o(s):
    """Print to output screen after clearing it."""
    global out_win
    out_win.clear()
    try:
        o(s, append=False)
    except:
        o("RIP", append=False)


def complete():
    """Autocomplete currently typed word."""
    global c_prompt, prompt, last_completion_num
    af = all_functions()
    for (i, f) in enumerate(af):
        if f.startswith(c_prompt) and not prompt == f and i > last_completion_num:
            prompt = f
            # o(getattr(lib, f).__doc__)
            last_completion_num = i
            p("> " + prompt)
            return
    for (i, f) in enumerate(af):
        if f.startswith(c_prompt) and not prompt == f:
            prompt = f
            last_completion_num = i
            p("> " + prompt)
            return


hist_num = 1


def up_history():
    """Set prompt to older command."""
    global hist_num
    try:
        prompt = prompt_history[-hist_num]
        hist_num += 1
        p("> " + prompt)
    except:
        pass


def down_history():
    """Set prompt to newer command."""
    global hist_num
    try:
        prompt = prompt_history[(-hist_num) + 1]
        hist_num -= 1
        p("> " + prompt)
    except:
        pass


def handle_special_prompt(c):
    """Handle prompts that are not lib commands."""
    if c == "quit":
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()
        os._exit(1)
    elif c == "help":
        s = ""
        for f in all_functions():
            s += f + " "
        o(s)
        return True
    elif c == "clear":
        clear_o("")
        return True
    return False


def send_command(cmd):
    """Send command to server."""
    return send_data(cmd)


def handle_cmd_output(resp):
    """Handle output of response from server."""
    o(resp)


def exec_shell_prompt():
    """Parse and execute a shell prompt."""
    global prompt, prompt_history
    if prompt.isspace() or prompt == "":
        p("> ")
        return
    old_p = prompt
    prompt = ""
    prompt_history += [
        old_p,
    ]
    if not handle_special_prompt(old_p):
        handle_cmd_output(send_command(old_p))


def handle_char(char):
    """Handle the typing of alnum chars."""
    global prompt, c_prompt, hist_num
    hist_num = 1
    prompt = prompt + char
    c_prompt = prompt
    last_completion_num = -1
    p("> " + prompt)


def resize():
    """Handle resize event of terminal window."""
    curses.update_lines_cols()
    screen.resize(curses.LINES - 1, int(curses.COLS / 2))
    out_win.resize(curses.LINES - 1, int(curses.COLS / 2))
    out_win.mvwin(1, int(curses.COLS / 2))
    out_win.clear()
    out_win.box()
    out_win.refresh()
    screen.refresh()


def handle(key):
    """Handle keypresses."""
    global prompt, c_prompt
    if key == 127:  # BACKSPACE
        prompt = prompt[0:-1]
        c_prompt = prompt
        last_completion_num = -1
        p("> " + prompt)
    elif key == 9:  # TAB
        complete()
    elif key == 10:  # ENTER
        (y, _) = screen.getyx()
        c_prompt = ""
        try:
            screen.move(y + 1, 0)
        except:
            screen.move(0, 0)
            screen.deleteln()
            screen.move(y, 0)
        exec_shell_prompt()
        p("> ")
    elif key == 188:  # ü
        handle_char("")
    elif key == 164:  # ä
        handle_char("")
    elif key == 182:  # ö
        handle_char("")
    elif key == 159:  # ß
        handle_char("")
    elif key == 156:  # Ü
        handle_char("")
    elif key == 132:  # ä
        handle_char("")
    elif key == 150:  # Ö
        handle_char("")
    elif key == 45:  # -
        handle_char("-")
    elif key == 16:  # up
        up_history()
    elif key == 14:  # down
        down_history()
    elif key == 65:  # C-p
        old_prompt = prompt
        prompt = "go_up"
        exec_shell_prompt()
        prompt = old_prompt
    elif key == 66:  # C-n
        old_prompt = prompt
        prompt = "go_down"
        exec_shell_prompt()
        prompt = old_prompt
    elif key == 95:  # _
        handle_char("_")
    elif key == 32:  # _
        handle_char(" ")
    elif key == curses.KEY_RESIZE:
        resize()
    elif key == 12:  # clear_screen
        clear_screen()
    elif chr(key).isalnum():
        handle_char(chr(key))


def main(host, port):
    global stdscr, screen, out_win
    stdscr = curses.initscr()
    screen = curses.newwin(curses.LINES - 1, int(curses.COLS / 2), 1, 0)
    out_win = curses.newwin(
        curses.LINES - 1, int(curses.COLS / 2), 1, int(curses.COLS / 2)
    )
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    resize()
    init_client(host, port)
    p("> ")
    while True:
        a = stdscr.getch()
        t("WhatsApp Web CLI - {}\n".format(a))
        handle(a)
