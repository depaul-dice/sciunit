cmake_minimum_required(VERSION 3.1.3)
project(sciunit2-deps NONE)

include(ExternalProject)

set_directory_properties(PROPERTIES EP_BASE build)

ExternalProject_Add(
  ptu
  GIT_REPOSITORY "git@bitbucket.org:depauldbgroup/provenance-to-use.git"
  CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
  INSTALL_COMMAND install -s <BINARY_DIR>/ptu ${CMAKE_BINARY_DIR}/build/
)

ExternalProject_Add(
  scripter
  GIT_REPOSITORY "git@bitbucket.org:geotrust/scripter.git"
  CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
  INSTALL_COMMAND install -s <BINARY_DIR>/scripter ${CMAKE_BINARY_DIR}/build/
)

ExternalProject_Add(
  vvpkg
  GIT_REPOSITORY "git@bitbucket.org:depauldbgroup/vvpkg.git"
  CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
  INSTALL_COMMAND install -s <BINARY_DIR>/demo/vv ${CMAKE_BINARY_DIR}/build/
  TEST_COMMAND <BINARY_DIR>/tests/run
)
