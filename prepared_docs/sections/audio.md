## Audio

### Whisper Speech-to-Text (Local)

#### `WHISPER_MODEL`

- Type: `str`
- Default: `base`
- Description: Sets the Whisper model to use for Speech-to-Text. The backend used is faster_whisper with quantization to `int8`.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `WHISPER_MODEL_DIR`

- Type: `str`
- Default: `${DATA_DIR}/cache/whisper/models`
- Description: Specifies the directory to store Whisper model files.

#### `WHISPER_VAD_FILTER`

- Type: `bool`
- Default: `False`
- Description: Specifies whether to apply a Voice Activity Detection (VAD) filter to Whisper Speech-to-Text.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `WHISPER_MODEL_AUTO_UPDATE`

- Type: `bool`
- Default: `False`
- Description: Toggles automatic update of the Whisper model.

#### `WHISPER_LANGUAGE`

- Type: `str`
- Default: `None`
- Description: Specifies the ISO 639-1 language Whisper uses for STT (ISO 639-2 for Hawaiian and Cantonese). Whisper predicts the language by default.

### Speech-to-Text (OpenAI)

#### `AUDIO_STT_ENGINE`

- Type: `str`
- Options:
  - Leave empty to use the built-in local Whisper engine for Speech-to-Text.
  - `openai` - Uses OpenAI engine for Speech-to-Text.
  - `deepgram`- Uses Deepgram engine for Speech-to-Text.
  - `azure` Uses Azure engine for Speech-to-Text.
- Description: Specifies the Speech-to-Text engine to use.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUDIO_STT_MODEL`

- Type: `str`
- Default: `whisper-1`
- Description: Specifies the Speech-to-Text model to use for OpenAI-compatible endpoints.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUDIO_STT_OPENAI_API_BASE_URL`

- Type: `str`
- Default: `${OPENAI_API_BASE_URL}`
- Description: Sets the OpenAI-compatible base URL to use for Speech-to-Text.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUDIO_STT_OPENAI_API_KEY`

- Type: `str`
- Default: `${OPENAI_API_KEY}`
- Description: Sets the OpenAI API key to use for Speech-to-Text.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Speech-to-Text (Azure)

#### `AUDIO_STT_AZURE_API_KEY`

- Type: `str`
- Default: `None`
- Description: Specifies the Azure API key to use for Speech-to-Text.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUDIO_STT_AZURE_REGION`

- Type: `str`
- Default: `None`
- Description: Specifies the Azure region to use for Speech-to-Text.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUDIO_STT_AZURE_LOCALES`

- Type: `str`
- Default: `None`
- Description: Specifies the locales to use for Azure Speech-to-Text.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Speech-to-Text (Deepgram)

#### `DEEPGRAM_API_KEY`

- Type: `str`
- Default: `None`
- Description: Specifies the Deepgram API key to use for Speech-to-Text.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Text-to-Speech

#### `AUDIO_TTS_API_KEY`

- Type: `str`
- Description: Sets the API key for Text-to-Speech.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUDIO_TTS_ENGINE`

- Type: `str`
- Options:
  - Leave empty to use the built-in WebAPI engine for Text-to-Speech.
  - `azure` - Uses Azure engine for Text-to-Speech.
  - `elevenlabs` - Uses ElevenLabs engine for Text-to-Speech
  - `openai` - Uses OpenAI engine for Text-to-Speech.
  - `transformers` - Uses SentenceTransformers for Text-to-Speech.
- Description: Specifies the Text-to-Speech engine to use.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUDIO_TTS_MODEL`

- Type: `str`
- Default: `tts-1`
- Description: Specifies the OpenAI text-to-speech model to use.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUDIO_TTS_VOICE`

- Type: `str`
- Default: `alloy`
- Description: Sets the OpenAI text-to-speech voice to use.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUDIO_TTS_SPLIT_ON`

- Type: `str`
- Default: `punctuation`
- Description: Sets the OpenAI text-to-speech split on to use.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Azure Text-to-Speech

#### `AUDIO_TTS_AZURE_SPEECH_REGION`

- Type: `str`
- Description: Sets the region for Azure Text to Speech.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUDIO_TTS_AZURE_SPEECH_OUTPUT_FORMAT`

- Type: `str`
- Description: Sets the output format for Azure Text to Speech.
- Persistence: This environment variable is a `PersistentConfig` variable.

### OpenAI Text-to-Speech

#### `AUDIO_TTS_OPENAI_API_BASE_URL`

- Type: `str`
- Default: `${OPENAI_API_BASE_URL}`
- Description: Sets the OpenAI-compatible base URL to use for text-to-speech.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUDIO_TTS_OPENAI_API_KEY`

- Type: `str`
- Default: `${OPENAI_API_KEY}`
- Description: Sets the API key to use for text-to-speech.
- Persistence: This environment variable is a `PersistentConfig` variable.