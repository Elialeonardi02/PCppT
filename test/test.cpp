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

  tuple_t(unsigned int key, float value) 
  {
    this->key = key;
    this->value = value;
  }

  friend std::ostream & operator<<(std::ostream & os, const tuple_t & d) 
  {
    os<<"key: "<<"d.key,"<<"value: "<<"d.value";
    return os;
  }

};
