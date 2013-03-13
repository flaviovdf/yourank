# -*- coding: utf8
from __future__ import division, print_function
'''
This module maintains the application logic. It is responsible
for bridging the views with the database.
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

   while has_id(new_id):
       new_id = int(''.join(random.choice(chars) for x in xrange(IDLEN)))

   return new_id

def add_id(session_id):
    '''Adds session id to the databases'''
    #TODO: treat error if already exists

    db.add_id(session_id)

def num_pairs():
    '''
    Gets the total number of pair to be evaluated
    '''

    return db.num_pairs()

def has_id(session_id):
    '''Tests if an id is in the databases'''

    return db.has_id(session_id)

def get_video_ids(session_id):
    '''
    Gets the videos id to be evaluated, returning
    None when the experiment is finished.
    '''

    pair_number = db.get_pair_number(session_id)
    if pair_number > db.num_pairs():
        return None
    else:
        vid1, vid2 = db.get_videos(session_id)
        return pair_number, vid1, vid2

def save_results(session_id, like, share, pop, details):
    '''Saves results and increments video pair number'''

    pair_id, id1, id2 = get_video_ids(session_id)
    with DB.transaction():
        db.save_choice(session_id, pair_id, id1, id2, like, share, pop, 
                details)
        return db.update_session(session_id)
