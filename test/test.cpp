#include <ostream>
void rangeStop();

void rangeStop()
{
  int stop = 10;
  int total = 0;
  for (int i = 0; i < stop; ++i) {
    total += i * 2;
  }
}

