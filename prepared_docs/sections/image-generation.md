## Image Generation

#### `IMAGE_GENERATION_ENGINE`

- Type: `str`
- Options:
  - `openai` - Uses OpenAI DALL-E for image generation.
  - `comfyui` - Uses ComfyUI engine for image generation.
  - `automatic1111` - Uses AUTOMATIC1111 engine for image generation.
  - `gemini` - Uses Gemini for image generation.
- Default: `openai`
- Description: Specifies the engine to use for image generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_IMAGE_GENERATION`

- Type: `bool`
- Default: `False`
- Description: Enables or disables image generation features.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_IMAGE_PROMPT_GENERATION`

- Type: `bool`
- Default: `True`
- Description: Enables or disables image prompt generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE`

- Type: `str`
- Default: `None`
- Description: Specifies the template to use for generating image prompts.
- Persistence: This environment variable is a `PersistentConfig` variable.



#### `IMAGE_SIZE`

- Type: `str`
- Default: `512x512`
- Description: Sets the default image size to generate.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `IMAGE_STEPS`

- Type: `int`
- Default: `50`
- Description: Sets the default iteration steps for image generation. Used for ComfyUI and AUTOMATIC1111.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `IMAGE_GENERATION_MODEL`

- Type: `str`
- Description: Default model to use for image generation
- Persistence: This environment variable is a `PersistentConfig` variable.

### AUTOMATIC1111

#### `AUTOMATIC1111_BASE_URL`

- Type: `str`
- Description: Specifies the URL to AUTOMATIC1111's Stable Diffusion API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUTOMATIC1111_API_AUTH`

- Type: `str`
- Description: Sets the AUTOMATIC1111 API authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUTOMATIC1111_CFG_SCALE`

- Type: `float`
- Description: Sets the scale for AUTOMATIC1111 inference.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUTOMATIC1111_SAMPLER`

- Type: `str`
- Description: Sets the sampler for AUTOMATIC1111 inference.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUTOMATIC1111_SCHEDULER`

- Type: `str`
- Description: Sets the scheduler for AUTOMATIC1111 inference.
- Persistence: This environment variable is a `PersistentConfig` variable.

### ComfyUI

#### `COMFYUI_BASE_URL`

- Type: `str`
- Description: Specifies the URL to the ComfyUI image generation API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `COMFYUI_API_KEY`

- Type: `str`
- Description: Sets the API key for ComfyUI.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `COMFYUI_WORKFLOW`

- Type: `str`
- Default:

```
{
  "3": {
    "inputs": {
      "seed": 0,
      "steps": 20,
      "cfg": 8,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1,
      "model": [
        "4",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "5",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "model.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "5": {
    "inputs": {
      "width": 512,
      "height": 512,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "6": {
    "inputs": {
      "text": "Prompt",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "9": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  }
}
```

- Description: Sets the ComfyUI workflow.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Gemini

#### `GEMINI_API_BASE_URL`

- Type: `str`
- Default: `None`
- Description: Specifies the URL to Gemini's API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GEMINI_API_KEY`

- Type: `str`
- Default: `None`
- Description: Sets the Gemini API key.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `IMAGES_GEMINI_API_BASE_URL`

- Type: `str`
- Default: `None`
- Description: Specifies the URL to Gemini's image generation API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `IMAGES_GEMINI_API_KEY`

- Type: `str`
- Default: `None`
- Description: Sets the Gemini API key for image generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

### OpenAI DALL-E

#### `IMAGES_OPENAI_API_BASE_URL`

- Type: `str`
- Default: `${OPENAI_API_BASE_URL}`
- Description: Sets the OpenAI-compatible base URL to use for DALL-E image generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `IMAGES_OPENAI_API_KEY`

- Type: `str`
- Default: `${OPENAI_API_KEY}`
- Description: Sets the API key to use for DALL-E image generation.
- Persistence: This environment variable is a `PersistentConfig` variable.