auto tuple_key_extractor = [](auto t) {t.key;};
struct tuple_t{
  unsigned int key;

  float value;

  tuple_t() 
  :key(0),value(0.0) {}

  int a() 
  {
    return 1;
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

};
struct window_functor{
  window_functor() 
   = default;

  template <typename T> T __call__(tuple_t tuple, result_t result) 
  {
    result.sum += tuple.value;
    result.count = result.count + 1;
  }

};
