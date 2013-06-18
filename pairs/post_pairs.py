from itertools import combinations

import glob
import os

IN = 'save'

for fpath in glob.glob(os.path.join(IN, '*')):
    curr_set = set()
    with open(fpath) as in_file:
        for line in in_file:
            spl = line.strip().split('/')[:-1]

            curr_set.update(spl)
        
        for video1, video2 in combinations(curr_set, 2):
            print video1, video2, 1
