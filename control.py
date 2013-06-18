# -*- coding: utf8
from __future__ import division, print_function
'''
This module maintains the application logic. It is responsible for bridging 
the views with the database.
'''

from config import DB
from config import IDLEN

import db
import string
import random

def random_id():
    '''Generates a random ascii string composed of numbers'''
    
    chars = string.digits
    new_id = int(''.join(random.choice(chars) for x in xrange(IDLEN)))

    with DB.transaction():
        while has_id(new_id): #TODO: We can make IDs in sequence
            new_id = int(''.join(random.choice(chars) for x in xrange(IDLEN)))
        db.add_id(new_id)

    return new_id

def num_pairs(session_id):
    '''
    Gets the total number of pair to be evaluated
    '''

    return db.num_pairs(session_id)

def has_id(session_id):
    '''Tests if an id is in the databases'''

    return db.has_id(session_id)

def get_video_ids(session_id):
    '''
    Gets the videos id to be evaluated, returning None when the experiment is 
    finished.
    '''

    pair_number = db.get_pair_number(session_id)
    if pair_number > db.num_pairs(session_id):
        return None
    else:
        vid1, vid2 = db.get_videos(session_id)
        return pair_number, vid1, vid2

def has_user_id(session_id):
    '''Tests if the user has already supplied demographic data. This is done
    by checking if the database has this information'''

    return db.has_user_id(session_id)

def save_user_info(session_id, age, gender, country, view, share, share_all):
    '''Saves used info to the database'''

    with DB.transaction():
        db.save_user_info(session_id, age, gender, country, view, share, 
                share_all)

def save_start_eval(session_id, pair_number):
    '''Saves the timestamp of when a videopage is loaded'''

    with DB.transaction():
        db.save_start_eval(session_id, pair_number)

def save_results(session_id, like, share, pop, details):
    '''Saves results and increments video pair number'''

    pair_id, id1, id2 = get_video_ids(session_id)
    with DB.transaction():
        db.save_choice(session_id, pair_id, id1, id2, like, share, pop, 
                details)
        return db.update_session(session_id)
