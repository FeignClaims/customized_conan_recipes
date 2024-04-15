#include <ut2>

[[nodiscard]] constexpr auto sum(auto... args) -> auto {
  return (... + args);
}

int main() {
  using namespace ut;
  "sum"_test = [] {
    expect(sum(1, 2, 3) == 6_i);
  };
}