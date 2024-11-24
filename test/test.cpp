#include <ostream>
auto tuple_key_extractor = [](auto t) {t.key;};
struct tuple_t{
  unsigned int key;

  float value;

  tuple_t() 
  {
    this->key = 0;
    this->value = 0.0;
  }

  friend std::ostream & operator<<(std::ostream & os, const tuple_t & d) 
  {
    os<<"key: "<<"d.key,"<<"value: "<<"d.value";
    return os;
  }

};
struct result_t{
  float sum;

  unsigned int count;

  result_t() 
  {
    this->sum = 0.0;
    this->count = 0;
  }

  float mean() 
  {
    return this->sum / this->count;
  }

  friend std::ostream & operator<<(std::ostream & os, const result_t & d) 
  {
    os<<"sum: "<<"d.sum,"<<"count: "<<"d.count";
    return os;
  }

};
