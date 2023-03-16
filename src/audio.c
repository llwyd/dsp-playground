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
    int err = (X) ; \
    if( err < 0 ) \
    { \
        printf("ALSA error!: %s\n", \
                snd_strerror(err)); \
        assert(false); \
    } \
} \

static snd_pcm_t * handle;
static snd_pcm_uframes_t offset;
static snd_pcm_uframes_t frames;
static snd_pcm_uframes_t size;
static const snd_pcm_channel_area_t * areas;

static uint32_t * ptr;

extern snd_pcm_uframes_t * Audio_FramesToWrite( void )
{
    frames = snd_pcm_avail_update( handle );
    return &frames;
}

extern uint32_t Audio_GenerateSineSample( float freq )
{
    static int idx = 0;
    const float fs = (float)FS;
    const float T = 1.f / fs;
    
    double x_f = sin( 2 * M_PI * freq * T * (float)idx )+ 1.0f;
    
    idx++;
    return ((uint32_t)( ( x_f / 2.0f )*( (double)(UINT32_MAX) ) ));
}

extern uint32_t * Audio_GetChannelBuffer( uint32_t index )
{
    assert( index < CHANNELS );
    
    ALSA_FUNC(snd_pcm_mmap_begin(handle, &areas, &offset, &frames));
    ptr = (uint32_t *)areas[index].addr; /* Initial location */

    assert( areas[index].step == 32 );

    /* Add first offset (in bits ) */    
    ptr += ( areas[index].first >> 5U );

    /* Offset is in frames */
    ptr += offset;
    
    return ptr;
}

extern void Audio_CommitSamples( void )
{
    ALSA_FUNC (snd_pcm_mmap_commit(handle, offset, frames) );
}

extern void Audio_Init(void)
{
    ALSA_FUNC(snd_pcm_open( &handle,
                            "plughw:1,0",
                    SND_PCM_STREAM_PLAYBACK,
                    SND_PCM_NONBLOCK));

    ALSA_FUNC(snd_pcm_set_params( handle,
                        SND_PCM_FORMAT_U32_LE, 	        /* little endian*/
                        SND_PCM_ACCESS_MMAP_NONINTERLEAVED,	/* interleaved */
                        CHANNELS,				/* channels */
                        FS,				        /* sample rate */
                        2,				        /* alsa resampling */
                        LATENCY));			        /* desired latency */
    
    (void)Audio_FramesToWrite();
    (void)Audio_GetChannelBuffer( 0 );
    for( uint32_t idx = 0; idx < frames; idx++ )
    {
        *ptr++ = 0U;
    }
    Audio_CommitSamples();
    ALSA_FUNC( snd_pcm_start( handle ) );
}

extern void Audio_Close(void)
{
    assert( handle != NULL );
    ALSA_FUNC( snd_pcm_drop(handle) );
    ALSA_FUNC( snd_pcm_close(handle) );
}

