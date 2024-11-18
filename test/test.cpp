auto tuple_key_extractor = [](auto t) {t.key;};
struct tuple_t{
  unsigned int key;

  float value;

  int a[3]={1, 2, 3};

  tuple_t() 
  {
  }

  tuple_t(unsigned int key, float value) 
  {
    this->key = key;
    this->value = value;
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

  template <typename T> T __str__() 
  {
    return <<"(sum: "<<this->sum<<", count: "<<this->count<<")";
  }

};
struct window_functor{
  window_functor() 
   =default;

  template <typename T> T __call__(tuple_t tuple, result_t result) 
  {
    adfbvfd.rec;
    decltype(result_t()) a = result_t();
  }

};
