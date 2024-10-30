class test{
protected:
  float _b;

public:
  int a = 2;

  int c[3] = {1, 2, 3};

  void fun1() 
  {
  }

  void fun2() 
  {
    int d = 3;
  }

};
void fun(int y);

void fun(int y)
{
  int c[] = {1, 2, 3, 4};
  test test1[] = {test(), test()};
  test1[1].fun1();
  int d[3] = {1, 2, 3};
  int z = 1;
  for (int i = 0; i < 1; ++i) {
    z += 2;
  }
  auto l = [](auto x, auto y) {x + y;};
  l(1, 2);
}

