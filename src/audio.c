#include "audio.h"
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <stdbool.h>

#define FS ( 44100U ) /* Hz */
#define LATENCY ( 10000U ) /* us */
#define CHANNELS ( 1U )

static snd_pcm_t * handle;
static snd_pcm_uframes_t offset;
static snd_pcm_uframes_t frames;
static snd_pcm_uframes_t size;

extern void Audio_Init(void)
{
    int err = snd_pcm_open( &handle,
                            "plughw:0,0",
                    SND_PCM_STREAM_PLAYBACK,
                    SND_PCM_NONBLOCK);

    if( err < 0 )
    {
        printf("Failed to open: %s\n", 
                snd_strerror(err));
        assert(false);
    }
    snd_pcm_set_params( handle,
                        SND_PCM_FORMAT_U32_LE, 	        /* little endian*/
                        SND_PCM_ACCESS_MMAP_NONINTERLEAVED,	/* interleaved */
                        CHANNELS,				/* channels */
                        FS,				        /* sample rate */
                        2,				        /* alsa resampling */
                        LATENCY);			        /* desired latency */
}

extern void Audio_Close(void)
{
    assert( handle != NULL );
    snd_pcm_drain(handle);
    snd_pcm_close(handle);
}

