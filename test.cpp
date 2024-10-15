class person{
  public:  int age;
  public:  float weight;
  public:  person(int a, float w)
  {
    this->age = a;
    this->weight = w;
  }
  public:  int get_age()
  {
    return this->age;
  }
  public:  void set_age(int a)
  {
    this->age = a;
  }
};
void create_person(int a, int w);

void create_person(int a, int w)
{
  person p =  person(a, w);
  int a1 = 2;
  float w1 = 4.6;
  person p1 =  person(a1, w1);
  p1.get_age();
  p1.set_age(10);
}

