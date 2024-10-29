void fun1();

void fun(int y);

void fun1()
{
  int c = 2;
}

void fun(int y)
{
  int z = 1;
  for (int i = 0; i < 1; ++i) {
    z += 2;
  }
  auto l = [](auto x, auto y) {return z + y;};
  l(1, 2);
}

