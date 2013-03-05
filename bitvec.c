#include <stdlib.h>
#include <stdio.h>

typedef unsigned int uint;

// struct Foo containing bit fields a, b, c, d, each occupying 4 bits
struct Foo
{
  uint a : 4;
  uint b : 4;
  int c : 4;
  int d : 4;
};

void printFoo(struct Foo f)
{
  static int calls = 0;
  calls++;
  
  printf("Fields of current Foo, number %d:\n", calls);
  printf("  a:  %u\n", f.a);
  printf("  b:  %u\n", f.b);
  printf("  c:  %d\n", f.c);
  printf("  d:  %d\n", f.d);
}

int main()
{
  printf("\nSTACK FOO:\n\n");

  struct Foo ex;
  printFoo(ex);

  ex.a = 0;
  ex.b = 15;
  ex.c = -8;
  ex.d = 7;
  printFoo(ex);

  ex.a = -1;
  ex.a = 16;
  ex.c = -9;
  ex.d = 8;
  printFoo(ex);

  printf("\nHEAP FOO:\n\n");

  struct Foo *hxp = malloc(sizeof(struct Foo));
  printFoo((*hxp));

  (*hxp).a = 0;
  (*hxp).b = 15;
  (*hxp).c = -8;
  (*hxp).d = 7;
  printFoo((*hxp));

  hxp->a = -1;
  hxp->b = 16;
  hxp->c = -9;
  hxp->d = 8;
  printFoo((*hxp));

  free(hxp);

  return 0;
}
