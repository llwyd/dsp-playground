#ifndef AUDIO_H_
#define AUDIO_H_

#include "alsa/asoundlib.h"
#include <stdint.h>
#include <stdbool.h>
#include "types.h"

typedef enum
{
    AUDIOSTATE_IDLE,
    AUDIOSTATE_NEWFRAMES,
    AUDIOSTATE_ERROR,

    AUDIOSTATE_COUNT,
}
audio_state_t;

extern void Audio_Init( uint32_t numChannels );
extern void Audio_Close(void);
extern void Audio_HandleError();
extern void Audio_CommitSamples( snd_pcm_uframes_t frames );
extern snd_pcm_uframes_t Audio_GetMonoBuffer( float32_t ** ptr );
extern snd_pcm_uframes_t Audio_GetStereoBuffers( float32_t ** left, float32_t ** right );
extern bool Audio_FramesAvailable( void );
extern audio_state_t Audio_GetState(void);

#endif /* AUDIO_H_ */
