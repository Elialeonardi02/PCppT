int a;
class test {
  int b;
  test() 
{
    this->b = 1;
  }
};
int fun(int a, int b);

int fun(int a, int b)
{
  a = 2;
  return a + b;
}

