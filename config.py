# -*- coding: utf8
from __future__ import division, print_function
'''Configuration constants are kept here'''

import os

import web

SELF_DIR = os.path.dirname(os.path.realpath(__file__))
relative_fpath_opt = lambda fpath: os.path.join(SELF_DIR, fpath)

TEMPLATE_DIR = relative_fpath_opt('templates/')
DATABASE_FILE = relative_fpath_opt('database.db')
DB_SCRIPTS_FOLDER = relative_fpath_opt('sql/')
CREATE_DB_SCRIPT = relative_fpath_opt(os.path.join('sql', 'create.sql'))

DB = web.database(dbn='sqlite', db=DATABASE_FILE)
