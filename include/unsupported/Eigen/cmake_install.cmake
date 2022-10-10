# Install script for directory: /Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/Library/Developer/CommandLineTools/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Devel" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/eigen3/unsupported/Eigen" TYPE FILE FILES
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/AdolcForward"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/AlignedVector3"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/ArpackSupport"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/AutoDiff"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/BVH"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/EulerAngles"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/FFT"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/IterativeSolvers"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/KroneckerProduct"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/LevenbergMarquardt"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/MatrixFunctions"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/MoreVectorization"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/MPRealSupport"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/NonLinearOptimization"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/NumericalDiff"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/OpenGLSupport"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/Polynomials"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/Skyline"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/SparseExtra"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/SpecialFunctions"
    "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/Splines"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Devel" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/eigen3/unsupported/Eigen" TYPE DIRECTORY FILES "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/unsupported/Eigen/src" FILES_MATCHING REGEX "/[^/]*\\.h$")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/unsupported/Eigen/CXX11/cmake_install.cmake")

endif()

