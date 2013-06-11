#!/usr/bin/env python
# -*- coding: utf8

from itertools import combinations

import glob
import json
import os
import plac
import sys

def ids_on_folder(input_folder):
    fpaths = glob.glob(os.path.join(input_folder, '*'))
    collected_ids = set()
    for fpath in fpaths:
        collected_ids.add(os.path.basename(fpath))
    return [video_id for video_id in collected_ids]

def get_from_json(input_folder, video_id):
    fpath = os.path.join(input_folder, video_id)
    with open(fpath) as json_file:
        json_data = json.loads(json_file.read())
        topics = set()
        if 'items' in json_data and len(json_data['items']) > 0:
            sub_data = json_data['items'][0]
            category = sub_data['snippet']['categoryId']
            #topics.add(category)
            if 'topicDetails' in sub_data \
                and 'topicIds' in sub_data['topicDetails']:
                topics.update(sub_data['topicDetails']['topicIds'])
        
        return set(topics)

def get_topics(input_folder, video_id, cache):
    if video_id in cache:
        topics = cache[video_id]
    else:
        topics = get_from_json(input_folder, video_id)
        cache[video_id] = topics

    return topics

def main(input_folder):
    
    collected = ids_on_folder(input_folder)
    cache = {}

    for video_id, other_video_id in combinations(collected, 2):
        topics_video_id = get_topics(input_folder, video_id, cache)
        topics_other_video_id = get_topics(input_folder, other_video_id, cache)

        inter = len(topics_video_id.intersection(topics_other_video_id))
        union = len(topics_video_id.union(topics_other_video_id))
        sim = 0 if union == 0 else (1.0 * inter) / union

        print video_id, other_video_id, sim

if __name__ == '__main__':
    sys.exit(plac.call(main))
