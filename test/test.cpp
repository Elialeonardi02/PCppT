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
int testa();

void testF(testC t);

int testa()
{
  return 1;
}

void testF(testC t)
{
  testC a = t;
  t.c = 1;
  float z = t.rint() + 1e-10;
  t.rint();
  testa();
}

