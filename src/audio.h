#ifndef AUDIO_H_
#define AUDIO_H_

#include "alsa/asoundlib.h"
#include <stdint.h>

extern void Audio_Init(void);
extern void Audio_Close(void);
extern uint32_t * Audio_GetChannelBuffer( uint32_t index );
extern uint32_t Audio_GenerateSineSample( float freq );
extern snd_pcm_uframes_t * Audio_FramesToWrite( void );
extern void Audio_CommitSamples( void );

#endif /* AUDIO_H_ */
