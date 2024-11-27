#include <ostream>
auto tuple_key_extractor = [](auto t) {t.key;};
struct result_t{
  float sum;

  unsigned int count;

  float result;

  result_t() 
  :sum(0.0),count(0),result(0.0) {}

  float  mean() 
  {
    this->result = this->sum / this->count;
    return this->sum / this->count;
  }

  friend std::ostream & operator<<(std::ostream & os, const result_t & d) 
  {
    os<<"sum: "<<d.sum<<","<<"count: "<<d.count<<","<<"result: "<<d.result<<"";
    return os;
  }

};
