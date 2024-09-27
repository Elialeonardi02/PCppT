#include <chrono>

// Type your code here, or load an example.
int square(long long num) {
    return num / 1000'000'000;
}

#include <iostream>
#include <time.h>
int main()
{
    auto yyy = std::chrono::system_clock::now();
    std::cout << (int64_t&)yyy;

}