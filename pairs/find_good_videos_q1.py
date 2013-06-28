#!/usr/bin/env python
# -*- coding: utf8

from random import shuffle
from collections import defaultdict

import numpy as np

MIN_VIEWS = 5000 #videos must have at least this many views
FOLDS = 10
PER_FOLD = 6

#Loading data
X = np.genfromtxt('tseries.dat')[:, 1:] + 1e-6
ids = np.genfromtxt('tseries.dat', dtype='S11')[:, 0]
sum_views = X.sum(axis=1)

to_compare_idx = (sum_views >= MIN_VIEWS)
to_compare = set(ids[to_compare_idx])

#Counting number of time each video appears
possible = []
with open('possible.pairs') as pairs_file:
    for line in pairs_file:
        spl = line.split()
        vid1 = spl[0]
        vid2 = spl[1]
        
        if vid1 in to_compare and vid2 in to_compare:
            possible.append((vid1, vid2))

shuffle(possible)
possible = possible[:PER_FOLD * FOLDS]

curr_fold = 0
for pair in possible:
    vid1, vid2 = pair

    print curr_fold, vid1, vid2
    curr_fold = (curr_fold + 1) % FOLDS
