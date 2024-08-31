#include "pink.h"

_Static_assert(NUM_GENERATORS == 15U);

#define ROLLOVER (1 << (NUM_GENERATORS - 1))
#define DIV_SHIFT ( 4U )

union Integer{
    uint32_t u32;
    int32_t s32;
};

extern void Pink_Init(pink_t * const pink)
{
    random_t seed;
    pink->counter = 1U;
    pink->accumulator = 0U;
    pink->s_acc = 0;

    Random_Init(&seed);
    Random_SetSeed(&pink->white, Random_Next(&seed));
    Random_Init(&pink->white);

    pink->accumulator = (uint64_t)Random_Next(&pink->white);
    for(uint32_t idx = 0; idx < NUM_GENERATORS; idx++)
    {
        Random_SetSeed(&pink->generator[idx], Random_Next(&seed));
        Random_Init(&pink->generator[idx]);
        pink->accumulator += (uint64_t)Random_Next(&pink->generator[idx]);
    }
}

extern uint32_t Pink_Kick(pink_t * const pink)
{
    uint32_t index = __builtin_stdc_first_trailing_zero(pink->counter);

    pink->accumulator += Random_Next(&pink->generator[index]);
    pink->accumulator -= Random_Prev(&pink->generator[index]);

    pink->accumulator += Random_Next(&pink->white);
    pink->accumulator -= Random_Prev(&pink->white);
   
    pink->counter = (pink->counter & (ROLLOVER - 1) );
    pink->counter++;

    uint32_t next_pink = (uint32_t)(pink->accumulator >> DIV_SHIFT);
    return next_pink;
}


extern int32_t Pink_KickS32(pink_t * const pink)
{
    uint32_t index = __builtin_stdc_first_trailing_zero(pink->counter);

    union Integer rng;
    union Integer prv;  

    rng.u32 = Random_Next(&pink->generator[index]);
    prv.u32 = Random_Prev(&pink->generator[index]);

    pink->s_acc -= prv.s32;
    pink->s_acc += rng.s32;

    rng.u32 = Random_Next(&pink->white);
    prv.u32 = Random_Prev(&pink->white);
    
    pink->s_acc -= prv.s32;
    pink->s_acc += rng.s32;
   
    pink->counter = (pink->counter & (ROLLOVER - 1) );
    pink->counter++;

    int32_t next_pink = (int32_t)(pink->s_acc >> DIV_SHIFT);
    return next_pink;
}


