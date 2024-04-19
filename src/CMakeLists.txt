cmake_minimum_required(VERSION 3.25)
project(TSPPH_PerformanceAnalysis C)

set(CMAKE_C_STANDARD 11)

if(WIN32)
    add_compile_options(-Wall)
else(WIN32)
    add_compile_options(-Wall -Wextra)
endif(WIN32)

find_package(Git QUIET)
if(GIT_FOUND AND EXISTS "${PROJECT_SOURCE_DIR}/../.git")
# Update submodules as needed
    option(GIT_SUBMODULE "Check submodules during build" ON)
    if(GIT_SUBMODULE)
        message(STATUS "Submodule update")
        execute_process(COMMAND ${GIT_EXECUTABLE} submodule update --init --recursive --remote
                        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/..
                        RESULT_VARIABLE GIT_SUBMOD_RESULT)
        if(NOT GIT_SUBMOD_RESULT EQUAL "0")
            message(FATAL_ERROR "git submodule update --init --recursive --remote failed with ${GIT_SUBMOD_RESULT}, please checkout submodules")
        endif()
    endif()
endif()

if(NOT EXISTS "${PROJECT_SOURCE_DIR}/../TSPPartitionHeuristic/CMakeLists.txt")
    message(FATAL_ERROR "The submodules were not downloaded! GIT_SUBMODULE was turned off or failed. Please update submodules and try again.")
endif()

add_subdirectory(../TSPPartitionHeuristic TSPPartitionHeuristic)

add_executable(ExecutionTimeScript
                running_scripts/execution_time_script.c
                solvers/highsSolver.c)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}")
find_package(HIGHS REQUIRED)

target_include_directories(ExecutionTimeScript 
                PRIVATE ${HIGHS_INCLUDE_DIR}
                PRIVATE ${PROJECT_SOURCE_DIR}/../TSPPartitionHeuristic/src/model)

    if(${HIGHS_INCLUDE_DIR} PATH_EQUAL ${HIGHS_SOURCE_DIR}/HiGHS/src)
        find_path(HIGHS_INCLUDE_BUILD HConfig.h
        PATHS
        ${HIGHS_SOURCE_DIR}/HiGHS/build
        )
        target_include_directories(ExecutionTimeScript
                PRIVATE ${HIGHS_INCLUDE_BUILD})
    endif (${HIGHS_INCLUDE_DIR} PATH_EQUAL ${HIGHS_SOURCE_DIR}/HiGHS/src)
   
target_link_libraries(ExecutionTimeScript TSPPartitionHeuristic ${HIGHS_LIBRARIES} m)
                