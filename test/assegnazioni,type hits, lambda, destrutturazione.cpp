#include <ostream>
auto x = [](auto t) {return t + 1;};
void test();

void test()
{
  int a1;
  double b1 = 0.0;
  float b[] = {1, 2, 3, 4};
  int c[2] = {1, 2};
  int d[10] = {9, 8};
  d[4] = 5;
  int f[4] = {};
  f[1] = 4;
  int g = 1;
  float h = 0.2;
  float i = g + h;
  float l[3] = {1, g + 2 + h, h};
  l[1] += 1;
  i += 0.2;
  auto x1 = [](auto t) {return t + 1;};
  auto c1 = [](auto t) {return t + 1;};
  auto c2 = [](auto t) {return t + 1;};
  auto c3 = [](auto t) {return t + 1;};
  auto c4 = [](auto t) {return t + 1;};
  float d1[3] = {1, 2, 0.4 + 1};
  float d2[3] = {1, 2, 0.4 + 1};
  float d3[3] = {1, 2, 0.4 + 1};
}

