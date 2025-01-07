#include <ostream>
void nWhile();

void doWhile();

void nWhile()
{
  int limit = 15;
  int total = 0;
  int i = 1;
  while(i <= limit){
    total += i * 3;
    i += 2;
  }
}

void doWhile()
{
  int product = 1;
  int i = 1;
  int limit = 10;
  while(true){
    product *= i;
    i += 2;
    if (i > limit) {
      break;
    }
  }
}

