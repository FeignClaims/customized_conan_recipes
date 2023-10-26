cmake_minimum_required(VERSION 3.1)
project(test_package)

message("building test_package for conan2")

find_package(cppfront REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp2)