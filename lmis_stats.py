import datetime
from random import randint
from lmis_fast import lmis

f = open("lmis_stats.txt", "w")
garbage = datetime.datetime.now()

for i in xrange(1,300):
  for j in xrange(0,5):
    datapoint = str(i) + "  "
  
    tmp = [randint(0,i) for x in xrange(0,i+1)]
    start = datetime.datetime.now()
    lmis(tmp,i)
    stop = datetime.datetime.now()
  
    delta = stop - start
    datapoint += str(delta.microseconds)
  
    f.write(datapoint + "\n")

f.close()
