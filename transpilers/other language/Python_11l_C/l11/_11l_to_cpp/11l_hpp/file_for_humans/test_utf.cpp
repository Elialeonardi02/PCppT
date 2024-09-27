#include <iostream>
#include "utf.hpp"

int main()
{
    std::cout << u8"Рус\n";
    std::cout << utf::as_str8(u"Рус2\n");
    std::cout << utf::as_str8(U"Рус3\n");
}
