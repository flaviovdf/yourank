#!/usr/bin/env python
# -*- coding: utf8
from __future__ import division, print_function
'''
Script to create the database. This script simple uses the sqllite3 module to 
create a new empty database. Errors are not handled by the script and must be
done manually.
'''

from collections import defaultdict

from config import CREATE_DB_SCRIPT
from config import DATABASE_FILE
from config import PAIRS_DB_NAME
from config import ROUND_ROBIN_DB_NAME
from config import VIDEO_PAIRS_FILE

import sqlite3

def main():
    conn = sqlite3.connect(DATABASE_FILE)
    with open(CREATE_DB_SCRIPT) as sql_file:
        script = sql_file.read()

    cursor = conn.cursor()
    cursor.executescript(script)
    conn.commit()

    round_robin_pairs = defaultdict(int)

    with open(VIDEO_PAIRS_FILE) as pairs_file:
        for line in pairs_file:
            round_rbn, video1, video2 = line.split()

            round_rbn = int(round_rbn)
            round_robin_pairs[round_rbn] += 1
            pair_num = round_robin_pairs[round_rbn]

            cursor.execute('INSERT INTO %s VALUES (?, ?, ?, ?)' % \
                    PAIRS_DB_NAME, (round_rbn, pair_num, video1, video2))
    
    total_rounds = len(round_robin_pairs)
    for round_num in xrange(total_rounds):
        if round_num not in round_robin_pairs:
            raise Exception('Round numbers are not contiguous [0..n-1]')

    conn.commit()

    first_round = 0
    total_rounds = len(round_robin_pairs)

    cursor.execute('INSERT INTO %s VALUES (?, ?)' % ROUND_ROBIN_DB_NAME, \
            (first_round, total_rounds));

    conn.commit()
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
