#include "types.h"


typedef struct
{
    float32_t a1;
    float32_t a2;
    float32_t b0;
    float32_t storage[2];
}
resonator_t;

typedef struct
{
    float32_t freq;
    float32_t fs;
    float32_t amplitude;
}
resonator_config_t;

extern void Resonator_Init(resonator_t * const r, const resonator_config_t * const config );
extern float32_t Resonator_NewSample( resonator_t * const r );

