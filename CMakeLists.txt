cmake_minimum_required(VERSION 3.2)

project( dsp )

set (CMAKE_C_STANDARD 11 )
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY bin/ )
set (CMAKE_BUILD_TYPE Debug )

add_executable( playback.out
                src/audio_playback.c
                src/audio.c
                src/audio.h )

target_link_libraries( playback.out asound)
