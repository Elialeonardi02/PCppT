#include <ostream>
auto tuple_key_extractor = [](auto t) {return t + 1;};
struct tuple_t{
  unsigned int key;

  float value;

  tuple_t() 
  {
    this->key = 0;
    this->value = 0.0;
  }

  tuple_t(unsigned int key, float value) 
  {
    this->key = key;
    this->value = value;
  }

  friend std::ostream & operator<<(std::ostream & os, const tuple_t & d) 
  {
    os<<"key: "<<d.key<<","<<"value: "<<d.value<<"";
    return os;
  }

};
struct result_t{
  float sum;

  unsigned int count;

  float result;

  result_t() 
  {
    this->sum = 0.0;
    this->count = 0;
  }

  int   a() 
  {
    int a = 1;
    int bac[4] = {1, 2, 3, 4};
    return a;
  }

  float   mean(int a[10]) 
  {
    this->result = this->sum + this->count;
    return this->sum / this->count;
  }

  friend std::ostream & operator<<(std::ostream & os, const result_t & d) 
  {
    os<<"sum: "<<d.sum<<","<<"count: "<<d.count<<","<<"result: "<<d.result<<"";
    return os;
  }

};
struct window_functor{
  void   __call__(tuple_t tuple, result_t result) 
  {
    result.sum += tuple.value;
    result.count = result.count + 1;
  }

  tuple_t   test(tuple_t tuple) 
  {
    return tuple;
  }

};
int a();

int testl();

int fun(int a);

int a()
{
  int a = 1;
  return a;
}

int testl()
{
  auto z = [](auto x) {return x + 1;};
  int a = 1;
  auto t = tuple_key_extractor(1);
  return 1;
}

int fun(int a)
{
  int b = 0;
  int test = testl();
  return b;
}

