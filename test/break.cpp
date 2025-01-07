#include <ostream>
void breakCycle();

void breakCycle()
{
  int limit = 50;
  int total = 0;
  int sum = 0;
  for (int i = 1; i < limit; ++i) {
    sum += i;
    if (sum > 100) {
      break;
    }
    total += i * 2;
  }
}

