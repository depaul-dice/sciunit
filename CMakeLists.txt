cmake_minimum_required(VERSION 3.1.3)
project(sciunit2-deps NONE)

include(ExternalProject)

set_directory_properties(PROPERTIES EP_BASE build)
set(_LIBEXEC_DIR ${CMAKE_BINARY_DIR}/sciunit2/libexec)

ExternalProject_Add(
  ptu
  GIT_REPOSITORY "git@bitbucket.org:depauldbgroup/provenance-to-use.git"
  CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
  INSTALL_COMMAND install -Ds <BINARY_DIR>/ptu ${_LIBEXEC_DIR}/ptu
)

ExternalProject_Add(
  scripter
  GIT_REPOSITORY "git@bitbucket.org:geotrust/scripter.git"
  CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
  INSTALL_COMMAND install -Ds <BINARY_DIR>/scripter ${_LIBEXEC_DIR}/scripter
)

ExternalProject_Add(
  vvpkg
  GIT_REPOSITORY "git@bitbucket.org:depauldbgroup/vvpkg.git"
  CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
  INSTALL_COMMAND install -Ds <BINARY_DIR>/demo/vv ${_LIBEXEC_DIR}/vv
  TEST_COMMAND <BINARY_DIR>/tests/run
)
