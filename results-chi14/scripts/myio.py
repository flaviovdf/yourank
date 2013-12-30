#!/usr/bin/env python
from __future__ import division, print_function

import csv
import numpy as np
import os

EVAL = 'eval.csv'
PAIRS =  'video.pairs'
POP = 'pop.dat'
TSERIES = 'tseries.dat'
SURVEY = 'survey.csv'

def set_folder(folder):
    #Ugly but works
    global EVAL
    global PAIRS
    global POP
    global TSERIES
    global SURVEY

    EVAL = os.path.join(folder, 'eval.csv')
    PAIRS = os.path.join(folder, 'video.pairs')
    POP = os.path.join(folder, 'pop.dat')
    TSERIES = os.path.join(folder, 'tseries.dat')
    SURVEY = os.path.join(folder, 'survey.csv')

def get_last_eval_time():
    import time
    rv = {}
    with open(EVAL) as eval_file:
        csv_reader = csv.reader(eval_file)
        for line in csv_reader:
            id_ = line[0]
            date = line[-1]

            date_1 = date.split('.')[0]
            date = time.mktime(time.strptime(date_1, '%Y-%m-%d %H:%M:%S'))
            if id_ not in rv:
                rv[id_] = date
            else:
                rv[id_] = max(rv[id_], date)
    return rv
 
def get_survey_time():
    import time
    rv = {}
    with open(SURVEY) as survey_csv:
        csv_reader = csv.reader(survey_csv)
        for line in csv_reader:
            id_ = line[0]
            date = line[-1]

            date_1 = date.split('.')[0]
            date = time.mktime(time.strptime(date_1, '%Y-%m-%d %H:%M:%S'))
            
            rv[id_] = date
    return rv
 
def get_survey_data():

    data = {}
    data['age'] = []
    data['gender'] = []
    data['watch'] = []
    data['share_vids'] = []
    data['share_content'] = []

    with open(SURVEY) as survey_csv:
        csv_reader = csv.reader(survey_csv)
        for line in csv_reader:
            age = int(line[1])
            gender = int(line[2])
            watch = int(line[4])
            share_vids = int(line[5])
            share_content = int(line[6])

            data['age'].append(age)
            data['gender'].append(gender)
            data['watch'].append(watch)
            data['share_vids'].append(share_vids)
            data['share_content'].append(share_content)
    
    for key in data.keys():
        data[key] = np.asarray(data[key])

    return data

def get_pairs():
    
    pairs = {}
    with open(PAIRS) as pairs_file:
        pair_num = 0
        for line in pairs_file:
            pair_num += 1
            fold, video_id1, video_id2 = line.split()

            pairs[pair_num] = (video_id1, video_id2)

    for pair_num in pairs:
        assert len(pairs[pair_num]) == 2

    return pairs

def get_tseries():

    tseries = {}
    ids = set(np.genfromtxt(POP, dtype='S11')[:, 0])
    with open(TSERIES) as tseries_file:
        for line in tseries_file:
            spl = line.split()
            vid = spl[0]
            data = np.array([int(x) for x in spl[1:]])
            
            if vid in ids:
                tseries[vid] = data

    return tseries

def get_db_results():

    results_like = {}
    results_share = {}
    results_pop = {}
    results_know = {}

    with open(EVAL) as eval_file:
        csv_reader = csv.reader(eval_file)
        for line in csv_reader:
            pair_id1 = line[2]
            pair_id2 = line[3]

            like_choice = int(line[4])
            share_choice = int(line[5])
            pop_choice = int(line[6])
            know_choice = int(line[7])

            if pair_id1 not in results_like:
                results_like[pair_id1] = 0

            if pair_id2 not in results_like:
                results_like[pair_id2] = 0
            
            if pair_id1 not in results_share:
                results_share[pair_id1] = 0

            if pair_id2 not in results_share:
                results_share[pair_id2] = 0
            
            if pair_id1 not in results_pop:
                results_pop[pair_id1] = 0

            if pair_id2 not in results_pop:
                results_pop[pair_id2] = 0

            if pair_id1 not in results_know:
                results_know[pair_id1] = 0

            if pair_id2 not in results_know:
                results_know[pair_id2] = 0

            if like_choice == 1:
                results_like[pair_id1] += 1
            elif like_choice == 2:
                results_like[pair_id2] += 1
            elif like_choice == 3:
                results_like[pair_id1] += 1
                results_like[pair_id2] += 1

            if share_choice == 1:
                results_share[pair_id1] += 1
            elif share_choice == 2:
                results_share[pair_id2] += 1
            elif share_choice == 3:
                results_share[pair_id1] += 1
                results_share[pair_id2] += 1
        
            if pop_choice == 1:
                results_pop[pair_id1] += 1
            elif pop_choice == 2:
                results_pop[pair_id2] += 1
            elif pop_choice == 3:
                results_pop[pair_id1] += 1
                results_pop[pair_id2] += 1

            if know_choice == 1:
                results_know[pair_id1] += 1
            elif know_choice == 2:
                results_know[pair_id2] += 1
            elif know_choice == 3:
                results_know[pair_id1] += 1
                results_know[pair_id2] += 1

    return results_like, results_share, results_pop, results_know

def get_opinions():

    return_value = {}
    with open(EVAL) as eval_file:
        csv_reader = csv.reader(eval_file)
        for line in csv_reader:
            pair_id1 = line[2]
            pair_id2 = line[3]
            op = line[-2]

            if (pair_id1, pair_id2) not in return_value:
                ops = []
                return_value[pair_id1, pair_id2] = ops
            else:
                ops = return_value[pair_id1, pair_id2]
            
            ops.append(op)
    return return_value


def get_kappa_matrices():

    num_eval = {}
    with open(EVAL) as eval_file:
        csv_reader = csv.reader(eval_file)
        for line in csv_reader:
            pair_id1 = line[2]
            pair_id2 = line[3]

            if (pair_id1, pair_id2) not in num_eval:
                num_eval[pair_id1, pair_id2] = 0

            num_eval[pair_id1, pair_id2] += 1

    kappa_matrices = {}
    kappa_matrices['like'] = {}
    kappa_matrices['share'] = {}
    kappa_matrices['pred'] = {}

    with open(PAIRS) as pairs_file:
        for line in pairs_file:
            _, pair_id1, pair_id2 = line.split()
            num = num_eval[pair_id1, pair_id2]
            kappa_matrices['like'][pair_id1, pair_id2] = \
                    np.zeros((2, num))
            kappa_matrices['share'][pair_id1, pair_id2] = \
                    np.zeros((2, num)) 
            kappa_matrices['pred'][pair_id1, pair_id2] = \
                    np.zeros((2, num)) 

    with open(EVAL) as eval_file:
        csv_reader = csv.reader(eval_file)
        curr_eval = {}
        for line in csv_reader:
            pair_id1 = line[2]
            pair_id2 = line[3]

            if (pair_id1, pair_id2) not in curr_eval:
                curr_eval[pair_id1, pair_id2] = 0
            else:
                curr_eval[pair_id1, pair_id2] += 1

            i = curr_eval[pair_id1, pair_id2]
            
            like_choice = int(line[4])
            share_choice = int(line[5])
            pred_choice = int(line[6])
            know_choice = int(line[7])
            
            if know_choice != 0:
                continue

            if like_choice == 1:
                kappa_matrices['like'][pair_id1, pair_id2][0, i] = 1
            elif like_choice == 2:
                kappa_matrices['like'][pair_id1, pair_id2][1, i] = 1
            elif like_choice == 3:
                kappa_matrices['like'][pair_id1, pair_id2][0, i] = 1
                kappa_matrices['like'][pair_id1, pair_id2][1, i] = 1

            if share_choice == 1:
                kappa_matrices['share'][pair_id1, pair_id2][0, i] = 1
            elif share_choice == 2:
                kappa_matrices['share'][pair_id1, pair_id2][1, i] = 1
            elif share_choice == 3:
                kappa_matrices['share'][pair_id1, pair_id2][0, i] = 1
                kappa_matrices['share'][pair_id1, pair_id2][1, i] = 1

            if pred_choice == 1:
                kappa_matrices['pred'][pair_id1, pair_id2][0, i] = 1
            elif pred_choice == 2:
                kappa_matrices['pred'][pair_id1, pair_id2][1, i] = 1
            elif pred_choice == 3:
                kappa_matrices['pred'][pair_id1, pair_id2][0, i] = 1
                kappa_matrices['pred'][pair_id1, pair_id2][1, i] = 1

    return kappa_matrices

def equalize_keys(pop_dict, ratings_dict):
    return_val = {}
    for key in ratings_dict:
        return_val[key] = pop_dict[key]
    return return_val

def load_dicts(pop_column=1):

    assert pop_column >= 1

    pop = np.genfromtxt(POP)[:, pop_column]
    ids = np.genfromtxt(POP, dtype='S11')[:, 0]

    pop_dict = dict(zip(ids, pop))

    like_dict, share_dict, pred_dict, know_dict = get_db_results()

    return pop_dict, like_dict, share_dict, pred_dict, know_dict


