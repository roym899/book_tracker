#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import sys

import interface


def main():
    user_interface = interface.Interface()
    user_interface.run_loop()

if __name__ == "__main__":
    # execute only if run as a script
    main()