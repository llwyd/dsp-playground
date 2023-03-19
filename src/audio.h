#ifndef AUDIO_H_
#define AUDIO_H_

#include "alsa/asoundlib.h"
#include <stdint.h>
#include <stdbool.h>

extern void Audio_Init( uint32_t numChannels );
extern void Audio_Close(void);
extern uint32_t Audio_GenerateSineSample( float freq );
extern void Audio_CommitSamples( snd_pcm_uframes_t frames );
extern snd_pcm_uframes_t Audio_GetMonoBuffer( uint32_t ** ptr );
extern bool Audio_FramesAvailable( void );

#endif /* AUDIO_H_ */
