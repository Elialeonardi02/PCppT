class cl{
  int p;
 public:  cl(){
    this->p = 1;
  }
 public:  void _s(){
    int a =  1;
    this->p = 2;
  }
 protected:};
int fun(int a, int b);

int fun(int a, int b)
{
  a = a + b;
  cl p =  cl();
  return 1;
}

