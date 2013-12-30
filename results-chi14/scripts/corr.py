#!/usr/bin/env python
from __future__ import division, print_function

import matplotlib
matplotlib.use('Agg')

from all_kappa import all_kappa
from all_kappa import get_pairs_pass

from matplotlib.ticker import FuncFormatter
from matplotlib import pyplot as plt
from matplotlib import rc

from myio import get_pairs
from myio import load_dicts
from myio import set_folder

from scipy import stats as ss

import csv
import numpy as np
import plac 

def initialize_matplotlib():
    inches_per_pt = 1.0 / 72.27
    golden_mean = (np.sqrt(5) - 1.0) / 2.0
    
    fig_width = 100 * inches_per_pt
    fig_height = fig_width
    
    rc('axes', labelsize=7.2)
    rc('axes', unicode_minus=False)
    rc('axes', grid=False)
    rc('figure', figsize=(fig_width, fig_height))
    rc('grid', linestyle=':')
    rc('font', family='serif')
    rc('legend', fontsize=7.2)
    rc('lines', linewidth=0.5)
    rc('axes', linewidth=0.5)
    rc('ps', usedistiller='xpdf')
    rc('text', usetex=True)
    rc('xtick', labelsize=7.2)
    rc('ytick', labelsize=7.2)

def my_formatter(x, pos):
    if x == 0:
        return '0'
    elif x >= 1:
        return '1'
    else:
        return str(x).replace('0', '', 1)

def main(in_folder):

    set_folder(in_folder)
    initialize_matplotlib()

    pop_dict = load_dicts(1)[0]
    pairs = get_pairs()
    kappas = all_kappa()
    pass_ = get_pairs_pass(.05)

    x_pass = []
    x_not_pass = []

    y_pass = []
    y_not_pass = []
    for video1, video2 in pass_['pred']:
        if not pass_['pred'][video1, video2]:
            x = x_not_pass
            y = y_not_pass
        else:
            x = x_pass
            y = y_pass
        
        p1 = pop_dict[video1]
        p2 = pop_dict[video2]
        
        kap = kappas['pred'][video1, video2]
        y.append(abs(p1 - p2) / 1e4)
        x.append(kap)
 
    major_formatter = FuncFormatter(my_formatter)

    plt.plot(x_not_pass, y_not_pass, 'rs', label=r'$\kappa \leq 0$', ms=2.5)
    plt.plot(x_pass, y_pass, 'go', label=r'$\kappa > 0$', ms=2.5)

    ax = plt.gca()
    ax.xaxis.set_major_formatter(major_formatter)

    plt.xlabel('Kappa score')
    plt.ylabel(r'Diff. in Popularity x$10^4$')
    plt.setp(plt.xticks()[1], rotation=10)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08), ncol=2, fancybox=True, numpoints=1,
            fontsize=5, columnspacing=0)
    plt.tight_layout(pad=0)
    plt.savefig('corr-kap.pdf')

    print('Spearman', ss.spearmanr(x_pass + x_not_pass, y_pass + y_not_pass))
    print('Kendall', ss.kendalltau(x_pass + x_not_pass, y_pass + y_not_pass))
    
if __name__ == '__main__':
    plac.call(main)
