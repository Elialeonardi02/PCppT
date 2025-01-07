#include <ostream>
void passCycle();

void passCycle()
{
  int total = 0;
  for (int i = 1; i < 21; ++i) {
    if (i % 3 == 0) {

    }
    else {
      total += i * 2;
    }
  }
}

