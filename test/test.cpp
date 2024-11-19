auto tuple_key_extractor = [](auto t) {t.key;};
struct tuple_t{
  unsigned int key;

  float value;

  tuple_t() 
  {
  #pragma HLS inline
    this->key = 0;
    this->value = 0.0;
  }

  tuple_t(unsigned int key, float value) 
  {
  #pragma HLS inline
    this->key = key;
    this->value = value;
  }

};
struct result_t{
  float sum;

  unsigned int count;

  result_t() 
  {
  #pragma HLS inline
    this->sum = 0.0;
    this->count = 0;
  }

  float mean() 
  {
  #pragma HLS inline
    return this->sum / this->count;
  }

};
struct window_functor{
  window_functor() 
   =default;
  #pragma HLS inline

  template <typename T> T __call__(tuple_t tuple, result_t result) 
  {
  #pragma HLS inline
    result.sum += tuple.value;
    result.count = result.count + 1;
  }

};
