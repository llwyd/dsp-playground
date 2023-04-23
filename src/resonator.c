#include "resonator.h"

extern void Resonator_Init(resonator_t * const r, const resonator_config_t * const config )
{
    assert( r != NULL );
    assert( config != NULL );
}

extern float32_t Resonator_NewSample( resonator_t * const r )
{
    assert( r != NULL );

    return 0.0f;
}
