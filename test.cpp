int f();

int fun(long long a, int b);

int f()
{
  return 1;
}

int fun(long long a, int b)
{
  b = 1;
  for (int i = 0; i < 10; ++i) {
    a += 1;
  }
  return 1;
}

