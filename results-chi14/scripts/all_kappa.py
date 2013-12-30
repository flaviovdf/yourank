#!/usr/bin/env python
from __future__ import division, print_function

from itertools import combinations

from myio import get_kappa_matrices
from myio import set_folder

from rpy2.robjects.packages import importr
from scipy import stats as ss
from statsmodels.stats import multitest

import csv
import numpy as np
import plac
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri #Automagic conversion of numpy to R
rpy2.robjects.numpy2ri.activate()

def main(in_folder):
    set_folder(in_folder)

    pass05, kappas05 = get_pairs_pass(.05, True) 
    pass01, kappas05 = get_pairs_pass(.01, True)
    pass001, kappas05 = get_pairs_pass(.001, True)
    
    for kind in pass05:
        test05 = pass05[kind].values()
        test01 = pass01[kind].values()
        test001 = pass001[kind].values()
        
        array_pass05 = []
        array_pass01 = []
        array_pass001 = []
        for pair in pass05[kind]:
            if pass05[kind][pair]:
                array_pass05.append(kappas05[kind][pair])
            
            if pass01[kind][pair]:
                array_pass01.append(kappas05[kind][pair])
            
            if pass001[kind][pair]:
                array_pass001.append(kappas05[kind][pair])


        print(kind)
        print('percept.', 'fract_pass_test', '< .4')
        print(kind, sum(test05) / len(test05), np.asarray(array_pass05) < 0.4)
        print(kind, sum(test01) / len(test01), np.asarray(array_pass01) < 0.4)
        print(kind, sum(test001) / len(test001), np.asarray(array_pass001) < 0.4)

def get_pairs_pass(sig=.05, return_kappa=False):
    matrix_kappa, matrix_pvals = all_kappa(True)
    return_val_pass = {}
    return_val_kappa = {}

    for kind in matrix_pvals:
        return_val_pass[kind] = {}
        return_val_kappa[kind] = {}

        pairs = matrix_pvals[kind].keys()
        pvals = []
        kappas = []
        for pair in pairs:
            pval = matrix_pvals[kind][pair]
            kappa = matrix_kappa[kind][pair]
            
            pvals.append(pval)
            kappas.append(kappa)
        
        pass_ = multitest.multipletests(pvals, sig, 'bonferroni')[0]
        for i, p in enumerate(pass_):
            return_val_pass[kind][pairs[i]] = pass_[i]
            return_val_kappa[kind][pairs[i]] = kappas[i]

    if return_kappa:
        return return_val_pass, return_val_kappa
    else:
        return return_val_pass
 
def all_kappa(return_pvals=False):
    irr = importr('irr')
    fleiss = irr.kappam_fleiss

    kappa_m = get_kappa_matrices()
    return_val = {}
    p_vals = {}

    for kind in ('like', 'share', 'pred'):
        
        pair_matrices = kappa_m[kind]
        return_val[kind] = {}
        p_vals[kind] = {}

        for pair in pair_matrices:
            rate_matrix = pair_matrices[pair]
            res = fleiss(rate_matrix, exact=False)
            val = res.rx2('value')[0]
            p_val = res.rx2('p.value')[0]
            
            return_val[kind][pair] = val
            p_vals[kind][pair] = p_val
    
    if not return_pvals:
        return return_val
    else:
        return return_val, p_vals

if __name__ == '__main__':
    plac.call(main)
