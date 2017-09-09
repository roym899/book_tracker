#!/usr/bin/env python
# -*- coding: utf-8 -*-
import book

import curses
import time
import sys
import yaml
import os
import errno

class Interface:
    def __init__(self):
        self.books = []
        self.load()

    def save(self):
        """ Saves the user data to ~/.book_tracker/pydo.yaml """
        home_dir = os.path.expanduser('~')
        user_dir = os.path.join(home_dir, '.book_tracker')
        try:
            os.makedirs(user_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        user_path = os.path.join(user_dir, 'pydo.yaml')

        with open(user_path, 'w') as books_file:
            yaml.dump(self.books, books_file)

    def load(self):
        """ Loads the user data from ~/.book_tracker/pydo.yaml"""
        home_dir = os.path.expanduser('~')
        user_dir = os.path.join(home_dir, '.book_tracker')
        user_path = os.path.join(user_dir, 'pydo.yaml')

        try:
            with open(user_path, 'r') as books_file:
                self.books = yaml.load(books_file)
        except IOError:
            self.books = []
            pass
        except yaml.YAMLError:
            self.books = []
            pass

    def run_loop(self):
        curses.wrapper(self.curses_main)

    def curses_main(self, stdscr):
        # setup
        curses.start_color()
        curses.use_default_colors()
        curses.cbreak()
        curses.noecho()
        stdscr.keypad(True)
        curses.curs_set(False)

        self.main_menu(stdscr)

    def main_menu(self, stdscr):
        stdscr.clear()
        current_item = 0
        stdscr.addstr(1, 1, 'Book Tracker', curses.A_BOLD)
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

    def book_selection(self, stdscr):
        stdscr.clear()
        stdscr.addstr(1, 1, 'Book Tracker', curses.A_BOLD)

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
                        self.books.append(book.Book(name, author, int(year), int(pages)))
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