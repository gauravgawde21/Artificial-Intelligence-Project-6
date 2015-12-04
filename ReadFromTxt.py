__author__ = 'gp'

with open("DataSet/featnames.csv") as f:
   for line in f:
       print line

str = "Line1-abcdef \nLine2-abc \nLine4-abcd";
print str.split( )[1];

