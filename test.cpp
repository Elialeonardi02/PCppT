#include "pcppt/codeCpp/FlexibleValue.h"
#include "pcppt/codeCpp/ArrayMap.h"
void fun();

void fun()
{
  ArrayMap<float,int,2> a(
    KeyValuePair<float,int>(1.1,1),
    KeyValuePair<float,int>(2.2,2)
  );
  a.insert(1.1, 2);
  int b;
  FlexibleValue c[]= {{1}, {2}, {"a"}, {4}};
  float d[] = {1.0f, 2.3f};
  if (c[1].compare([](auto FlexibleValuec1)->bool{return FlexibleValuec1 == 1;})) {
    d[0] += 1;
  }
  float f = d[1];
  char e[] = "tests str";
  b = 3;
}

