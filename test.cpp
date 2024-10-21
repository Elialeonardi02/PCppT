#include "pcppt/codeCpp/FlexibleValue.h"

class persona{
  public:  int age;
  public:  float weight;
  public:  persona(int a, float w)
  {
    this->age = a;
    this->weight = w;
  }
  public:  int get_age()
  {
    return this->age;
  }
  public:  void set_age(int a)
  {
    this->age = a;
  }
};
void fun();

void fun()
{
  persona p = persona(1, 1.1);
  int c = 1;
  c = 2;
  int a = 3;
}

