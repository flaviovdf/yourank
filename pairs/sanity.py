#!/usr/bin/env python
# -*- coding: utf8

from collections import defaultdict

data = defaultdict(set)
with open('video.pairs') as video_file:
    for line in video_file:
        fold, vid1, vid2 = line.split()

        if vid1 in data[fold]:
            print vid1, fold
        if vid2 in data[fold]:
            print vid2, fold

        data[fold].add(vid1)
        data[fold].add(vid2)
