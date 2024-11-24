#include <ostream>
auto tuple_key_extractor = [](auto t) {t.key;};
void funct(int la);

void fun();

void funct(int la)
{
  auto a = 1 + 1;
}

void fun()
{
  funct(2);
}

