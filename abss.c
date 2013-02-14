#include <stdio.h>
#include <limits.h>

int abs(int x) 
{
  if (x >=0) return x;
  return -x;
}

void abstest(int x) 
{
  printf("abs(%d) == %d\n",x,abs(x));
}

int main() 
{
  short a = 0, b = -1, c = SHRT_MAX, d = SHRT_MIN;
  int ai = 0, bi = -1, ci = -65536, di = 65535, ei = INT_MAX, fi = INT_MIN;
  float af = 0.0, bf = 5.0;

  printf("\nshorts\n");
  abstest(a);
  abstest(b);
  abstest(c);
  abstest(d);

  printf("\nints:\n");
  abstest(ai);
  abstest(bi);
  abstest(ci);
  abstest(di);
  abstest(ei);
  abstest(fi);
  printf("\nfloats:\n");
  abstest(af);
  abstest(bf);
}
