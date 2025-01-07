#include <ostream>
class personclass{
private:
  float __height;

  int __age;

public:
  personclass() 
  :__height(0.0),__age(0) {}

  personclass(int age, float height) 
  {
    this->__height = height;
    this->__age = age;
  }

  friend std::ostream & operator<<(std::ostream & os, const personclass & d) 
  {
    os<<"__height: "<<d.__height<<","<<"__age: "<<d.__age<<"";
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
