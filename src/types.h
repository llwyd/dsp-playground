#include <stddef.h>
#include <stdint.h>
#include <assert.h>

typedef float float32_t;

_Static_assert( sizeof(float32_t) == 4U, "float32 not expected size" );
