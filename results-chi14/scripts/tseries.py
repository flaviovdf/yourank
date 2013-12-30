#!/usr/bin/env python
from __future__ import division, print_function

import matplotlib
matplotlib.use('Agg')

from collections import defaultdict

from matplotlib import rc
from matplotlib import pyplot as plt

from all_kappa import get_pairs_pass

from myio import get_opinions
from myio import get_kappa_matrices
from myio import get_tseries
from myio import set_folder

import numpy as np

import os

import plac

def initialize_matplotlib():
    inches_per_pt = 1.0 / 72.27
    golden_mean = (np.sqrt(5) - 1.0) / 2.0
    
    fig_width = 121 * inches_per_pt
    fig_height = fig_width * .5
    
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

def main(in_folder, out_folder):
    initialize_matplotlib()
    set_folder(in_folder)

    kappa_matrices = get_kappa_matrices()
    pairs_pass = get_pairs_pass()
    tseries = get_tseries()
    ops = get_opinions()

    i = 0
    for pair in pairs_pass['pred']:
        if pairs_pass['pred'][pair]:
            continue
        i += 1
        vid1, vid2 = pair
        tseries1 = tseries[vid1]
        tseries2 = tseries[vid2]

        tseries1 = tseries1[:-15] / 1e2
        tseries2 = tseries2[:-15] / 1e2

        pop1 = sum(tseries1)
        pop2 = sum(tseries2)
        
        if (abs(pop1 - pop2) / min(pop1, pop2)) >= 10:
            #plt.title('Pop G %d ; Pop L %d' % (max(pop1, pop2), min(pop1, pop2)))
            if pop1 > pop2:
                plt.plot(np.arange(tseries1.shape[0]), tseries1, 'r-', label='youtu.be/%s' % vid1)
                plt.plot(np.arange(tseries2.shape[0]), tseries2, 'b--', label='youtu.be/%s' % vid2)
            else:
                plt.plot(np.arange(tseries2.shape[0]), tseries2, 'r-', label='youtu.be/%s' % vid2)
                plt.plot(np.arange(tseries1.shape[0]), tseries1, 'b--', label='youtu.be/%s' % vid1)
            
            #plt.legend(loc='upper right')
            plt.xlabel('Days since upload')
            plt.ylabel(r'Views ($10^2$)')
            ax = plt.gca()
            for loc, spine in ax.spines.items():
                if loc in ['right','top']:
                    spine.set_color('none') # don't draw spine
                    plt.setp(plt.xticks()[1], rotation=0)
                    ax.xaxis.set_ticks_position('bottom')
                    ax.yaxis.set_ticks_position('left')
            out = os.path.join(out_folder, '%d.pdf' %i)
            plt.tight_layout(pad=0)
            plt.savefig(out)
            plt.close()

if __name__ == '__main__':
    plac.call(main)
