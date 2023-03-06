#include "audio.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


int main( int argc, char ** argv )
{
    printf("Audio Playback\n");
    Audio_Init();

    //int32_t frames = Audio_FramesToWrite();


    //printf("Frames: %lld\n",frames);
    Audio_Loop();
    Audio_Close();
    return 0;
}
