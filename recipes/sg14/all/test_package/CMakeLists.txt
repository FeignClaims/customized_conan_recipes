cmake_minimum_required(VERSION 3.21)
project(test_package)

message("building test_package for conan2")

find_package(sg14 CONFIG REQUIRED)

add_executable(test_package)
target_sources(test_package
  PRIVATE
  test_package.cpp
)
target_link_libraries(test_package
  PRIVATE
  sg14::sg14
)
target_compile_features(test_package
  PRIVATE
  cxx_std_14
)