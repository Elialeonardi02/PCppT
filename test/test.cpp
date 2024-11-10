struct test{
public:
  test() 
  {
    char a[] = "aaaaa";
    const char* b[3] = {"Aaaa", "a", "aaaa"};
  }

};
template <typename T> T fun();

template <typename T> T fun()
{
  test a[10] = {test()};
}

