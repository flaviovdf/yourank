#!/usr/bin/env python
from __future__ import division, print_function

from matplotlib import pyplot as plt
from collections import defaultdict

from myio import set_folder
from myio import get_last_eval_time
from myio import get_survey_time

import numpy as np

import plac

def main(in_folder):
    set_folder(in_folder)

    st = get_survey_time()
    et = get_last_eval_time()
    
    res = np.zeros(len(et), dtype='f')
    for i, key in enumerate(st):
        res[i] = et[key] - st[key]
    
    plt.hist(res, bins=20)
    plt.show()

    print(np.mean(res))
    print(np.std(res))
    print(np.std(res) / np.mean(res))

if __name__ == '__main__':
    plac.call(main)
