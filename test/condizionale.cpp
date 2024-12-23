#include <ostream>
void ifelse();

void ifelseifelse();

void ifelseshort();

void ifelse()
{
  int x = 12;
  int y = 20;
  if (x + y > 30) {
    x = x * y;
  }
  else {
    x = x * y + 30;
  }
}

void ifelseifelse()
{
  int x = 45;
  if (x * 3 > 70) {
    x = x * 2;
  }
  else   if (40 <= x && x <= 70) {
    x = x * 3;
  }
  else {
    x = x * 4;
  }
}

void ifelseshort()
{
  int x = 1;
  int y = 1;
  x = (x > y ? x * 2 + y * 3 : y * 2 + x * 3 * 2);
}

