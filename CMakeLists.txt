cmake_minimum_required(VERSION 3.24.4)
project(HexGen VERSION 1.0)

set(SOURCES
    src/Main.cpp
    src/HexGen.cpp
    src/Stl.cpp
    src/Mesh.cpp
)

set(HEADERS
    src/HexGen.h
    src/Stl.h
    src/Initialization.h
    src/Mesh.h
    src/StaticVars.h
)

add_executable(HexGen ${SOURCES} ${HEADERS})
target_include_directories(HexGen PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)
