#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime


class Issue:
    """ Representation of an issue which can refer to multiple (or maybe even no book) """
    def __init__(self):
        # timestamp is stored in utc and displayed in local timezone
        self.comments = []
        self.closed = None

    def add_comment(self, text, book=None, page=None):
        self.comments.append(Comment(text))


class Comment:
    def __init__(self, text, book=None, page=None):
        self.created = datetime.datetime.utcnow()
        self.text = text

    def set_time_to_now(self):
        self.created = datetime.datetime.utcnow()