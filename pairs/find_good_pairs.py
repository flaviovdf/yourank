from random import shuffle
from collections import defaultdict

import numpy as np

X = np.genfromtxt('tseries.dat')[:, 1:] + 1e-6
ids = np.genfromtxt('tseries.dat', dtype='S11')[:, 0]

sum_views = X.sum(axis=1)
peak_frac = X.max(axis=1) / sum_views
peak_time = X.argmax(axis=1)

late_peak_idx = (sum_views >= 5000) & (peak_frac >= .1) & (peak_time > 10)
late_peak_videos = set(ids[late_peak_idx])

to_compare_idx = sum_views >= 5000 & (peak_frac < .1)
to_compare = set(ids[to_compare_idx])

num_use = 5
used_counter = defaultdict(int)
possible_q1 = []
possible_q2 = []
with open('possible.pairs') as pairs_file:
    for line in pairs_file:
        spl = line.split()
        vid1 = spl[0]
        vid2 = spl[1]
        
        if vid1 in late_peak_videos and \
                vid2 not in late_peak_videos and \
                vid2 in to_compare:
            possible_q1.append((vid1, vid2))
            
            used_counter[vid1] = min(num_use, used_counter[vid1] + 1)
            used_counter[vid2] = min(num_use, used_counter[vid2] + 1)

        elif vid2 in late_peak_videos and \
                vid1 not in late_peak_videos and \
                vid1 in to_compare:
            possible_q1.append((vid1, vid2))
            
            used_counter[vid1] = min(num_use, used_counter[vid1] + 1)
            used_counter[vid2] = min(num_use, used_counter[vid2] + 1)

        elif vid1 in to_compare and vid2 in to_compare:
            possible_q2.append((vid1, vid2))
        
            used_counter[vid1] = min(num_use, used_counter[vid1] + 1)
            used_counter[vid2] = min(num_use, used_counter[vid2] + 1)

for vid in used_counter.keys():
    if used_counter[vid] < num_use:
        used_counter[vid] = 0

shuffle(possible_q1)
shuffle(possible_q2)

folds = 20
curr_fold = 0
num_pairs_q1 = 0
for pair in possible_q1:
    vid1, vid2 = pair
    if used_counter[vid1] > 0 and used_counter[vid2] > 0:
        used_counter[vid1] -= 1
        used_counter[vid2] -= 1

        print curr_fold, vid1, vid2
        curr_fold = (curr_fold + 1) % folds
        num_pairs_q1 += 1

curr_fold = 0
num_pairs_q2 = 0
for pair in possible_q2:
    vid1, vid2 = pair
    if used_counter[vid1] > 0 and used_counter[vid2] > 0:
        used_counter[vid1] -= 1
        used_counter[vid2] -= 1

        print curr_fold, vid1, vid2
        curr_fold = (curr_fold + 1) % folds
        num_pairs_q2 += 1

        if num_pairs_q2 == num_pairs_q1:
            break
