#include <ostream>
void continueCicle();

void continueCicle()
{
  int total = 0;
  for (int i = 1; i < 21; ++i) {
    if (i % 2 == 0) {
      continue;
    }
    total += i;
  }
}

