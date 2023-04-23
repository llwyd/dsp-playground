#include "audio.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <signal.h>
#include <time.h>
#include "resonator.h"

static void StopAudio(int sig)
{
    signal(sig, SIG_IGN);
    printf("\b\bClosing ALSA Interface\n");
    Audio_Close();
    printf("FIN\n");
    exit(0);
}

void ComputeNextSamples( void )
{
    static uint32_t left_idx = 0U;
    static uint32_t right_idx = 0U;
    
    uint32_t * left, * right;
    snd_pcm_uframes_t frames = Audio_GetStereoBuffers( &left, &right );
    for( uint32_t idx = 0; idx < frames; idx++ )
    {
        left[idx] = Audio_GenerateSineSample( &left_idx, 1000.0f );
        right[idx] = Audio_GenerateSineSample( &right_idx, 10000.0f );
    }
    Audio_CommitSamples( frames );
}

void SuperLoop( void )
{
    switch( Audio_GetState() )
    {
        case AUDIOSTATE_NEWFRAMES:
        {
            /* Produce new samples */
            ComputeNextSamples();
            break;
        }
        case AUDIOSTATE_ERROR:
        {
            /* Handle Error */
            Audio_HandleError();
            Audio_Close();
            break;
        }
        case AUDIOSTATE_IDLE:
        {
            struct timespec delay;
            delay.tv_sec = 0;
            delay.tv_nsec = 5000000;
            
            nanosleep( &delay, NULL );
            break;
        } 
        case AUDIOSTATE_COUNT:
        default:
        {
            assert(false);
            break;
        }

    }
}

int main( int argc, char ** argv )
{
    Audio_Init(2U);
    signal(SIGINT, StopAudio);

    while(1)
    {
        SuperLoop();
    }

    return 0;
}

