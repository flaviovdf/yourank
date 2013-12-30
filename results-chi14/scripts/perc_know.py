#!/usr/bin/env python
from __future__ import division, print_function

from collections import defaultdict

from all_kappa import get_pairs_pass

from myio import set_folder
from myio import load_dicts

import plac

def main(in_folder):
    set_folder(in_folder)

    know_dict = load_dicts()[-1]
    pairs_pass = get_pairs_pass(1)
    
    q = 'like'
    for pair in sorted(pairs_pass[q]):
        vid1 = pair[0]
        vid2 = pair[1]
        
        print(vid1, vid2, know_dict[vid1], know_dict[vid2])

if __name__ == '__main__':
    plac.call(main)
