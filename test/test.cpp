#include <ostream>
struct testC{
  int c;

  int a;

  testC() 
  {
    this->c = 0;
    this->a = this->c;
    int c = this->rint();
  }

  int   rint() 
  {
    return 1;
  }

  friend std::ostream & operator<<(std::ostream & os, const testC & d) 
  {
    os<<"c: "<<d.c<<","<<"a: "<<d.a<<"";
    return os;
  }

};
struct testB{
  testC b;

  testB() 
  :b() {}

  testB(testC a) 
  {
    this->b = a;
  }

  friend std::ostream & operator<<(std::ostream & os, const testB & d) 
  {
    os<<"b: "<<d.b<<"";
    return os;
  }

};
int testa();

int testa()
{
  return 1;
}

