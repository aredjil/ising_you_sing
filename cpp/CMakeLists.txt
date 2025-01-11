# Minimum CMake version required
cmake_minimum_required(VERSION 3.10)

# Project name
project(IsingModel)
find_package(OpenMP REQUIRED)
# Set the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# Add the executable target
add_executable(IsingModel main.cpp)

target_link_libraries(IsingModel PRIVATE OpenMP::OpenMP_CXX)
set(ENV{OMP_NUM_THREADS} 8)
# Include the header files directory
target_include_directories(IsingModel PRIVATE ${CMAKE_SOURCE_DIR}/include)