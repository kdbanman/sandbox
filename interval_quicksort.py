# NOT COMPLETE, I FUCKED UP AND HAD TO GO HOME.  NOT CORRECT AND BROKEN
#   can be fixed by partitioning on left interval boundaries w.r.t the
#   left boundary of the pivot, then partitioning the left partition on the
#   right boundaries w.r.t the pivot's left boundary, then partitioning the
#   right partition on the left boundaries w.r.t the pivot's right boundary

from random import randint
from random import shuffle

def swap(A, x, y):
  tmp = A[x]
  A[x] = A[y]
  A[y] = tmp

def right_of_bounds(a, b):
  return a[0] > b[0] and a[1] > b[1]

def left_of_bounds(a, b):
  return a[0] < b[0] and a[1] < b[1]

def on_left_bound(a, b):
  return a[0] < b[0] and a[1] > b[0]

def on_right_bound(a, b):
  return a[0] < b[1] and a[1] > b[1]

def fuzzy_partition(A, p, r):
  pivot = A[randint(p, r)]

  print "before partition:"
  print A, p, r

  left = p-1
  right = r+1

  for j in xrange(p, right):
    if left_of_bounds(A[j], pivot):
      left += 1
      swap(A, left, j)
 
  for j in xrange(r, left, -1):
    if right_of_bounds(A[j], pivot):
      right -= 1
      swap(A, right, j)

  return_left = left
  return_right = right

  for j in xrange(left+1, right):
    if on_left_bound(A[j], pivot):
      left += 1
      swap(A, left, j)

  for j in xrange(right-1, left, -1):
    if on_right_bound(A[j], pivot):
      right -= 1
      swap(A, right, j)

  fuzzy_sort(A, left, right)

  print "after partition"
  print A, left, right
  raw_input()

  return return_left, return_right

def fuzzy_sort(A, p, r):
  if p < r:
    q1, q2 = fuzzy_partition(A, p, r)
    fuzzy_sort(A, p, q1)
    fuzzy_sort(A, q2, r)

if __name__ == "__main__":

  test = [(1.0,5.6),(2.9,3.1),(-2.3,9.1),(7.6,10.8),(0.0,1.2),(-5.0,-1.0)]
  fuzzy_sort(test,0,len(test)-1)

  test2 = [(-10,10),(-9,-8),(-7,-6),(-5,-4),(-3,-2)]
  shuffle(test2)
  fuzzy_sort(test2,0,len(test2)-1)
