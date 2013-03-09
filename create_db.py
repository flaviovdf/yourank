#!/usr/bin/env python
# -*- coding: utf8
from __future__ import division, print_function
'''
Script to create the database. This script simple uses
the sqllite3 module to create a new empty database. Errors
are not handled by the script and must be done manually.
'''
from config import DATABASE_FILE
from config import CREATE_DB_SCRIPT

import sqlite3

def main():
    conn = sqlite3.connect(DATABASE_FILE)
    with open(CREATE_DB_SCRIPT) as sql_file:
        cmd = sql_file.read()

    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
