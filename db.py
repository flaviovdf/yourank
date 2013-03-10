# -*- coding: utf8
from __future__ import division, print_function
'''
Code for managing the database. Here we maintain
some "wrappers" for accessing the database. A lot 
of this code is unoptimized. Due to the small scale 
of our web experiment this should not be an issue.
'''

from config import DB
from config import EVAL_DB_NAME
from config import SESSION_DB_NAME
from config import PAIRS_DB_NAME

def num_pairs():
    '''Simply counts the number of rows in the pairs database'''

    count = 0
    for _ in DB.select(PAIRS_DB_NAME):
        count += 1
    return count

def has_id(session_id):

    try:
        result = DB.select(SESSION_DB_NAME, where='id=%d' % session_id, \
                what='curr_pair')
        result[0]['curr_pair']
        return True
    except IndexError:
        return False

def add_id(session_id):
    
    return DB.insert(SESSION_DB_NAME, id=session_id, curr_pair=1)

def get_pair_number(session_id):

    result = DB.select(SESSION_DB_NAME, where='id=%d' % session_id, \
            what='curr_pair')

    return result[0]['curr_pair']

def update_session(session_id):

    result = DB.select(SESSION_DB_NAME, where='id=%d' % session_id, \
            what='curr_pair')
    pair_number = result[0]['curr_pair'] + 1

    DB.update(SESSION_DB_NAME, where='id=%d' % session_id,
            curr_pair=pair_number)
    return pair_number


def get_videos(session_id):
    
    result = DB.select(SESSION_DB_NAME, where='id=%d' % session_id,
            what='curr_pair')
    pair_number = result[0]['curr_pair']

    result = DB.select(PAIRS_DB_NAME, where='pair_num=%d' % pair_number,
            what='video_id1,video_id2')

    row = result[0]
    return row['video_id1'], row['video_id2']
