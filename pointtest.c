#include <stdio.h>

int main()
{
  int x;
  int *pointer = &x;
  for (int i = 0; i < 10 ; ++pointer, ++i) {
    printf("%d\n",(*pointer)++);
    printf("%d\n",*(pointer++));
  }
  
  return 0;
}
