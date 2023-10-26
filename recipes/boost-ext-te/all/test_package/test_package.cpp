#include <iostream>

#include <boost/te.hpp>
namespace te = boost::te;

// Define interface of something which is drawable
struct Drawable {
  void draw(std::ostream& out) const {
    te::call([](auto const& self, auto& out) { self.draw(out); }, *this, out);
  }
};

// Define implementation which is drawable (No inheritance)
struct Square {
  void draw(std::ostream& out) const {
    out << "Square";
  }
};

// Define other implementation which is drawable (No inheritance)
struct Circle {
  void draw(std::ostream& out) const {
    out << "Circle";
  }
};

// Define object which can hold drawable objects
void draw(te::poly<Drawable> const& drawable) {
  drawable.draw(std::cout);
}

int main() {
  // Call draw polymorphically (Value semantics / Small Buffer Optimization)
  draw(Circle{});  // prints Circle
  draw(Square{});  // prints Square
}