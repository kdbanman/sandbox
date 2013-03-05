import random
import sys


def padded(A, width=5):
  tmp = ""
  for elem in A:
    tmp += str(elem).center(width)
  
  return tmp


def prPrint(A, p, r):
  top = padded(A)
  middle = ""
  if p < r:
    middle = "     "*p + "  p  " + "     "*(r-p-1) + "  r  "
  else:
    middle = "     "*p + " p r "
  bottom = ""
 
  print top + "\n" + middle + "\n" + bottom + "\n"


def quickPrint(A, p, q, r):
  top = padded(A)
  middle = "     "*q + "  q  "
  bottom = ""
  if p < r:
    bottom = "     "*p + "  p  " + "     "*(r-p-1) + "  r  "
  else:
    bottom = "     "*p + " p r "

  print top + "\n" + middle + "\n" + bottom + "\n"


def partitionPrint(A, p, r, i, j):
  if (p == r):
    print "UH OH"

  top = padded(A)

  middle = ""
  if i == -1 and j == 0:
    middle = "i j  "
  elif i == -1:
    middle = "i    " + "     "*(j-1) + "  j  "
  elif i == j:
    middle = "     "*i + " i j "
  else:
    middle = "     "*i + "  i  " + "     "*(j-i-1) + "  j  "

  bottom = "     "*p + "  p  " + "     "*(r-p-1) + "  r  "
  
  print top + "\n" + middle + "\n" + bottom + "\n"


def partition(A, p, r):
  pivot = A[r]
  i = p-1
  for j in xrange(p,r+1):

    if j != p:
      print "PARTITIONING ABOUT PIVOT A[r], INCREMENTING j:"
    else:
      print "PARTITIONING ABOUT PIVOT A[r]:"

    partitionPrint(A, p, r, i, j)
    raw_input()

    if A[j] < pivot:
      print "ELEMENT A[j] LESS THAN PIVOT A[r], INCREMENTING i:"
      partitionPrint(A, p, r, i, j)
      raw_input()

      i += 1
      
      if i != j:
        print "SWAPPING A[i] WITH ELEMENT A[j]:"
      else:
        print "i EQUAL TO j, SO ELEMENT A[i] GETS SELF-SWAPPED:"
      partitionPrint(A, p, r, i, j)
      raw_input()

      swap = A[i]
      A[i] = A[j]
      A[j] = swap

      if i != j:
        print "SWAPPING A[i] WITH ELEMENT A[j]:"
      else:
        print "i EQUAL TO j, SO ELEMENT A[i] GETS SELF-SWAPPED:"
      partitionPrint(A, p, r, i, j)
      raw_input()

  if i != r - 1:
    print "SWAPPING PIVOT A[r] INTO PLACE:"
    partitionPrint(A, p, r, i, r)
    raw_input()
  
    i += 1
  
    print "SWAPPING PIVOT A[r] INTO PLACE:"
    partitionPrint(A, p, r, i, r)
    raw_input()
  
    swap = A[i]
    A[i] = pivot
    A[r] = swap
    
    print "SWAPPING PIVOT A[r] INTO PLACE:"
    partitionPrint(A, p, r, i, r)
    raw_input()

  else:
    print "PIVOT A[r] ALREADY IN PLACE, NO NEED TO SWAP:"
    partitionPrint(A, p, r, i, r)
    raw_input()
   
    i += 1

  return i


recurCall = 1
def tail_quicksort(A, p, r):
  global recurCall
  
  print "RECURSIVE CALL " + str(recurCall)
  recurCall += 1

  if p < r:
    print "NOW SORTING ARRAY FROM p TO r:"
    prPrint(A, p, r)
    raw_input()

  while p < r:

    q = partition(A, p, r)

    print("DONE PARTITIONING ABOUT INDEX q:")
    quickPrint(A, p, q, r)
    raw_input()

    tail_quicksort(A, p, q-1)
    p = q+1


def printUsage():
  print "\n  to visualize the sorting of an array of length <len>:"
  print "    >python tail_quicksort.py <len>"
  print "  where <len> is greater than 3\n"
  sys.exit(1)

  
if __name__ == "__main__":

  if len(sys.argv) != 2:
    printUsage()
  
  arrLen = 10
  try:
    arrLen = int(sys.argv[1])
    assert arrLen >= 3 
  except:
    printUsage()

  arr = [random.randint(1,100) for x in xrange(0, arrLen)]
  
  tail_quicksort(arr, 0, len(arr)-1)

  print "ARRAY OF LENGTH " + str(len(arr)) + " SORTED:\n" + padded(arr)
