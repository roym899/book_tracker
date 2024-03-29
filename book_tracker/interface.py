#!/usr/bin/env python
# -*- coding: utf-8 -*-
import book
import issue

import curses
import time
import sys
import yaml
import os
import errno
import time
import datetime

import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)


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
    KEY_SHIFT_UP = 337
    KEY_SHIFT_DOWN = 336
    KEY_SHIFT_LEFT = 393
    KEY_SHIFT_RIGHT = 402
    KEY_R = 114
    KEY_SHIFT_R =82
    KEY_I = 105
    KEY_RESIZE = 410
    KEY_BACKSPACE = 263
    KEY_CTRL_X = 24
    KEY_CTRL_D = 4
    KEY_CTRL_LEFT = 68
    KEY_CTRL_RIGHT = 67
    KEY_ENTER = 10
    KEY_F1 = 265
    KEY_F2 = 266
    KEY_F3 = 267
    KEY_CTRL_L = 12



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
        stdscr.erase()


    def curses_main(self, stdscr):
        color_testing = True

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
        curses.init_pair(2, 46, 236) # green on dark grey
        curses.init_pair(3, 196, 236) # red on dark grey
        curses.init_pair(4, 255, 202) # white on orange
        curses.init_pair(5, 255, 239) # white on light grey
        curses.init_pair(6, 255, 202) # white on orange
        curses.init_pair(7, 46, 202) # green on orange
        curses.init_pair(8, 196, 202) # red on orange

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
                        self.environment.books.append(book.Book(name, author, int(year), int(pages), self.environment.books))
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
        stdscr.clear()

        current_item = 0
        while True:
            stdscr.erase()
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
                    stdscr.addstr(3+row, 1, '▣ {title}'.format(title=book.title))
                else:
                    stdscr.addstr(3+row, 1, '□ {title}'.format(title=book.title))
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

    def book_reading(self, stdscr, current_book):
        """ Shows the books page overview """

        current_page = 0
        first_row = 0
        curses.curs_set(True)
        stdscr.clear()

        current_pages_start = None

        while True:
            size = stdscr.getmaxyx()
            max_pages_per_line = 50
            rows = size[0]
            cols = min(size[1], max_pages_per_line+7)

            stdscr.addstr(1, 1, 'Book Tracker ({rows}x{cols}), ({start}-{end})'.format(rows=rows, cols=cols, start=current_pages_start, end=current_page), curses.A_BOLD)

            if current_pages_start is None:
                pagestring = '(@{book_id}:{current_page})'.format(book_id=current_book.identifier,
                                                                  current_page=current_page + 1)
            else:
                pagestring = '(@{book_id}:{current_page_start}-{current_page_end})' \
                    .format(book_id=current_book.identifier,
                            current_page_start=min([current_pages_start, current_page])+1,
                            current_page_end=max([current_pages_start, current_page])+1)

            stdscr.addnstr(rows-1, 0,
                           '(🠉🠋🠈🠊) Move Cursor  (r/R) Mark as read/unread (i) Create/Open issue  (Esc) Close book'
                           .ljust(size[1]-1-len(pagestring))+pagestring,
                           size[1]-1,
                           curses.color_pair(4) | curses.A_BOLD)

            rows_available = rows - 5
            rows_needed = (len(current_book.pages)-1) // (cols-7) + 1

            if current_page // (cols - 7) - first_row >= rows_available-1:
                first_row = first_row + 1
            if current_page // (cols - 7) - first_row <= 0:
                first_row = first_row - 1

            if first_row < 0:
                first_row = 0
            if first_row >= rows_needed - rows_available:
                first_row = rows_needed - rows_available

            for number, pagestate in enumerate(current_book.pages):
                row = number // (cols - 7)
                if row < first_row:
                    continue

                row = row - first_row

                if row >= rows_available:
                    continue

                if number % (cols - 7) == 0:
                    stdscr.addstr(row + 3, 1, str(number + 1).rjust(4))

                # different color depending on page state
                if pagestate == book.Book.UNREAD:
                    if current_pages_start is not None and \
                                    abs(current_page - current_pages_start) >= abs(current_page - number) and \
                                    abs(current_page - current_pages_start) >= abs(current_pages_start - number):
                        stdscr.addstr(row + 3, number % (cols - 7) + 6, '▮', curses.color_pair(6) | curses.A_BOLD)
                    else:
                        stdscr.addstr(row + 3, number % (cols - 7) + 6, '▮', curses.color_pair(1) | curses.A_BOLD)
                elif pagestate == book.Book.READ:
                    if current_pages_start is not None and \
                                    abs(current_page - current_pages_start) >= abs(current_page - number) and \
                                    abs(current_page - current_pages_start) >= abs(current_pages_start - number):
                        stdscr.addstr(row + 3, number % (cols - 7) + 6, '▮', curses.color_pair(7) | curses.A_BOLD)
                    else:
                        stdscr.addstr(row + 3, number % (cols - 7) + 6, '▮', curses.color_pair(2) | curses.A_BOLD)
                else:
                    if current_pages_start is not None and \
                                    abs(current_page - current_pages_start) >= abs(current_page - number) and \
                                    abs(current_page - current_pages_start) >= abs(current_pages_start - number):
                        stdscr.addstr(row + 3, number % (cols - 7) + 6, '▮', curses.color_pair(8) | curses.A_BOLD)
                    else:
                        stdscr.addstr(row + 3, number % (cols - 7) + 6, '▮', curses.color_pair(3) | curses.A_BOLD)

            stdscr.move(current_page // (cols - 7) + 3 - first_row, current_page % (cols - 7) + 6)

            # key handling
            c = stdscr.getch()
            if c == Interface.KEY_RIGHT or c == '\n':
                current_page = current_page + 1
                if current_page >= len(current_book.pages):
                    current_page = len(current_book.pages) - 1
                current_pages_start = None
                current_pages_end = None
            elif c == Interface.KEY_UP:
                current_page = current_page - (cols - 7)
                if current_page < 0:
                    current_page = current_page + (cols - 7)
                current_pages_start = None
                current_pages_end = None
            elif c == Interface.KEY_DOWN:
                current_page = current_page + (cols - 7)
                if current_page >= len(current_book.pages):
                    current_page = current_page - (cols - 7)
                current_pages_start = None
                current_pages_end = None
            elif c == Interface.KEY_LEFT:
                current_page = current_page - 1
                if current_page < 0:
                    current_page = 0
                current_pages_start = None
                current_pages_end = None
            elif c == Interface.KEY_SHIFT_LEFT:
                if current_pages_start is None:
                    current_pages_start = current_page

                current_page = current_page - 1
                if current_page < 0:
                    current_page = 0

                if current_pages_start == current_page:
                    current_pages_start = None

            elif c == Interface.KEY_SHIFT_RIGHT:
                if current_pages_start is None:
                    current_pages_start = current_page

                current_page = current_page + 1
                if current_page >= len(current_book.pages):
                    current_page = len(current_book.pages) - 1

                if current_pages_start == current_page:
                    current_pages_start = None

            elif c == Interface.KEY_ESC:
                break
            elif c == Interface.KEY_R:
                if current_pages_start is None:
                    current_pages = [current_page]
                else:
                    current_pages = list(range(min(current_page, current_pages_start),
                                               max(current_page, current_pages_start) + 1))

                for cp in current_pages:
                    if current_book.pages[cp] == book.Book.READ:
                        current_book.pages[cp] = book.Book.UNREAD
                    elif current_book.pages[cp] == book.Book.UNREAD:
                        current_book.pages[cp] = book.Book.READ
                self.save()
                current_page = current_page + 1
                if current_page >= len(current_book.pages):
                    current_page = len(current_book.pages) - 1
            elif c == Interface.KEY_SHIFT_R:
                if current_pages_start is None:
                    current_pages = [current_page]
                else:
                    current_pages = list(range(min(current_page, current_pages_start),
                                               max(current_page, current_pages_start) + 1))

                for cp in current_pages:
                    if current_book.pages[cp] == book.Book.READ:
                        current_book.pages[cp] = book.Book.UNREAD
                    else:
                        current_book.pages[cp] = book.Book.READ

                self.save()
                current_page = current_page + 1
                if current_page >= len(current_book.pages):
                    current_page = len(current_book.pages) - 1
            elif c == Interface.KEY_I:
                if current_pages_start is None:
                    issue = self.issue_editor(stdscr, current_book, [current_page])
                else:
                    issue = self.issue_editor(stdscr, current_book,
                                              list(range(min(current_page,current_pages_start),
                                                         max(current_page, current_pages_start)+1)))
                curses.curs_set(True)
            elif c == Interface.KEY_RESIZE:
                stdscr.erase()
                pass
            else:
                stdscr.addstr(1, 1, 'Book Tracker ({rows}x{cols}, {c})'.format(rows=rows, cols=cols, c=c),
                              curses.A_BOLD)
                stdscr.getch()

        self.book_selection(stdscr)

    def issue_editor(self, stdscr, current_book=None, current_pages=None):
        """ current_pages is a list of pages or None if the issue editor has not been opened from a specific page"""
        left_margin = 1
        right_margin = 1
        top_margin = 2
        bottom_margin = 2
        date_width = 11
        size = stdscr.getmaxyx()
        stdscr.keypad(True)
        stdscr.clear()
        curses.noecho()

        if current_book is not None and current_book.pages[current_pages[0]] >= 0:
            current_issue_id = current_book.pages[current_pages[0]]
            current_issue = self.environment.issues[current_issue_id]
        else:
            current_issue = issue.Issue()
            current_issue_id = len(self.environment.issues)

        current_text = ""
        current_cursor_position = 0

        c = 0

        while True:
            stdscr.erase()

            current_row = top_margin

            stdscr.addstr(0, 0, 'Issue #{issue} ({char})'
                          .format(issue=current_issue_id,
                                  char=c),
                          curses.A_BOLD)

            if current_book is not None:
                if len(current_pages) == 1:
                    pagestring = '(@{book_id}:{current_page})'.format(book_id=current_book.identifier,
                                                                      current_page=current_pages[0]+1)
                else:
                    pagestring = '(@{book_id}:{current_page_start}-{current_page_end})'\
                        .format(book_id=current_book.identifier,
                                current_page_start=current_pages[0]+1,
                                current_page_end=current_pages[-1]+1)
                stdscr.addnstr(size[0]-1, 0, '(🠉🠋🠈🠊) Scroll/Move Cursor  (F1 F2) Select Issue'
                                             '  (^L) Close and Exit  (^D) Save and Exit  (^X) Discard and Exit'
                               .ljust(size[1]-1-len(pagestring))+pagestring,
                               size[1]-1,
                               curses.color_pair(4) | curses.A_BOLD)

            # add all the previous comments if there are any for the selected issue
            for comment in current_issue.comments:
                # the creation date
                stdscr.addstr(current_row, left_margin, utc_to_local(comment.created).strftime("%Y-%m-%d"))
                stdscr.addstr(current_row+1, left_margin, utc_to_local(comment.created).strftime("%H:%M"))
                # the actual comment
                row = current_row
                col = left_margin+date_width
                for index, c in enumerate(comment.text):
                    stdscr.addstr(row, col, c)

                    current_row = row + 2

                    col = col + 1
                    if col >= size[1] - right_margin - 1:
                        col = left_margin+date_width
                        row = row + 1

            if current_issue.is_closed():
                curses.curs_set(False)
                stdscr.addstr(current_row, left_margin, utc_to_local(current_issue.closed).strftime("%Y-%m-%d"))
                stdscr.addstr(current_row+1, left_margin, utc_to_local(current_issue.closed).strftime("%H:%M"))
                stdscr.addstr(current_row, left_margin+date_width, "Issue closed.")
            else:
                curses.curs_set(True)
                # add the current comment element
                # first the date and time
                utcnow = datetime.datetime.utcnow()
                stdscr.addstr(current_row, left_margin, utc_to_local(utcnow).strftime("%Y-%m-%d"))
                stdscr.addstr(current_row+1, left_margin, utc_to_local(utcnow).strftime("%H:%M"))
                # second the current text
                row = current_row
                col = left_margin+date_width
                cursor_row = 0
                cursor_col = 0
                for index, c in enumerate(current_text):
                    stdscr.addstr(row, col, c)

                    if index == current_cursor_position:
                        cursor_row = row
                        cursor_col = col

                    col = col + 1
                    if col >= size[1] - right_margin - 1:
                        col = left_margin+date_width
                        row = row + 1
                # set the right cursor position
                if current_cursor_position < len(current_text):
                    stdscr.move(cursor_row, cursor_col)
                else:
                    stdscr.move(row, col)

            c = stdscr.getch()
            if c == Interface.KEY_RESIZE:
                size = stdscr.getmaxyx()
            elif c == Interface.KEY_BACKSPACE:
                if current_cursor_position > 0:
                    current_text = current_text[:current_cursor_position-1]+current_text[current_cursor_position:]
                    current_cursor_position = current_cursor_position - 1
            elif c == Interface.KEY_UP:
                pass
            elif c == Interface.KEY_DOWN:
                pass
            elif c == Interface.KEY_LEFT:
                current_cursor_position = current_cursor_position - 1
                if current_cursor_position < 0:
                    current_cursor_position = 0
            elif c == Interface.KEY_RIGHT:
                current_cursor_position = current_cursor_position + 1
                if current_cursor_position > len(current_text):
                    current_cursor_position = len(current_text)
            elif c == Interface.KEY_CTRL_X:
                stdscr.clear()
                return None
            elif c == Interface.KEY_CTRL_D:
                if len(current_text) > 10:
                    current_issue.add_comment(current_text)
                    if current_issue_id == len(self.environment.issues):
                        self.environment.issues.append(current_issue)
                    if current_book is not None:
                        for current_page in current_pages:
                            current_book.pages[current_page] = current_issue_id
                    self.save()
                    stdscr.clear()
                    return current_issue
            elif c == Interface.KEY_F2:
                current_issue_id = current_issue_id - 1
                if current_issue_id < 0:
                    current_issue_id = 0
                if current_issue_id >= len(self.environment.issues):
                    current_issue_id = len(self.environment.issues)
                    current_issue = issue.Issue()
                else:
                    current_issue = self.environment.issues[current_issue_id]
            elif c == Interface.KEY_F3:
                current_issue_id = current_issue_id + 1
                if current_issue_id >= len(self.environment.issues):
                    current_issue_id = len(self.environment.issues)
                    current_issue = issue.Issue()
                else:
                    current_issue = self.environment.issues[current_issue_id]
            elif c == Interface.KEY_ENTER:
                pass
            elif c == Interface.KEY_CTRL_L:
                if current_issue_id != len(self.environment.issues):
                    current_issue.closed = utcnow
                    for b in self.environment.books:
                        for i, p in enumerate(b.pages):
                            if p == current_issue_id:
                                b.pages[i] = book.Book.READ
                    self.save()
                    stdscr.clear()
                    return None

            else:
                current_text = current_text[:current_cursor_position]+chr(c)+current_text[current_cursor_position:]
                current_cursor_position = current_cursor_position + 1
