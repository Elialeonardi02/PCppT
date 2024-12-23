#include <ostream>
void linkedComparison();

void linkedComparison()
{
  int x = 25;
  if (10 < x && x < 30) {
    x = x * 4 - 3 * x * 2 + x / 2;
  }
  else {
    x = x + 5 * 3 - x * 2;
  }
}

