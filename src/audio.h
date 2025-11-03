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
    snd_pcm_uframes_t offset;
}
audio_t;

extern void Audio_InitMono( audio_t * const driver);
extern snd_pcm_uframes_t Audio_GetMonoBuffer( audio_t * const driver, int32_t ** ptr );

extern void Audio_Close(audio_t * driver);
extern void Audio_HandleError();
extern void Audio_CommitSamples( audio_t * driver, snd_pcm_sframes_t frames );
extern snd_pcm_sframes_t Audio_GetStereoBuffers( float32_t ** left, float32_t ** right );
extern bool Audio_FramesAvailable( audio_t * driver );
extern audio_state_t Audio_GetState(void);

#endif /* AUDIO_H_ */
