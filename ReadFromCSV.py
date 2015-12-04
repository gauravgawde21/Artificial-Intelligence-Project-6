__author__ = 'gp'

import csv

from itertools import izip;

'''
count = 0;
with open('DataSet/featnames.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        print row[0]
        count = count + 1;

print "count",count;
'''

'''
#buildDataMaps(trainFeat, "./DataSet/trainfeat.csv", "./DataSet/trainlabs.csv");
count = 0;
with open("./DataSet/trainfeat.csv") as csvfile1, open("./DataSet/trainlabs.csv") as csvfile2:
    for x, y in izip(csvfile1, csvfile2):
        x = x.strip()
        y = y.strip()
        print y;
        count = count + 1;
    print count;
'''

arr = "1 2 3 4 5 6 7 8";

for a in arr:
    print a;