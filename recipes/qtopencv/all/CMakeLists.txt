cmake_minimum_required(VERSION 3.12)
project(qtopencv LANGUAGES CXX)

find_package(Qt6 CONFIG REQUIRED)
find_package(OpenCV CONFIG REQUIRED)

add_library(${PROJECT_NAME})
target_sources(${PROJECT_NAME}
  PRIVATE
  ${QTOPENCV_SRC_DIR}/cvmatandqimage.cpp
)
target_link_libraries(${PROJECT_NAME}
  PRIVATE
  qt::qt
  opencv::opencv
)
target_compile_features(${PROJECT_NAME}
  PRIVATE
  cxx_std_20
)

include(GNUInstallDirs)
install(TARGETS ${PROJECT_NAME}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
install(FILES ${QTOPENCV_SRC_DIR}/cvmatandqimage.h TYPE INCLUDE)