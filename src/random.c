#include "random.h"

#define MAGIC_SEED (0x12345678)

static uint32_t XORShift(uint32_t x)
{
    /* Xorshift */
    x ^= x << 13;
	x ^= x >> 17;
	x ^= x << 5;

    return x;
}

extern void Random_Init(random_t * const rng)
{
    if(rng->seed == 0U)
    {
        rng->seed = MAGIC_SEED;
        rng->prev = MAGIC_SEED;
        rng->seed = XORShift(rng->seed);
    }
    else
    {
        rng->prev = rng->seed;
        rng->seed = XORShift(rng->seed);
    }
}

extern uint32_t Random_Prev(random_t * const rng)
{
    return rng->prev;
}

extern uint32_t Random_Next(random_t * const rng)
{
    rng->prev = rng->seed;
    rng->seed = XORShift(rng->seed);
    return rng->seed;
}

extern void Random_SetSeed(random_t* const rng, uint32_t seed)
{
    rng->seed = seed;
}

