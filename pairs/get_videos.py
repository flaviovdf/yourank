import glob
import os

IN = 'save'

set_ids = set()
for fpath in glob.glob(os.path.join(IN, '*')):
    curr_set = set()
    with open(fpath) as in_file:
        for line in in_file:
            spl = line.strip().split('/')[:-1]

            set_ids.update(spl)
            curr_set.update(spl)

for video_id in set_ids:
    print video_id
