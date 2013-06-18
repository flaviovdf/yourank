#!/usr/bin/env python
# -*- coding: utf8

import glob
import json
import os

IN = 'videos'

for f in glob.glob(os.path.join(IN, '*api.json')):
    with open(f) as json_file:
        data = json.load(json_file)
        first_idx = f.find('-')
        last_idx = f.rfind('-')
        
        assert first_idx >= 0
        assert last_idx > first_idx
        
        vid_id = f[first_idx + 1:last_idx]
        print f[first_idx + 1:last_idx], data['view']
