#!/usr/bin/env python
# -*- coding: utf8

from apiclient.discovery import build

from collections import defaultdict

from itertools import combinations

from math import log10
from math import trunc

from random import shuffle

import json
import os
import plac
import urllib
import sys

DEVELOPER_KEY = 'AIzaSyDi6lWtWCOzHVA6RgC15IlvyzPAHTVLsgo'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
FREEBASE_URL = 'https://www.googleapis.com/freebase/v1/search?filter=(all name:"%s")'

def youtube_service():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY)

def get_mids(query):
    freebase_url = FREEBASE_URL % (query)
    freebase_response = json.loads(urllib.urlopen(freebase_url).read())
    mids = []
    print freebase_response
    if 'result' in freebase_response:
        for result in freebase_response['result']:
            mids.append(result['mid'])
    return mids

def get_ids(youtube, topic, month):
    
    if log10(month) >= 1:
        m = '%s' % month
    else:
        m = '0%s' % month
    
    pageToken = ''
    ids = set()
    while pageToken is not None:
        search = youtube.search().list(
                order='relevance', 
                publishedAfter='2012-%s-01T00:00:00Z' % m,
                publishedBefore='2012-%s-28T23:59:59Z' % m, 
                videoEmbeddable='true', videoSyndicated='true', 
                topicId=topic, 
                maxResults=50, pageToken=pageToken, regionCode='US', 
                safeSearch='strict', videoDuration='medium', 
                type='video', part='id')
        
        results = search.execute()
        for video in results['items']:
            ids.add(video['id']['videoId'])
        
        if 'nextPageToken' in results:
            pageToken = results['nextPageToken']
        else:
            pageToken = None

    return ids

def get_pop_duration(youtube, video):
    response = youtube.videos().list(
            id=video, part='statistics,contentDetails').execute()
    pop = response['items'][0]['statistics']['viewCount']
    dur = response['items'][0]['contentDetails']['duration']
    return pop, dur

def main():
    #topics = ['/m/09p14', '/m/05f4p', '/m/01hmnh', '/m/05gwr', '/m/01664_', '/m/018jz']
    topic = '/m/0mdxd'
    num_per_group = 3
    candidates = []

    youtube = youtube_service()
    count = defaultdict(list)
    pops_dur = {}
    ids = get_ids(youtube, topic, 4)
    for video in ids:
        pop, dur = get_pop_duration(youtube, video)
        pop = int(pop)
        dur_mins = int(dur.split('M')[0].split('T')[1])
        if dur_mins >= 3 and dur_mins <= 6:
            count[trunc(log10(pop + 1))].append(video)
            pops_dur[video] = (pop, dur)
            
    for k in sorted(count):
        if k in [1, 3, 5]:
            ids = count[k]
            shuffle(ids)
            candidates.extend(ids[:num_per_group])

    for video in candidates:
        print >>sys.stderr, video, pops_dur[video]

    fold = 0
    sorted_candidates = sorted(candidates)
    num_folds = 9

    free = {}
    for video in candidates:
        free[video] = range(num_folds)

    for i in xrange(len(sorted_candidates)):
        for j in xrange(i + 1, len(sorted_candidates)):
            print candidates[i], candidates[j]

if __name__ == '__main__':
    sys.exit(plac.call(main))
