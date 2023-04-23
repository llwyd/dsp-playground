cmake_minimum_required(VERSION 3.2)

project( dsp )

set (CMAKE_C_STANDARD 11 )
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY bin/ )
set (CMAKE_BUILD_TYPE Debug )

add_executable( playback.out
                src/simple_playback.c
                src/audio.c
                src/audio.h )

add_executable( stereo_playback.out
                src/simple_stereo_playback.c
                src/audio.c
                src/audio.h )


add_executable( audio_sm.out
                src/audio_sm.c
                src/audio.c
                src/audio.h 
                src/resonator.c
                src/resonator.h
                src/types.h)

target_link_libraries( playback.out asound)
target_link_libraries( playback.out m)

target_link_libraries( stereo_playback.out asound)
target_link_libraries( stereo_playback.out m)

target_link_libraries( audio_sm.out asound)
target_link_libraries( audio_sm.out m)
