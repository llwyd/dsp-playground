cmake_minimum_required(VERSION 3.2)

project( dsp )

set (CMAKE_C_STANDARD 11 )
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY bin/ )

add_executable( playback.out
                src/audio_playback.c )
