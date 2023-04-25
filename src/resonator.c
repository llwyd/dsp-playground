#include "resonator.h"
#include <math.h>

extern void Resonator_Init(resonator_t * const r, const resonator_config_t * const config )
{
    assert( r != NULL );
    assert( config != NULL );
    assert( config->amplitude <= 1.f );

    float32_t omega = (2.0f * M_PI * config->freq) / config->fs;

    float32_t b0 = config->amplitude * sinf(omega);
    r->a1 = -2.f * cosf(omega);
    r->a2 = 1.f;

    r->y[0] = ( 1.0 * b0 );
    r->y[1] = 0.f;
}

extern float32_t Resonator_NewSample( resonator_t * const r )
{
    assert( r != NULL );

    float32_t y = -(r->a1*r->y[0]) - (r->a2 * r->y[1] );

    r->y[1] = r->y[0];
    r->y[0] = y;

    return y;
}
