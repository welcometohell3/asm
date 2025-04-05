#include <stdio.h>

extern int asm_foo(int a, int b, int c, int d, int e, int f, int g, int h);

int c_foo(int x, int y) { return x + y; }

int main() {
  int result = asm_foo(1, 2, 3, 4, 5, 6, 7, 8);
  printf("%d\n", result);
  return 0;
}