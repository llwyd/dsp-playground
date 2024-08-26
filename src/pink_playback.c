#include "pink.h"
#include "random.h"
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>


int main(int argc, char ** argv)
{
    (void)argc;
    (void)argv;
    pink_t pink;
    Pink_Init(&pink);

    for(uint32_t idx = 0; idx < 48000; idx++)
    {
        printf("%u\n", Pink_Kick(&pink));
    }
}
