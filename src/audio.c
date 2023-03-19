#include "audio.h"
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <stdbool.h>
#include <math.h>

#define FS ( 44100U ) /* Hz */
#define LATENCY ( 10000U ) /* us */

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


static uint32_t channels;
static snd_pcm_t * handle;
static snd_pcm_uframes_t offset;
static snd_pcm_uframes_t size;
static const snd_pcm_channel_area_t * areas;

extern bool Audio_FramesAvailable( void )
{
    return( snd_pcm_avail_update( handle ) > 0 );
}

extern uint32_t Audio_GenerateSineSample( uint32_t * index, float freq )
{
    const float fs = (float)FS;
    const float T = 1.f / fs;
    
    double x_f = sin( 2 * M_PI * freq * T * (float)(*index) )+ 1.0f;
    
    (*index)++;
    return ((uint32_t)( ( x_f / 2.0f )*( (double)(UINT32_MAX) ) ));
}

extern snd_pcm_uframes_t Audio_GetMonoBuffer( uint32_t ** ptr )
{ 
    assert( channels == 1U );
    snd_pcm_uframes_t frames;
    ALSA_FUNC(snd_pcm_mmap_begin(handle, &areas, &offset, &frames));
    *ptr = (uint32_t *)areas[0U].addr; /* Initial location */

    assert( areas[0U].step == 32 );

    /* Add first offset (in bits ) */    
    *ptr += ( areas[0U].first >> 5U );

    /* Offset is in frames */
    *ptr += offset;
    
    return frames;
}

extern snd_pcm_uframes_t Audio_GetStereoBuffers( uint32_t ** left, uint32_t ** right )
{ 
    assert( channels == 2U );
    snd_pcm_uframes_t frames;
    ALSA_FUNC(snd_pcm_mmap_begin(handle, &areas, &offset, &frames));
    *left = (uint32_t *)areas[0U].addr; /* Initial location */
    *right = (uint32_t *)areas[1U].addr; /* Initial location */

    assert( areas[0U].step == 32 );
    assert( areas[1U].step == 32 );

    /* Add first offset (in bits ) */    
    *left += ( areas[0U].first >> 5U );
    *right += ( areas[1U].first >> 5U );

    /* Offset is in frames */
    *left += offset;
    *right += offset;
    
    return frames;
}

extern void Audio_CommitSamples( snd_pcm_uframes_t frames )
{
    ALSA_FUNC (snd_pcm_mmap_commit(handle, offset, frames) );
}

extern void Audio_Init( uint32_t numChannels )
{
    assert( numChannels > 0 );
    assert( numChannels <= 2 );

    channels = numChannels;
    ALSA_FUNC(snd_pcm_open( &handle,
                            "plughw:1,0",
                            SND_PCM_STREAM_PLAYBACK,
                            SND_PCM_NONBLOCK));

    ALSA_FUNC(snd_pcm_set_params( handle,
                        SND_PCM_FORMAT_U32_LE, 	            /* little endian*/
                        SND_PCM_ACCESS_MMAP_NONINTERLEAVED,	/* interleaved */
                        channels,				            /* channels */
                        FS,				                    /* sample rate */
                        0,				                    /* alsa resampling */
                        LATENCY));			                /* desired latency */
    
    assert( Audio_FramesAvailable() );
    snd_pcm_uframes_t frames; 
    if( channels == 1U )
    {
        uint32_t * buffer;
        frames = Audio_GetMonoBuffer( &buffer );
        for( uint32_t idx = 0; idx < frames; idx++ )
        {
            *buffer++ = 0U;
        }
    }
    else if( channels == 2U )
    {
        uint32_t * left, * right;
        frames = Audio_GetStereoBuffers(&left, &right );
        for( uint32_t idx = 0; idx < frames; idx++ )
        {
            *left++ = 0U;
            *right++ = 0U;
        }
    }
    else
    {
        assert( false );
    }

    Audio_CommitSamples(frames);
    ALSA_FUNC( snd_pcm_start( handle ) );
}

extern void Audio_Close(void)
{
    assert( handle != NULL );
    ALSA_FUNC( snd_pcm_drop(handle) );
    ALSA_FUNC( snd_pcm_close(handle) );
}

