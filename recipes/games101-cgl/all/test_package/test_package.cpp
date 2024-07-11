#include <iostream>

#include <CGL/CGL.h>

int main() {
  CGL::Viewer viewer{};
  viewer.init();

  CGL::Vector2D vector{5, 4};
  std::cout << vector << '\n';
}