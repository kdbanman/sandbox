#include <stdio.h>

int main()
{
  while (1) {
    char gotten = getchar();
    if (gotten >0) printf("%c\n",gotten);
  }
}
