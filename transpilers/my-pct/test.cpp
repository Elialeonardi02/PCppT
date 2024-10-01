 //counts even numbers between two integers
int fun(int a, int b) {
  int c = 0;
 #pragma HLS LATENCY min=1 max=2
   for (int i = a; i < b; ++i) {
    if (i % 2 == 0) {
      c += 1;
    }
  }
  return c;
}
