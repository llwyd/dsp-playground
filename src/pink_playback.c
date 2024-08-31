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
    //audio_t audio_driver;
    
    pink_t pink;
    Pink_Init(&pink);
//    Audio_InitMono(&audio_driver);

    for(uint32_t idx = 0; idx < 48000; idx++)
    {
        //union Audio audio;
//        audio.u32 = Pink_Kick(&pink);
//        audio.u32 = 0x80000000 - audio.u32;

//        printf("%d\n", audio.s32);
//
        printf("%d\n", Pink_KickS32(&pink));
    }
}
