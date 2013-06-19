# -*- coding: utf8
from __future__ import division, print_function
'''
Code for managing the database. Here we maintain some "wrappers" for accessing
the database. This code is not thread safe, transactions must be used in order
to achieve such safety. Example:

    >>> from config import DB
    >>> import db
    >>> with DB.transaction():
        >>> db.add_id(1)

A lot of this code is unoptimized. Due to the small scale of our 
web experiment this should not be an issue.
'''

from config import DB
from config import EVAL_DB_NAME
from config import SESSION_DB_NAME
from config import PAIRS_DB_NAME
from config import ROUND_ROBIN_DB_NAME 
from config import START_DB_NAME
from config import USER_DB_NAME

from datetime import datetime

def num_pairs(session_id):
    '''
    Simply counts the number of rows in the pairs for the round of the
    given user.
    '''

    result = DB.select(SESSION_DB_NAME, 
            where='session_id=%d' % session_id, what='round_rbn')
    round_num = result[0]['round_rbn']

    count = 0
    for _ in DB.select(PAIRS_DB_NAME, where='round_rbn=%d' % round_num):
        count += 1
    return count

def has_id(session_id):
    '''Checks if the session database already has this session id'''

    try:
        result = DB.select(SESSION_DB_NAME, 
                where='session_id=%d' % session_id, what='num_eval')
        result[0]['num_eval']
        return True
    except IndexError:
        return False

def add_id(session_id):
    '''Adds new id to the session database'''
    
    round_select = DB.select(ROUND_ROBIN_DB_NAME)[0]
    curr_round = round_select['current_round']
    total_rounds = round_select['total_rounds']

    DB.insert(SESSION_DB_NAME, session_id=session_id, round_rbn=curr_round, 
            num_eval=0)

    next_round = (curr_round + 1) % total_rounds 
    return DB.update(ROUND_ROBIN_DB_NAME, 
            where='current_round=%d' % curr_round, current_round=next_round)
    
def has_user_id(session_id):
    '''Checks if the user demographic database already has this session id'''

    try:
        result = DB.select(USER_DB_NAME, where='session_id=%d' % session_id, \
                what='session_id')
        result[0]['session_id']
        return True
    except IndexError:
        return False

def get_number_evaluated(session_id):
    '''Get's number of pairs evaluted for a given session'''

    result = DB.select(SESSION_DB_NAME, where='session_id=%d' % session_id, \
            what='num_eval')

    return result[0]['num_eval']

def update_session(session_id):
    '''Increments the evaluation pair for a session'''

    result = DB.select(SESSION_DB_NAME, where='session_id=%d' % session_id, \
            what='num_eval')
    num_eval = result[0]['num_eval'] + 1

    DB.update(SESSION_DB_NAME, where='session_id=%d' % session_id,
            num_eval=num_eval)
    return num_eval

def save_choice(session_id, pair_id, id1, id2, like, share, pop, additional):
    '''Saves an evaluation'''

    return DB.insert(EVAL_DB_NAME, session_id=session_id, pair_num=pair_id, 
            video_id1=id1, video_id2=id2, like_choice=like, share_choice=share,
            pop_choice=pop, additional=additional, dateof=datetime.utcnow())

def save_user_info(session_id, age, gender, country, view, share, share_all):
    '''Saves user demographic data to the database'''

    return DB.insert(USER_DB_NAME, session_id=session_id, age=age, 
            gender=gender, country=country, watch_videos=view, 
            share_videos=share, share_content=share_all, 
            dateof=datetime.utcnow())

def save_start_eval(session_id, pair_id):
    '''Saves when an evaluation has started'''

    return DB.insert(START_DB_NAME,
            session_id=session_id, pair_num=pair_id, dateof=datetime.utcnow())

def get_evaluated(session_id):
    '''Gets videos which were evaluated to be evaluated'''
    
    results = DB.select(EVAL_DB_NAME, where='session_id=%d' % session_id,
            what='pair_num')

    evaluated = set()
    for result in results:
        evaluated.add(result['pair_num'])

    return evaluated

def save_current_pair(session_id, pair_number):
    '''Saves the current pair being evaluated'''

    return DB.update(SESSION_DB_NAME, where='session_id=%d' % session_id,
            curr_pair=pair_number)

def get_curr_pair(session_id):
    '''Gets the current pair being evaluated'''

    result = DB.select(SESSION_DB_NAME, 
            where='session_id=%d' % session_id, what='curr_pair')

    return result[0]['curr_pair']

def get_videos(session_id, pair_number):
    '''Gets the pair id for the round of the given user (session id)'''

    result = DB.select(SESSION_DB_NAME, 
            where='session_id=%d' % session_id, what='round_rbn')
    round_num = result[0]['round_rbn']

    result = DB.select(PAIRS_DB_NAME,
            where='pair_num=%d AND round_rbn=%d' % (pair_number, round_num),
            what='video_id1,video_id2')

    row = result[0]
    return row['video_id1'], row['video_id2']
