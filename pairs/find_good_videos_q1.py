#!/usr/bin/env python
# -*- coding: utf8

from random import shuffle
from collections import defaultdict

import numpy as np
import urllib2

MIN_VIEWS = 5000 #videos must have at least this many views
FOLDS = 6
PER_FOLD = 10
GT = .5

#Loading data
X = np.genfromtxt('tseries.dat')[:, 1:] + 1e-6
ids = np.genfromtxt('tseries.dat', dtype='S11')[:, 0]
sum_views = X.sum(axis=1)

to_compare_idx = (sum_views >= MIN_VIEWS)
to_compare = set(ids[to_compare_idx])
id_to_pop = dict((id_, pop) for id_, pop in zip(ids, sum_views))

#Counting number of time each video appears
possible = []
with open('possible.pairs') as pairs_file:
    for line in pairs_file:
        spl = line.split()
        vid1 = spl[0]
        vid2 = spl[1]
        
        if vid1 in to_compare and vid2 in to_compare:
            pop1 = id_to_pop[vid1]
            pop2 = id_to_pop[vid2]
            if abs(pop1 - pop2) / max(pop1, pop2) >= GT:
                possible.append((vid1, vid2))

shuffle(possible)
total_vids = PER_FOLD * FOLDS

base = "http://gdata.youtube.com/feeds/api/videos/%s?v=2"
curr_fold = 0
num_pairs = 0
used = set()
for pair in possible:
    vid1, vid2 = pair
    
    if vid1 in used or vid2 in used:
        continue

    try:
        urllib2.urlopen(base % vid1)
        urllib2.urlopen(base % vid2)
        
        print curr_fold, vid1, vid2

        curr_fold = (curr_fold + 1) % FOLDS
        num_pairs += 1
        if num_pairs == total_vids:
            break

        used.add(vid1)
        used.add(vid2)
    except Exception as e:
        continue
