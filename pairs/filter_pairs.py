#!/usr/bin/env python
# -*- coding: utf8

from random import shuffle

DATA = 'late_pop.pairs'
FLIM = .2
PLIM = 5e3

def main():
    videos_f = []
    videos_a = []
    with open(DATA) as data_file:
        for line in data_file:
            spl = line.split()
            
            vid1 = spl[0]
            vid2 = spl[1]

            view1 = float(spl[2])
            view2 = float(spl[3])

            frac1 = float(spl[4])
            cat = spl[-1]

            if view1 > PLIM and view2 > PLIM and cat != 'Music':
                if view1 >= view2 and frac1 >= FLIM:
                    videos_f.append((vid1, vid2))
                elif frac1 < FLIM:
                    videos_a.append((vid1, vid2))


    shuffle(videos_f)
    shuffle(videos_a)

    videos_a = videos_a[:len(videos_f)]
    
    for pair in videos_f:
        print pair[0], pair[1]
    
    for pair in videos_a:
        print pair[0], pair[1]

if __name__ == '__main__':
    main()
