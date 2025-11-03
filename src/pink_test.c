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
    
    pink_t pink;
    Pink_Init(&pink);

    for(uint32_t idx = 0; idx < (48000); idx++)
    {
    
        int32_t p = Pink_KickS32(&pink);
        printf("%d\n", p);
    }
}
