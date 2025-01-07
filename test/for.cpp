#include <ostream>
void rangeStop();

void rangeStartStop();

void rangeStartStopStep();

void rangeStop()
{
  int stop = 10;
  int total = 0;
  for (int i = 0; i < stop; ++i) {
    total += i * 2;
  }
}

void rangeStartStop()
{
  int start = 5;
  int stop = 15;
  int product = 1;
  for (int i = start; i < stop; ++i) {
    if (i % 2 == 0) {
      product *= i;
    }
  }
}

void rangeStartStopStep()
{
  int start = 2;
  int stop = 20;
  int step = 4;
  int weighted_sum = 0;
  int index = 0;
  for (int i = start; i < stop; i += step) {
    weighted_sum += i * index;
    index += 1;
  }
}

