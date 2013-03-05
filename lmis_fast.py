# computes the longest monotonically increasing subsequence 
# of a list

import random

runtime = 0
def lmis(A, p):
  '''
  LMIS stands for longest monotonically increasing subsequence
  A is a list of things that can be compared with > or <
  p is the index to start looking for the LMIS (from the right)
  lmis(A, len(A)) finds the LMIS of A
  '''
  # base case: LMIS of single element is itself
  if p == 0:
    return [A[0]]

  # find monotonically increasing elements that are contiguous
  CONTIG = [A[p]]
  i = p-1

  while i >= 0 and A[i] < A[i+1]:
    global runtime
    runtime += 1

    CONTIG.append(A[i])
    i -= 1
  CONTIG.reverse()

  i += 1
  if i == 0:
    return CONTIG
  
  # find LMIS from contiguous MIS onward
  C = []
  for j in range(i-1, -1, -1):
    global runtime
    runtime += 1

    if A[j] < A[i]:
      TMP = lmis(A, j)
      if len(TMP) > len(C):
        C = TMP

  C.extend(CONTIG)
  return C

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
  K = [random.randint(0,1000) for x in xrange(0,1000)]

  tests = [A,B,C,D,E,F,G,G1,G2,H,I,J,K]
  for L in tests:
    runtime = 0
    print L
    print lmis(L, len(L)-1)
    print runtime
    print ""
    raw_input()
