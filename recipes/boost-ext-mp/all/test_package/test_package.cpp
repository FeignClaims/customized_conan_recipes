#include <array>
#include <reflect>
#include <type_traits>

template <auto N, class... Ts>
using at_c = mp::type_of<std::array{mp::meta<Ts>...}[N]>;

static_assert(std::is_same_v<int, at_c<0, int, bool, float>>);
static_assert(std::is_same_v<bool, at_c<1, int, bool, float>>);
static_assert(std::is_same_v<float, at_c<2, int, bool, float>>);