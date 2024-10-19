#include "pcppt/codeCpp/FlexibleValue.h"

void fun();

void fun()
{
  FlexibleValue c[]= {{1}, {2}, {3}, {4}, {5}};
  int a =  1;
  c[a].setValue(1);
}

