#include "audio.h"
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <stdbool.h>
#include <math.h>
#include "types.h"

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
static snd_pcm_sframes_t error;
static const snd_pcm_channel_area_t * areas;

static audio_state_t state = AUDIOSTATE_IDLE;

static void StopAudio(int sig)
{
    signal(sig, SIG_IGN);
    //Audio_Close();
    exit(0);
}

extern bool Audio_FramesAvailable( audio_t * driver )
{
    return( snd_pcm_avail_update( driver->handle ) > 0 );
}

extern void Audio_HandleError( void )
{
    printf("ALSA error!: %s\n", snd_strerror(error));
}

extern audio_state_t Audio_GetState(void)
{
    assert( handle != NULL );
    const snd_pcm_sframes_t frames =snd_pcm_avail_update( handle );
    
    if( frames > 0 )
    {
        state = AUDIOSTATE_NEWFRAMES;
    }
    else if( frames < 0 )
    {
        state = AUDIOSTATE_ERROR;
        error = frames;
    }
    else
    {
        state = AUDIOSTATE_IDLE;
    }
    return state;
}


extern snd_pcm_uframes_t Audio_GetMonoBuffer( audio_t * const driver, int32_t ** ptr )
{ 
    assert( driver->handle != NULL );
    assert( driver->channels == 1U );
    
    snd_pcm_uframes_t frames;
    ALSA_FUNC(snd_pcm_mmap_begin(driver->handle, &driver->areas, &driver->offset, &frames));
    *ptr = (int32_t *)driver->areas[0U].addr; /* Initial location */

    assert( driver->areas[0U].step == 32 );

    /* Add first offset (in bits ) */    
    *ptr += ( driver->areas[0U].first >> 5U );

    /* Offset is in frames */
    *ptr += driver->offset;
    
    return frames;
}

extern snd_pcm_sframes_t Audio_GetStereoBuffers( float32_t ** left, float32_t ** right )
{ 
    assert( handle != NULL );
    assert( channels == 2U );
    snd_pcm_uframes_t frames;
    ALSA_FUNC(snd_pcm_mmap_begin(handle, &areas, &offset, &frames));
    *left = (float32_t *)areas[0U].addr; /* Initial location */
    *right = (float32_t *)areas[1U].addr; /* Initial location */

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

extern void Audio_CommitSamples( audio_t * driver, snd_pcm_sframes_t frames )
{
    assert( driver != NULL );
    assert( driver->handle != NULL );
    ALSA_FUNC (snd_pcm_mmap_commit(driver->handle, driver->offset, frames) );
}

extern void Audio_InitMono(audio_t * const driver)
{
    assert( driver != NULL );

    driver->channels = 1U;
    
    signal(SIGINT, StopAudio);
    
    ALSA_FUNC(snd_pcm_open( &driver->handle,
                            "default",
                            SND_PCM_STREAM_PLAYBACK,
                            SND_PCM_NONBLOCK));

    ALSA_FUNC(snd_pcm_set_params( driver->handle,
                        SND_PCM_FORMAT_S32_LE, 	        /* little endian*/
                        SND_PCM_ACCESS_MMAP_NONINTERLEAVED,	/* interleaved */
                        driver->channels,				            /* channels */
                        FS,				                    /* sample rate */
                        0,				                    /* alsa resampling */
                        LATENCY));			                /* desired latency */
    
    assert( Audio_FramesAvailable(driver) );
    snd_pcm_uframes_t frames; 

    int32_t * buffer;
    frames = Audio_GetMonoBuffer( driver, &buffer );
    for( uint32_t idx = 0; idx < frames; idx++ )
    {
        *buffer++ = 0U;
    }

    Audio_CommitSamples(driver, frames);
    ALSA_FUNC( snd_pcm_start( driver->handle ) );
}

extern void Audio_Close(audio_t * driver)
{
    assert( driver->handle != NULL );
    ALSA_FUNC( snd_pcm_drop(driver->handle) );
    ALSA_FUNC( snd_pcm_close(driver->handle) );
}

