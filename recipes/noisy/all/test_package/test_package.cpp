#include <noisy.h>

vz::Noisy make_noisy() {
  return {};
}

int main() {
  vz::Noisy x = vz::Noisy(make_noisy());
}