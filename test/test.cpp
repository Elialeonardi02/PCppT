struct test{
public:
  test() 
  {
    int a[3] = {1, 2, 1};
    int b[] = {};
  }

};
template <typename T> T fun();

template <typename T> T fun()
{
  test a[10] = {test()};
}

