#include "audio.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <signal.h>

static void StopAudio(int sig)
{
    signal(sig, SIG_IGN);
    printf("\b\bClosing ALSA Interface\n");
    Audio_Close();
    printf("FIN\n");
    exit(0);
}

int main( int argc, char ** argv )
{
    Audio_Init(2U);
    signal(SIGINT, StopAudio);

    uint32_t left_idx = 0U;
    uint32_t right_idx = 0U;

    while(1)
    {
        if( Audio_FramesAvailable() )
        {
            uint32_t * left, * right;
            snd_pcm_uframes_t frames = Audio_GetStereoBuffers( &left, &right );
            for( uint32_t idx = 0; idx < frames; idx++ )
            {
                left[idx] = Audio_GenerateSineSample( &left_idx, 1000.0f );
                right[idx] = Audio_GenerateSineSample( &right_idx, 10000.0f );
            }
            Audio_CommitSamples( frames );
        } 
    }
    return 0;
}
