#!/bin/sh

if [ ! bin/ ]; then
    mkdir bin
fi

cmake . -DCMAKE_C_COMPILER=gcc-15
cmake --build .

