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
    Audio_Init();
    signal(SIGINT, StopAudio);

    while(1)
    {
        snd_pcm_uframes_t * frames = Audio_FramesToWrite();
        if( frames > 0 )
        {
            uint32_t * ptr = Audio_GetChannelBuffer( 0 );
            for( uint32_t idx = 0; idx < *frames; idx++ )
            {
                ptr[idx] = Audio_GenerateSineSample( 1000.0f );
            }
            Audio_CommitSamples();
        } 
    }
    return 0;
}
