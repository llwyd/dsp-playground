#include "audio.h"

static snd_pcm_t * handle;
static snd_pcm_uframes_t offset;
static snd_pcm_uframes_t frames;
static snd_pcm_uframes_t size;

extern void Audio_Init(void)
{

}
