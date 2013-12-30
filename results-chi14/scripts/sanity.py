import csv

data = {}
with open('eval.csv') as eval_file:
    csv_reader = csv.reader(eval_file)
    for row in csv_reader:
        id_, p1, p2 = row[1:4]

        if (p1, p2) not in data:
            data[(p1, p2)] = id_
        else:
            assert data[(p1, p2)] == id_

print len(data)
