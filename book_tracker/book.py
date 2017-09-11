#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def generate_unique_identifier(title, year, books):
    simplified_title = re.sub('[^a-zA-Z]', ' ', title)
    title_abbreviation = "".join(word[0].lower() for word in simplified_title.split())
    year = year % 100
    prefix = "{title_abbreviation}{year}".format(title_abbreviation=title_abbreviation, year=year)
    reps = len([book for book in books if prefix in book.identifier])
    identifier = ''
    if reps > 0:
        identifier = chr(ord('a') + reps - 1)
    return "{prefix}{identifier}".format(prefix=prefix,
                                         identifier=identifier)

class Book:
    UNREAD = -1
    READ = -2

    """Representation of a book"""
    def __init__(self, title, author, year, pages, books):
        """ needs a lit of books to generate a unique identifier """
        self.title = title
        self.author = author
        self.year = year
        self.pages = [Book.UNREAD for i in range(pages)]
        self.identifier = generate_unique_identifier(title, year, books)


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