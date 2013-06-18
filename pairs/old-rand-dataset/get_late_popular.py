#!/usr/bin/env python
# -*- coding: utf8

from itertools import product

import numpy as np

ASSIGN = 'assign.dat'
CATEG = 'rand.tags'
TSERIES = 'rand.dat'
ONLINE = 'online.ids'
SIM = 'fb.sim'

def get_videos(cls, categs, ids, X, online_ids, cls_to_use, peak_time_min):
    categs = categs.copy()
    ids = ids.copy()
    X = X.copy()

    to_use = np.zeros(X.shape[0], dtype='bool')
    for k in cls_to_use:
        to_use[cls == k] = True

    X = X[to_use, :]
    ids = ids[to_use, :]
    categs = categs[to_use, :]

    reverse_sort = X.sum(axis=1).argsort()[::-1]
    X = X[reverse_sort]
    ids = ids[reverse_sort]
    categs = categs[reverse_sort]

    peak_time = X.argmax(axis=1)
    late_peak = peak_time > peak_time_min
    X = X[late_peak]
    ids = ids[late_peak]
    categs = categs[late_peak]

    online_idx = np.zeros(X.shape[0], dtype='bool')
    for i, id_ in enumerate(ids):
        online_idx[i] = id_ in online_ids

    X = X[online_idx]
    ids = ids[online_idx]
    categs = categs[online_idx]

    return ids, categs, X

def print_videos(Xi, Xj, categs_i, categs_j, ids_i, ids_j, similarities):

    pop_i = Xi.sum(axis=1)
    pop_j = Xj.sum(axis=1)
   
    max_i = Xi.max(axis=1) / pop_i
    max_j = Xj.max(axis=1) / pop_j

    argmx_i = Xi.argmax(axis=1)
    argmx_j = Xj.argmax(axis=1)

    range_i = range(Xi.shape[0])
    range_j = range(Xj.shape[0])

    for i, j in product(range_i, range_j):
        if categs_i[i] == categs_j[j] and ids_i[i] != ids_j[j] and \
                (ids_i[i], ids_j[j]) in similarities:

            print ids_i[i], ids_j[j], \
                    pop_i[i], pop_j[j], \
                    max_i[i], max_j[j], \
                    argmx_i[i], argmx_j[j], \
                    similarities[(ids_i[i], ids_j[j])], categs_i[i]

def load_similarites():
    similarities = {}
    with open(SIM) as sim_file:
        for line in sim_file:
            spl = line.split()
            vid1 = spl[0]
            vid2 = spl[1]
            sim = float(spl[2])

            if sim > 0:
                similarities[(vid1, vid2)] = sim
    return similarities

def main():
    cls = np.genfromtxt(ASSIGN, dtype='i')
    categs = np.genfromtxt(CATEG, usecols = [2], dtype='S10')
    ids = np.genfromtxt(TSERIES, dtype='S11')[:, 0]
    X = np.genfromtxt(TSERIES)[:, 1:]
    online_ids = set(np.genfromtxt(ONLINE, dtype='S11'))

    late_ids, late_categs, X_late = get_videos(cls, categs, ids, X, online_ids,
            [1, 2, 3], 10)
    cte_ids, cte_categs, X_cte = get_videos(cls, categs, ids, X, online_ids, 
            [0], -1)

    similarites = load_similarites()

    print_videos(X_late, X_cte, late_categs, cte_categs, late_ids, cte_ids,
            similarites)
    print_videos(X_cte, X_cte, cte_categs, cte_categs, cte_ids, cte_ids,
            similarites)

if __name__ == '__main__':
    main()
