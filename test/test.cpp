#include <ostream>
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

  friend std::ostream & operator<<(std::ostream & os, const personclass & d) 
  {
    os<<"__height: "<<d.__height<<","<<"age: "<<d.age<<"";
    return os;
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
  }

  friend std::ostream & operator<<(std::ostream & os, const personstruct & d) 
  {
    os<<"age: "<<d.age<<","<<"height: "<<d.height<<","<<"person: "<<d.person<<"";
    return os;
  }

};
struct window_functor{
  void  operator()(personclass & personS) 
  {
    personS.age += 1;
  }

};
void arrayParameter(int a[10][10], int b[1]);

void arrayParameter(int a[10][10], int b[1])
{
  a[1][2];
}

