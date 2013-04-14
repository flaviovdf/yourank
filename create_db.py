#!/usr/bin/env python
# -*- coding: utf8
from __future__ import division, print_function
'''
Script to create the database. This script simple uses the sqllite3 module to 
create a new empty database. Errors are not handled by the script and must be
done manually.
'''

from config import DATABASE_FILE
from config import CREATE_DB_SCRIPT
from config import PAIRS_DB_NAME
from config import VIDEO_PAIRS_FILE

import sqlite3

def main():
    conn = sqlite3.connect(DATABASE_FILE)
    with open(CREATE_DB_SCRIPT) as sql_file:
        script = sql_file.read()

    cursor = conn.cursor()
    cursor.executescript(script)
    conn.commit()

    with open(VIDEO_PAIRS_FILE) as pairs_file:
        pair_num = 0
        for line in pairs_file:
            video1, video2 = line.split()
            pair_num += 1
            cursor.execute('INSERT INTO %s VALUES (?, ?, ?)' % PAIRS_DB_NAME, \
                    (pair_num, video1, video2))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
