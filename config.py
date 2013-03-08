# -*- coding: utf8
from __future__ import division, print_function
'''Configuration constants are kept here'''

import os

import web

SELF_DIR = os.path.dirname(os.path.realpath(__file__))
relative_fpath_opt = lambda fpath: os.path.join(SELF_DIR, fpath)

TEMPLATER_DIR = relative_fpath_opt('templates/')
DATABASE_FILE = relative_fpath_opt('database.db')

DB = web.database(dbn='sqlite', db=DATABASE_FILE)
