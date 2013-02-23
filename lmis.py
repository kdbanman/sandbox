# computes the longest monotonically increasing subsequence 
# of a list

import random

runtime = 0
def lmis(A, p, r):
  '''
  LMIS stands for longest monotonically increasing subsequence
  A is a list of things that can be compared with > or <
  p is the index to start looking for the LMIS (from the left)
  r is the last index of the search
  lmis(A, 0, len(A)) finds the LMIS of A
  '''
  # base case: LMIS of single element is itself
  if p == r:
    return [A[p]]

  # find LMIS from contiguous MIS onward
  C = []
  for i in range(p+1, r+1):
    global runtime
    runtime += 1

    if A[i] > A[p]:
      TMP = lmis(A, i, r)
      if len(TMP) > len(C):
        C = TMP

  LONGEST = [A[p]]
  LONGEST.extend(C)
  return LONGEST

if __name__ == "__main__":
  A = [1,2,3,4]
  B = [5,4,3,2]
  C = [3,4,8,1,2,3,10]
  D = [2]
  E = [1,9,2,8,3,7,3,6,4]
  F = [1,9,2,8,3,7,3,6,4,5]
  G = [x for x in xrange(0,20)]
  G1 = [2*x for x in xrange(0,20)]
  G2 = [x for x in xrange(0,20)]
  G2[10] = 1
  H = [100-x for x in xrange(0,20)]
  I = [random.randint(0,100) for x in xrange(0,30)]
  J = [random.randint(0,100) for x in xrange(0,30)]

  tests = [A,B,C,D,E,F,G,G1,G2,H,I,J]
  for L in tests:
    runtime = 0
    print L
    print lmis(L, 0, len(L)-1)
    print runtime
    print ""
    raw_input()
