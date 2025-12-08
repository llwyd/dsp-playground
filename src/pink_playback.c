#include "audio.h"
#include "pink.h"
#include "random.h"
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>


union Audio
{
    uint32_t u32;
    int32_t s32;
};


int main(int argc, char ** argv)
{
    (void)argc;
    (void)argv;
    audio_t audio_driver;
    
    pink_t pink;
    Pink_Init(&pink);
    Audio_InitMono(&audio_driver);

    for(uint32_t idx = 0; idx < (48000 * 5); idx++)
    {
        while(!Audio_FramesAvailable(&audio_driver));
        int32_t * buffer;
        snd_pcm_uframes_t frames = Audio_GetMonoBuffer( &audio_driver, &buffer );
    
        for( uint32_t jdx = 0; jdx < frames; jdx++, idx++ )
        {
            //uint32_t p = 0x80000000 - Pink_Kick(&pink);
            *buffer++ = Pink_KickS32(&pink);
        }
    
        Audio_CommitSamples(&audio_driver, frames);
    }
    Audio_Close(&audio_driver);
}
