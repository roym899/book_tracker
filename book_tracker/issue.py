#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

class Issue:
    """ Representation of an issue which can refer to multiple (or maybe even no book) """
    def __init__(self, text):
        # timestamp is stored in utc and displayed in local timezone
        self.created = datetime.datetime.utcnow()
        self.comments = [self.Comment(text)]
        self.closed = None

    class Comment:
        def __init__(self, text):
            self.created = datetime.datetime.utcnow()
            self.text = text