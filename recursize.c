#include <stdio.h>

void recur(unsigned long x) {
  printf("recursion stack currently %lu levels deep\n",x++);
  recur(x);
  return;
}

void main() {
  unsigned long butt = 1;
  recur(butt);
}
