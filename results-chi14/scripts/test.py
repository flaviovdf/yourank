#!/usr/bin/env python
from __future__ import division, print_function

from collections import defaultdict

from all_kappa import get_pairs_pass

from myio import load_dicts
from myio import get_kappa_matrices
from myio import set_folder

from rpy2.robjects.packages import importr
from scipy import stats as ss

import numpy as np
import plac
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri #Automagic conversion of numpy to R
rpy2.robjects.numpy2ri.activate()


def get_majority_minority(popularity_dict, pairs):

    majority_group = []
    minority_group = []
    for pair in pairs:
        pair_id1, pair_id2 = pair

        if popularity_dict[pair_id1] > popularity_dict[pair_id2]:
            maj_video, min_video = pair_id1, pair_id2
        else:
            maj_video, min_video = pair_id2, pair_id1

        majority_group.append(maj_video)
        minority_group.append(min_video)

    return majority_group, minority_group

def binom_test(majority_a, majority_b):

    majority_a = set(majority_a)
    majority_b = set(majority_b)

    agree = majority_b.intersection(majority_a)
    
    num_agree = len(agree)
    num_test = len(majority_b)
    p = 0.5
    
    return ss.binom_test(num_agree, num_test, p=.5)

def binom_ci(majority_a, majority_b, alpha=.95):

    binom = importr('binom')

    majority_a = set(majority_a)
    majority_b = set(majority_b)

    n_agree = len(majority_a.intersection(majority_b))
    n_all = len(majority_b)
    
    ci_res = binom.binom_confint(n_agree, n_all, alpha, method='exact', alternative='greater')
    mean = ci_res.rx2('mean')[0]
    size = ci_res.rx2('mean')[0] - ci_res.rx2('lower')[0]

    return mean, size

def stat_tests(popularity_dict_a, popularity_dict_b, pairs):

    keys_a = set(popularity_dict_a.keys())
    keys_b = set(popularity_dict_b.keys())
    assert len(keys_a - keys_b) == 0
    assert len(keys_b - keys_a) == 0

    majority_a, minority_a = get_majority_minority(popularity_dict_a, pairs)
    majority_b, minority_b = get_majority_minority(popularity_dict_b, pairs)

    m, ci = binom_ci(majority_a, majority_b)
    print('Binomal Proportion CI of agreements: %.3f +- %.3f' % (m, ci))
    
    p_b = binom_test(majority_a, majority_b)
    print('Binomial Test for 0.5 (random chance): p = %.3f' % p_b)

def main(in_folder):
    set_folder(in_folder)

    pop_dict = load_dicts()[0]
    kappa_matrices = get_kappa_matrices()
    pairs_pass = get_pairs_pass(sig=.05)

    for t in kappa_matrices:
        print('Testing views with user ', t)
        
        all_pop = {}
        all_user = {}
        pairs = set()
        for i, pair in enumerate(kappa_matrices[t]):
            vid1 = pair[0]
            vid2 = pair[1]
            
            if (vid1, vid2) in kappa_matrices[t]:
                mat1 = kappa_matrices[t][(vid1, vid2)][0]
                mat2 = kappa_matrices[t][(vid1, vid2)][1]
            else:
                mat1 = kappa_matrices[t][(vid1, vid2)][1]
                mat2 = kappa_matrices[t][(vid1, vid2)][0]
            
            pass_ = pairs_pass[t]
            if ((vid1, vid2) in pass_ and pass_[(vid1, vid2)]) \
                    or ((vid2, vid1) in pass_ and pass_[(vid2, vid1)]):
                all_pop['%s-%d' % (vid1, i)] = pop_dict[vid1]
                all_pop['%s-%d' % (vid2, i)] = pop_dict[vid2]
            
                all_user['%s-%d' % (vid1, i)] = sum(mat1)
                all_user['%s-%d' % (vid2, i)] = sum(mat2)

                pairs.add(('%s-%d' % (vid1, i), '%s-%d' % (vid2, i)))
        
        print('Testing with %d pairs' % len(all_pop))
        stat_tests(all_pop, all_user, pairs)
        print()
    
if __name__ == '__main__':
    plac.call(main)
