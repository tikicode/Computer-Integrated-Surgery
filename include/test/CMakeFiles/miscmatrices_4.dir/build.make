# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.24

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/Cellar/cmake/3.24.2/bin/cmake

# The command to remove a file.
RM = /usr/local/Cellar/cmake/3.24.2/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include"

# Include any dependencies generated for this target.
include test/CMakeFiles/miscmatrices_4.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include test/CMakeFiles/miscmatrices_4.dir/compiler_depend.make

# Include the progress variables for this target.
include test/CMakeFiles/miscmatrices_4.dir/progress.make

# Include the compile flags for this target's objects.
include test/CMakeFiles/miscmatrices_4.dir/flags.make

test/CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.o: test/CMakeFiles/miscmatrices_4.dir/flags.make
test/CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.o: /Users/avnukala/Desktop/CIS\ I\ /Computer-Integrated-Surgery/include/Eigen3/test/miscmatrices.cpp
test/CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.o: test/CMakeFiles/miscmatrices_4.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object test/CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.o"
	cd "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/test" && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT test/CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.o -MF CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.o.d -o CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.o -c "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/test/miscmatrices.cpp"

test/CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.i"
	cd "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/test" && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/test/miscmatrices.cpp" > CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.i

test/CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.s"
	cd "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/test" && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/test/miscmatrices.cpp" -o CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.s

# Object files for target miscmatrices_4
miscmatrices_4_OBJECTS = \
"CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.o"

# External object files for target miscmatrices_4
miscmatrices_4_EXTERNAL_OBJECTS =

test/miscmatrices_4: test/CMakeFiles/miscmatrices_4.dir/miscmatrices.cpp.o
test/miscmatrices_4: test/CMakeFiles/miscmatrices_4.dir/build.make
test/miscmatrices_4: test/CMakeFiles/miscmatrices_4.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir="/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable miscmatrices_4"
	cd "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/test" && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/miscmatrices_4.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
test/CMakeFiles/miscmatrices_4.dir/build: test/miscmatrices_4
.PHONY : test/CMakeFiles/miscmatrices_4.dir/build

test/CMakeFiles/miscmatrices_4.dir/clean:
	cd "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/test" && $(CMAKE_COMMAND) -P CMakeFiles/miscmatrices_4.dir/cmake_clean.cmake
.PHONY : test/CMakeFiles/miscmatrices_4.dir/clean

test/CMakeFiles/miscmatrices_4.dir/depend:
	cd "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include" && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3" "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/Eigen3/test" "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include" "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/test" "/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/include/test/CMakeFiles/miscmatrices_4.dir/DependInfo.cmake" --color=$(COLOR)
.PHONY : test/CMakeFiles/miscmatrices_4.dir/depend

