#include <ostream>
auto z = [](auto x) {return x + 1;};
class personclass{
private:
  float __height;

public:
  int age;

  personclass() 
  :__height(0.0),age(0) {}

personclass(int age, float height) 
  {
    this->__height = height;
    this->age = age;
  }

};
struct personstruct{
  int age;

  float height;

  personclass person;

  personstruct() 
  :age(0),height(0.0),person() {}

personstruct(int age, float height, personclass person) 
  {
    this->age = age;
    this->height = height;
    this->person = person;
    z(1);
  }

};
struct window_functor{
  void __call__(personclass personS) 
  {
    personS.age += 1;
  }

};
void arrayParameter(int b = 1, float c = 2.23)
{

}

