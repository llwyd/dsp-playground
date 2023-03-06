#include "audio.h"
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <stdbool.h>
#include <math.h>

#define FS ( 44100U ) /* Hz */
#define LATENCY ( 10000U ) /* us */
#define CHANNELS ( 1U )

#define ALSA_FUNC(X) \
{ \
    err = (X) ; \
    if( err < 0 ) \
    { \
        printf("Failed to open: %s\n", \
                snd_strerror(err)); \
        assert(false); \
    } \
} \

static snd_pcm_t * handle;
static snd_pcm_uframes_t offset;
static snd_pcm_uframes_t frames;
static snd_pcm_uframes_t size;

static uint32_t tone[FS];
static uint32_t *write_ptr = tone;

extern snd_pcm_uframes_t Audio_FramesToWrite( void )
{
    return snd_pcm_avail_update( handle );
}

extern void GenerateTone( void )
{
    const float fs = (float)FS;
    const float freq = 1000.f;
    const float T = 1.f / fs;

    for( int idx = 0; idx < FS; idx++ )
    {
        float x_f = sinf( 2 * M_PI * freq * T * (float)idx )+ 1.0f;
        tone[idx] = (uint32_t)( ( x_f / 2.0f )*( (float)(UINT32_MAX) ) );
    }
}

extern void Audio_GenerateSine( void )
{
    const snd_pcm_channel_area_t * areas;
    int err = snd_pcm_mmap_begin(handle, &areas, &offset, &frames);
    if( err < 0 )
    {
        printf("Failed to open: %s\n", 
                snd_strerror(err));
        assert(false);
    }

    uint32_t * ptr = (uint32_t *)areas[0].addr; /* Initial location */
    const uint32_t * const start = ptr;
    
    ptr += (areas[0].first);
    ptr += offset; 

    for( uint32_t idx = 0; idx < frames ; idx++ )
    {
        *ptr++ = *write_ptr++;
        if (write_ptr == &tone[FS-1] )
        {
            break;
        }
    }
    
    err = snd_pcm_mmap_commit(handle, offset, frames);
    if( err < 0 )
    {
        printf("Failed to open: %s\n", 
                snd_strerror(err));
        assert(false);
    }
}

extern void Audio_Loop( void )
{
    while( write_ptr != &tone[FS-1] )
    {
        frames = snd_pcm_avail_update( handle );
        if( frames > 0 )
        {
            printf("Frames: %lld\n", frames );
            Audio_GenerateSine();
        }
    }
}

extern void Audio_Init(void)
{
    GenerateTone();
    int err;
    ALSA_FUNC(snd_pcm_open( &handle,
                            "plughw:0,0",
                    SND_PCM_STREAM_PLAYBACK,
                    SND_PCM_NONBLOCK));

    ALSA_FUNC(snd_pcm_set_params( handle,
                        SND_PCM_FORMAT_U32_LE, 	        /* little endian*/
                        SND_PCM_ACCESS_MMAP_NONINTERLEAVED,	/* interleaved */
                        CHANNELS,				/* channels */
                        FS,				        /* sample rate */
                        2,				        /* alsa resampling */
                        LATENCY));			        /* desired latency */
    
    frames = snd_pcm_avail_update( handle );
    Audio_GenerateSine();

    ALSA_FUNC( snd_pcm_start( handle ) );
    snd_pcm_prepare( handle );
}

extern void Audio_Close(void)
{
    assert( handle != NULL );
    int err;
    ALSA_FUNC( snd_pcm_drain(handle) );
    ALSA_FUNC( snd_pcm_close(handle) );
}

