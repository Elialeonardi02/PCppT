struct ty{
  int a;

  ty() 
  :a(0) {}

ty(auto a) 
  {
    this->a = a;
  }

};
void foo(ty a)
{
  ty<int, int> b;

}

