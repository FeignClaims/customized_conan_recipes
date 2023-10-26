#include <cassert>
#include <ranges>
#include <tuple>

#include <boost/mp.hpp>

int main(int argc, char const**) {
  namespace mp = boost::mp;
  using mp::operator""_c;

  auto slice = [](auto list, auto begin, auto end) {
    using mp::operator|;
    return list | std::views::drop(begin)  // use std.ranges
           | std::views::take(end - 1_c);  // any library which can operate on containers is supported!
  };

  assert((slice(std::tuple{1, argc, 3, 4}, 1_c, 3_c) == std::tuple{argc, 3}));
}