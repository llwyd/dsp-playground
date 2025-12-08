#ifndef PINK_H_
#define PINK_H_

#include "random.h"
#include <stdbool.h>
#include <stdint.h>

#define NUM_GENERATORS (15U)

typedef struct
{
    uint64_t accumulator;
    int64_t s_acc;
    random_t white;
    random_t generator[NUM_GENERATORS];
    uint32_t counter;
    uint32_t rollover;
}
pink_t;

extern void Pink_Init(pink_t * const pink);
extern uint32_t Pink_Kick(pink_t * const pink);
extern int32_t Pink_KickS32(pink_t * const pink);

#endif /* PINK_H_ */
