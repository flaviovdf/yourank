def roundRobin(units, sets=None):
    if len(units) % 2:
        units.append(None)

    count    = len(units)
    sets     = sets or (count - 1)
    half     = count / 2
    schedule = []
    for turn in range(sets):
        pairings = []
        for i in range(half):
            pairings.append((units[i], units[count-i-1]))
        units.insert(1, units.pop())
        schedule.append(pairings)
    return schedule

vid_set = set()
with open('video.pairs') as inf:
    for line in inf:
        v1, v2 = line.split()
        vid_set.add(v1)
        vid_set.add(v2)

vids = [v for v in vid_set]
fold = 0
for l in roundRobin(vids):
    for p in l:
        if p[0] is not None and p[1] is not None:
            print fold, p[0], p[1]
    fold += 1

#vids.append('off')

#fixtures = []
#rotation = list(vids)
#for i in range(0, len(vids) - 1):
#
#    fixtures.append(rotation)
#    rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]

#fold = 0
#for f in fixtures:
#    for v in range(0, len(f), 2):
#        if f[v] != 'off' and f[v + 1] != 'off':
#            print fold, f[v], f[v + 1]
#    fold += 1
