# -*- coding: utf8
# Configuration is kept as a python module of constants.
# Only change config for a new empty database!!
from __future__ import division, print_function
'''Configuration constants are kept here'''

import os
import web

SELF_DIR = os.path.dirname(os.path.realpath(__file__))
relative_fpath_opt = lambda fpath: os.path.join(SELF_DIR, fpath)

# ID length
IDLEN = 8

# Files and dirs
TEMPLATE_DIR = relative_fpath_opt('templates/')
DATABASE_FILE = relative_fpath_opt('database.db')
DB_SCRIPTS_FOLDER = relative_fpath_opt('sql/')
CREATE_DB_SCRIPT = relative_fpath_opt(os.path.join('sql', 'create.sql'))
VIDEO_PAIRS_FILE = relative_fpath_opt(os.path.join('pairs', 'video.pairs'))

# Database names
EVAL_DB_NAME = 'eval'
SESSION_DB_NAME = 'sstate'
PAIRS_DB_NAME = 'pairs'
START_DB_NAME = 'pageloads'
USER_DB_NAME = 'userdetails'

DB = web.database(dbn='sqlite', db=DATABASE_FILE)
