#!/usr/bin/env python
# -*- coding: utf-8 -*-
import book

import curses
import time
import sys
import yaml
import os
import errno

class Environment:
    def __init__(self):
        self.books = []
        self.issues = []

class Interface:
    KEY_ESC = 27
    KEY_UP = 259
    KEY_DOWN = 258
    KEY_LEFT = 260
    KEY_RIGHT = 261

    def __init__(self):
        self.environment = Environment()
        self.load()

    def save(self):
        """ Saves the user data to ~/.book_tracker/books.yaml """
        home_dir = os.path.expanduser('~')
        user_dir = os.path.join(home_dir, '.book_tracker')
        try:
            os.makedirs(user_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        user_path = os.path.join(user_dir, 'environment.yaml')

        with open(user_path, 'w') as books_file:
            yaml.dump(self.environment, books_file)

    def load(self):
        """ Loads the user data from ~/.book_tracker/books.yaml"""
        home_dir = os.path.expanduser('~')
        user_dir = os.path.join(home_dir, '.book_tracker')
        user_path = os.path.join(user_dir, 'environment.yaml')

        try:
            with open(user_path, 'r') as books_file:
                self.environment = yaml.load(books_file)
        except IOError:
            self.environment = Environment()
            pass
        except yaml.YAMLError:
            self.environment = Environment()
            pass

    def run_loop(self):
        os.environ.setdefault('ESCDELAY', '25')
        curses.wrapper(self.curses_main)

    def color_testing(self, stdscr):
        curses.init_pair(1, 255, 236)
        stdscr.bkgd(0, curses.color_pair(1))

        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, 236)
        try:
            for i in range(0, 255):
                stdscr.addstr(str(i-1), curses.color_pair(i))
        except curses.ERR:
            # End of screen reached
            pass

        stdscr.getch()
        stdscr.clear()


    def curses_main(self, stdscr):
        color_testing = False

        # setup
        curses.start_color()
        curses.cbreak()
        curses.noecho()
        stdscr.keypad(True)
        curses.curs_set(False)

        curses.start_color()
        curses.use_default_colors()

        if color_testing == True:
            self.color_testing(stdscr)

        # define and test color palette
        curses.init_pair(1, 255, 236) # white on dark grey
        curses.init_pair(2, 154, 236) # green on dark grey
        curses.init_pair(3, 196, 236) # red on dark grey
        curses.init_pair(4, 255, 202) # white on orange

        stdscr.bkgd(0, curses.color_pair(1))

        if color_testing == True:
            stdscr.addstr("normal ", curses.color_pair(1))
            stdscr.addstr("green " , curses.color_pair(2))
            stdscr.addstr("red ", curses.color_pair(3))
            stdscr.addstr("white on orange ", curses.color_pair(4))

            stdscr.getch()


        self.main_menu(stdscr)

    def main_menu(self, stdscr):
        stdscr.clear()
        current_item = 0
        stdscr.addstr(1, 1, 'Book Tracker', curses.A_BOLD | curses.color_pair(0))
        stdscr.addstr(3, 1, '▣ Select book')
        stdscr.addstr(4, 1, '□ Create book')
        while True:
            c = stdscr.getkey()
            if c == 'KEY_UP':
                current_item = (current_item-1+2) % 2
            if c == 'KEY_DOWN':
                current_item = (current_item+1+2) % 2
            if c == '\n':
                break
            if current_item == 0:
                stdscr.addstr(3, 1, '▣ Select book')
                stdscr.addstr(4, 1, '□ Create book')
            elif current_item == 1:
                stdscr.addstr(3, 1, '□ Select book')
                stdscr.addstr(4, 1, '▣ Create book')

        if current_item == 0:
            self.book_selection(stdscr)
        elif current_item == 1:
            self.book_creation(stdscr)

    def book_creation(self, stdscr):
        curses.echo()

        stdscr.clear()
        current_item = 0

        stdscr.addstr(1, 1, 'Book Tracker', curses.A_BOLD)

        c = ' '
        while True:
            if c == 'KEY_UP':
                current_item = (current_item-1+6) % 6
            if c == 'KEY_DOWN':
                current_item = (current_item+1+6) % 6
            if current_item == 0:
                stdscr.addstr(3, 1, '▣ Title: ')
                stdscr.addstr(4, 1, '□ Author: ')
                stdscr.addstr(5, 1, '□ Year: ')
                stdscr.addstr(6, 1, '□ Pages: ')
                stdscr.addstr(7, 1, '□ Add')
                stdscr.addstr(8, 1, '□ Cancel')
                stdscr.move(3, 12)

                curses.curs_set(True)
                c = stdscr.getkey()
                cursor_pos = stdscr.getyx()
                while c != 'KEY_UP' and c != 'KEY_DOWN' and c != '\n' and cursor_pos[1] < 60:
                    c = stdscr.getkey()
                    cursor_pos = stdscr.getyx()
                curses.curs_set(False)
            elif current_item == 1:
                stdscr.addstr(3, 1, '□ Title: ')
                stdscr.addstr(4, 1, '▣ Author: ')
                stdscr.addstr(5, 1, '□ Year: ')
                stdscr.addstr(6, 1, '□ Pages: ')
                stdscr.addstr(7, 1, '□ Add')
                stdscr.addstr(8, 1, '□ Cancel')
                stdscr.move(4, 12)

                curses.curs_set(True)
                c = stdscr.getkey()
                cursor_pos = stdscr.getyx()
                while c != 'KEY_UP' and c != 'KEY_DOWN' and c != '\n' and cursor_pos[1] < 60:
                    c = stdscr.getkey()
                    cursor_pos = stdscr.getyx()
                curses.curs_set(False)
            elif current_item == 2:
                stdscr.addstr(3, 1, '□ Title: ')
                stdscr.addstr(4, 1, '□ Author: ')
                stdscr.addstr(5, 1, '▣ Year: ')
                stdscr.addstr(6, 1, '□ Pages: ')
                stdscr.addstr(7, 1, '□ Add')
                stdscr.addstr(8, 1, '□ Cancel')

                curses.curs_set(True)
                stdscr.move(5, 12)
                c = stdscr.getkey()
                cursor_pos = stdscr.getyx()
                while c != 'KEY_UP' and c != 'KEY_DOWN' and c != '\n' and cursor_pos[1] < 16:
                    c = stdscr.getkey()
                    cursor_pos = stdscr.getyx()
                curses.curs_set(False)
            elif current_item == 3:
                stdscr.addstr(3, 1, '□ Title: ')
                stdscr.addstr(4, 1, '□ Author: ')
                stdscr.addstr(5, 1, '□ Year: ')
                stdscr.addstr(6, 1, '▣ Pages: ')
                stdscr.addstr(7, 1, '□ Add')
                stdscr.addstr(8, 1, '□ Cancel')

                curses.curs_set(True)
                stdscr.move(6, 12)
                c = stdscr.getkey()
                cursor_pos = stdscr.getyx()
                while c != 'KEY_UP' and c != 'KEY_DOWN' and c != '\n' and cursor_pos[1] < 16:
                    c = stdscr.getkey()
                    cursor_pos = stdscr.getyx()
                curses.curs_set(False)
            elif current_item == 4:
                stdscr.addstr(3, 1, '□ Title: ')
                stdscr.addstr(4, 1, '□ Author: ')
                stdscr.addstr(5, 1, '□ Year: ')
                stdscr.addstr(6, 1, '□ Pages: ')
                stdscr.addstr(7, 1, '▣ Add')
                stdscr.addstr(8, 1, '□ Cancel')
                c = stdscr.getkey()
                if c == '\n':
                    name = stdscr.instr(3, 12, 48).decode('UTF-8').rstrip()
                    author = stdscr.instr(4, 12, 48).decode('UTF-8').rstrip()
                    year = stdscr.instr(5, 12, 4).decode('UTF-8').rstrip()
                    pages = stdscr.instr(6, 12, 4).decode('UTF-8').rstrip()
                    if book.valid_book_definition(name, author, year, pages):
                        self.environment.books.append(book.Book(name, author, int(year), int(pages)))
                        self.save()
                        break
            elif current_item == 5:
                stdscr.addstr(3, 1, '□ Title: ')
                stdscr.addstr(4, 1, '□ Author: ')
                stdscr.addstr(5, 1, '□ Year: ')
                stdscr.addstr(6, 1, '□ Pages: ')
                stdscr.addstr(7, 1, '□ Add')
                stdscr.addstr(8, 1, '▣ Cancel')
                c = stdscr.getkey()
                if c == '\n':
                    break

        self.main_menu(stdscr)

    def book_selection(self, stdscr):
        """ Shows the book selection menu"""
        curses.curs_set(False)

        current_item = 0
        while True:
            stdscr.clear()
            stdscr.addstr(1, 1, 'Book Tracker', curses.A_BOLD)
            row = 0
            c = ' '
            # shift is there so more books so you can scroll the list if there are more books than terminal lines
            shift = min(current_item - curses.LINES + 5, len(self.environment.books) - curses.LINES + 3)
            for book_count, book in enumerate(self.environment.books):
                if shift > 0:
                    shift = shift - 1
                    continue

                if 3+row >= curses.LINES:
                    continue

                if current_item == book_count:
                    stdscr.addstr(3+row, 1, '▣ {title}'.format(title=book.name))
                else:
                    stdscr.addstr(3+row, 1, '□ {title}'.format(title=book.name))
                row = row+1

            # key handling
            c = stdscr.getkey()

            if c == 'KEY_RIGHT' or c == '\n':
                self.book_reading(stdscr, self.environment.books[current_item])
            if c == 'KEY_UP':
                current_item = (current_item - 1 + len(self.environment.books)) % len(self.environment.books)
            if c == 'KEY_DOWN':
                current_item = (current_item + 1 + len(self.environment.books)) % len(self.environment.books)
            if c == 'KEY_LEFT':
                break

        self.main_menu(stdscr)

    def book_reading(self, stdscr, book):
        """ Shows the books page overview """

        current_page = 0
        first_row = 0
        curses.curs_set(True)

        while(True):
            stdscr.clear()
            size = stdscr.getmaxyx()
            max_pages_per_line = 50
            rows = size[0]
            cols = min(size[1], max_pages_per_line+7)


            stdscr.addstr(1, 1, 'Book Tracker ({rows}x{cols})'.format(rows=rows, cols=cols), curses.A_BOLD)
            stdscr.addstr(rows-1, 0, '(🠉🠋🠈🠊) Move Cursor    (r) Mark as read    (i) Create issue    (Esc) Close book'.ljust(size[1]-1), curses.color_pair(4) | curses.A_BOLD)

            rows_available = rows - 5
            rows_needed = (len(book.pages)-1) // (cols-7) + 1
            current_row = current_page // (cols - 7)

            if current_page // (cols - 7) - first_row >= rows_available-1:
                first_row = first_row + 1
            if current_page // (cols - 7) - first_row <= 0:
                first_row = first_row - 1

            if first_row < 0:
                first_row = 0
            if first_row >= rows_needed - rows_available:
                first_row = rows_needed - rows_available

            for number, pagestate in enumerate(book.pages):
                shift = 0
                row = number // (cols - 7)
                if row < first_row:
                    continue

                row = row - first_row

                if row >= rows_available:
                    continue

                if number % (cols - 7) == 0:
                    stdscr.addstr(row + 3, 1, str(number + 1).rjust(4))

                # different color depending on page state
                if pagestate == -1:
                    stdscr.addstr(row + 3, number % (cols - 7) + 6, '|', curses.color_pair(1))
                elif pagestate == -2:
                    stdscr.addstr(row + 3, number % (cols - 7) + 6, '|', curses.color_pair(2))
                else:
                    stdscr.addstr(row + 3, number % (cols - 7) + 6, '|', curses.color_pair(3))

            stdscr.move(current_page // (cols - 7) + 3 - first_row, current_page % (cols - 7) + 6)

            # key handling
            c = stdscr.getch()
            if c == Interface.KEY_RIGHT or c == '\n':
                current_page = current_page + 1
                if current_page >= len(book.pages):
                    current_page = len(book.pages) - 1
            if c == Interface.KEY_UP:
                current_page = current_page - (cols - 7)
                if current_page < 0:
                    current_page = current_page + (cols - 7)
            if c == Interface.KEY_DOWN:
                current_page = current_page + (cols - 7)
                if current_page >= len(book.pages):
                    current_page = current_page - (cols - 7)
            if c == Interface.KEY_LEFT:
                current_page = current_page - 1
                if current_page < 0:
                    current_page = 0
            if c == Interface.KEY_ESC:
                break

        self.book_selection(stdscr)
