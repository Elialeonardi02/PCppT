struct struct_139911357259040 {
  MixedData elements[100];
  int size = 0;
};
struct MixedData { enum class DataType { INT, CHAR }; DataType type; union { int intValue; char charValue; }; MixedData(int v) : type(DataType::INT), intValue(v) {} MixedData(char v) : type(DataType::CHAR), charValue(v) {} void print() { switch (type) { case DataType::INT: std::cout << "Integer: " << intValue << std::endl; break; case DataType::CHAR: std::cout << "Char: " << charValue << std::endl; break; } } };int fun(int a, int b);

int fun(int a, int b)
{
  c = struct_139911357259040 my_list;
my_list.size = 2;
my_list.elements[0] = MixedData(2);
my_list.elements[1] = MixedData(1);
;
  return a + b;
}

