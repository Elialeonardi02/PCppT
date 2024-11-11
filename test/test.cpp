template <typename T> T test();

template <typename T> T test()
{
  int a = 0;
  int x;
  if (x == 1 && x == 2 || 1 < x && x < 2) {
    x = ~x;
  }
  while(a || true && false){
    x = 1 + 2;
    break;
  }
}

