/**/

#include <stdio.h>
#include <stdlib.h>

int main(void) {
  int i;
  
  srand(255+255+255+1);
  
  for (i = 0; i < 10; i++) {
    printf("%d\n", rand());
  }
  return 0;
}