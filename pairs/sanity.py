#!/usr/bin/env python
# -*- coding: utf8

from collections import defaultdict

data = defaultdict(set)
counts = defaultdict(int)
pairs = set()
with open('video.pairs') as video_file:
    for line in video_file:
        fold, vid1, vid2 = line.split()

        if (vid1, vid2) in pairs:
            print 'ERROR'

        if vid1 in data[fold]:
            print vid1, fold
        if vid2 in data[fold]:
            print vid2, fold

        counts[vid1] += 1
        counts[vid2] += 1

        pairs.add((vid1, vid2))
        pairs.add((vid2, vid1))

        data[fold].add(vid1)
        data[fold].add(vid2)

print counts
