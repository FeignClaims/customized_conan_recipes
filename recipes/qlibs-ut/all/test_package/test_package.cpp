#define UT_COMPILE_TIME_ONLY
#include <ut>
using namespace ut;

[[nodiscard]] constexpr auto sum(auto... args) -> auto {
  return (... + args);
}

static_assert(("sum"_test = [] {  // compile-time only
  expect(sum(1, 2, 3) == 6_i);
}));

int main() {}