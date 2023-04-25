#include "audio.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <signal.h>
#include <time.h>
#include "resonator.h"

static resonator_t left_tone;
static resonator_t right_tone;

static void StopAudio(int sig)
{
    signal(sig, SIG_IGN);
    printf("\b\bClosing ALSA Interface\n");
    Audio_Close();
    printf("FIN\n");
    exit(0);
}

static void Delay(void)
{
    struct timespec delay;
    delay.tv_sec = 0;
    delay.tv_nsec = 5000000;
          
    nanosleep( &delay, NULL );
}

static void ComputeNextSamples( void )
{
    static uint32_t left_idx = 0U;
    static uint32_t right_idx = 0U;
    
    float32_t * left, * right;
    snd_pcm_uframes_t frames = Audio_GetStereoBuffers( &left, &right );
    for( uint32_t idx = 0; idx < frames; idx++ )
    {
        left[idx] = Resonator_NewSample( &left_tone );
        right[idx] = Resonator_NewSample( &right_tone );
    }
    Audio_CommitSamples( frames );
}

void SuperLoop( void )
{
    switch( Audio_GetState() )
    {
        case AUDIOSTATE_NEWFRAMES:
        {
            ComputeNextSamples();
            break;
        }
        case AUDIOSTATE_ERROR:
        {
            Audio_HandleError();
            Audio_Close();
            break;
        }
        case AUDIOSTATE_IDLE:
        {
            Delay();
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

static void Init(void)
{
    resonator_config_t left_config =
    {
        .freq = 1000.f,
        .fs = 44100.f,
        .amplitude = .95f,
    };
    
    resonator_config_t right_config =
    {
        .freq = 10000.f,
        .fs = 44100.f,
        .amplitude = .95f,
    };

    Resonator_Init( &left_tone, &left_config);
    Resonator_Init( &right_tone, &right_config);

    Audio_Init(2U);
    signal(SIGINT, StopAudio);
}

int main( int argc, char ** argv )
{
    Init();
    while(1)
    {
        SuperLoop();
    }

    return 0;
}

