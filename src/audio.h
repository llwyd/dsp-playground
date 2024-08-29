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

typedef struct
{
    uint32_t channels;
    snd_pcm_t * handle;
    const snd_pcm_channel_area_t * areas;
}
audio_t;

extern void Audio_InitMono( audio_t * const driver);
extern snd_pcm_uframes_t Audio_GetMonoBuffer( audio_t * const driver, uint32_t ** ptr );

extern void Audio_Close(void);
extern void Audio_HandleError();
extern void Audio_CommitSamples( snd_pcm_uframes_t frames );
extern snd_pcm_uframes_t Audio_GetStereoBuffers( float32_t ** left, float32_t ** right );
extern bool Audio_FramesAvailable( void );
extern audio_state_t Audio_GetState(void);

#endif /* AUDIO_H_ */
