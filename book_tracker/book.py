#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Book:
    """Representation of a book"""
    def __init__(self, name, author, year, pages):
        self.name = name
        self.author = author
        self.year = year
        self.pages = pages


def valid_book_definition(name, author, year, pages):
    """Does some simple checks on whether the provided arguments are sufficient to defien a book"""
    if len(name) <= 1:
        return False

    if len(author) <= 1:
        return False

    try:
        int(pages)
        int(year)
    except ValueError:
        return False

    return True