cmake_minimum_required(VERSION 3.24.4)
project(HexGen VERSION 1.0)

set(SOURCES
    Main.cpp
    HexGen.cpp
    HexGen.h
    Stl.cpp
    Stl.h
    Initialization.h
    Mesh.cpp
    Mesh.h
    StaticVars.h
)

add_executable(HexGen ${SOURCES})

