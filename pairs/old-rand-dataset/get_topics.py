#!/usr/bin/env python
# -*- coding: utf8

from apiclient.discovery import build

import glob
import json
import os
import plac
import sys

DEVELOPER_KEY = 'AIzaSyBv2cM4hW0NU15-LFCgJe-0ILHj8N7_nQ0'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
YOUTUBE_SCOPE = 'https://www.googleapis.com/auth/youtube'

def youtube_service():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY)

def get_json(youtube, video_id):
    search_response = youtube.videos().list(
            id=video_id,
            part='snippet,topicDetails').execute()
    return search_response

def get_video_ids(video_ids_fpath):
    video_ids = set()
    with open(video_ids_fpath) as videos_file:
        for line in videos_file:
            video_ids.add(line.strip())
    return video_ids

def ids_on_folder(output_folder):
    fpaths = glob.glob(os.path.join(output_folder, '*'))
    collected_ids = set()
    for fpath in fpaths:
        collected_ids.add(os.path.basename(fpath))
    return collected_ids

def main(video_ids_fpath, output_folder):
    youtube = youtube_service()

    video_ids = get_video_ids(video_ids_fpath)
    collected = ids_on_folder(output_folder)
    to_collect = video_ids.difference(collected)

    for video_id in to_collect:
        json_data = get_json(youtube, video_id)
        out_fpath = os.path.join(output_folder, video_id)

        with open(out_fpath, 'w') as out_file:
            json.dump(json_data, out_file)

if __name__ == '__main__':
    sys.exit(plac.call(main))
