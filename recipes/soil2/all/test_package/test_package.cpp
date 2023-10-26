#include <iostream>

#include <soil2/SOIL2.h>

auto main() -> int {
  return SOIL_version() == 1300 ? 0 : 1;
}