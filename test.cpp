template <typename T> 
 T fun(int a, int b);

template <typename T> 
 T fun(int a, int b)
{
  b = 1;
  for (int i = 0; i < 10; ++i) {
    a += 1;
  }
  return 1;
}

