#!/usr/bin/env python
from __future__ import division, print_function

from collections import defaultdict

from myio import set_folder
from myio import get_survey_data

import numpy as np

import plac

def main(in_folder):
    set_folder(in_folder)
    survey = get_survey_data()

    for key in survey:
        print(key)
        d = survey[key]
        fracts = np.bincount(d) / d.shape[0]

        for a in sorted(set(d)):
            print(a, fracts[a])

if __name__ == '__main__':
    plac.call(main)
