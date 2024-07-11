cmake_minimum_required(VERSION 3.21)
project(test_package)

message("building test_package for conan2")

find_package(games101-cgl CONFIG REQUIRED)

add_executable(test_package)
target_sources(test_package
  PRIVATE
  test_package.cpp
)
target_link_libraries(test_package
  PRIVATE
  games101-cgl::games101-cgl
)
target_compile_features(test_package
  PRIVATE
  cxx_std_11
)