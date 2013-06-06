#!/usr/bin/env python
# -*- coding: utf8

import numpy as np

ASSIGN = 'assign.dat'
CATEG = 'rand.tags'
TSERIES = 'rand.dat'
ONLINE = 'online.ids'

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

cls = np.genfromtxt(ASSIGN, dtype='i')
categs = np.genfromtxt(CATEG, usecols = [2], dtype='S10', filling_values=['-'])
ids = np.genfromtxt(TSERIES, dtype='S11')[:, 0]
X = np.genfromtxt(TSERIES)[:, 1:]
online_ids = set(np.genfromtxt(ONLINE, dtype='S11'))

late_ids, late_categs, X_late = get_videos(cls, categs, ids, X, online_ids, [1, 2], 10)
cte_ids, cte_categs, X_cte = get_videos(cls, categs, ids, X, online_ids, [0], -1)
