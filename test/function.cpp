#include <ostream>
int function(int a);

float returnTypeInferenceFunction(int a);

int returnTypeInferenceFunction(auto a);

int function(int a)
{
  int b = 10;
  return a * b;
}

float returnTypeInferenceFunction(int a)
{
  float b = 10.2;
  return a * b;
}

int returnTypeInferenceFunction(auto a)
{
  float b = 10.2;
}

