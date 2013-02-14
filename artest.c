#include <stdio.h>

int main() {
  unsigned long A[10];
  // segfauts on purpose
  for (int i = 0 ; true; ++i) {
    printf("%d%15lu\n",i,(long int)&A[i]);
  }
}
