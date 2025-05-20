## App/Backend

The following environment variables are used by `backend/open_webui/config.py` to provide Open WebUI startup
configuration. Please note that some variables may have different default values depending on
whether you're running Open WebUI directly or via Docker. For more information on logging
environment variables, see our [logging documentation](https://docs.openwebui.com/getting-started/advanced-topics/logging).

### General

#### `WEBUI_URL`

- Type: `str`
- Default: `http://localhost:3000`
- Description: Specifies the URL where the Open WebUI is reachable. Currently used for search engine support.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_SIGNUP`

- Type: `bool`
- Default: `True`
- Description: Toggles user account creation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_LOGIN_FORM`

- Type: `bool`
- Default: `True`
- Description: Toggles email, password, sign-in and "or" (only when `ENABLE_OAUTH_SIGNUP` is set to True) elements.
- Persistence: This environment variable is a `PersistentConfig` variable.

:::danger

This should **only** ever be set to `False` when [ENABLE_OAUTH_SIGNUP](https://docs.openwebui.com/getting-started/env-configuration/#enable_oauth_signup)
is also being used and set to `True`. Failure to do so will result in the inability to login.

:::

#### `DEFAULT_LOCALE`

- Type: `str`
- Default: `en`
- Description: Sets the default locale for the application.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `DEFAULT_MODELS`

- Type: `str`
- Default: Empty string (' '), since `None`.
- Description: Sets a default Language Model.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `DEFAULT_USER_ROLE`

- Type: `str`
- Options:
  - `pending` - New users are pending until their accounts are manually activated by an admin.
  - `user` - New users are automatically activated with regular user permissions.
  - `admin` - New users are automatically activated with administrator permissions.
- Default: `pending`
- Description: Sets the default role assigned to new users.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `PENDING_USER_OVERLAY_TITLE`

- Type: `str`
- Default: Empty string (' ')
- Description: Sets a custom title for the pending user overlay.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `PENDING_USER_OVERLAY_CONTENT`

- Type: `str`
- Default: Empty string (' ')
- Description: Sets a custom text content for the pending user overlay.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_CHANNELS`

- Type: `bool`
- Default: `False`
- Description: Enables or disables channel support.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `WEBHOOK_URL`

- Type: `str`
- Description: Sets a webhook for integration with Discord/Slack/Microsoft Teams.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_ADMIN_EXPORT`

- Type: `bool`
- Default: `True`
- Description: Controls whether admin users can export data.

#### `ENABLE_ADMIN_CHAT_ACCESS`

- Type: `bool`
- Default: `True`
- Description: Enables admin users to access all chats.

#### `ENABLE_USER_WEBHOOKS`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user webhooks.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RESPONSE_WATERMARK`

- Type: `str`
- Default: Empty string (' ')
- Description: Sets a custom text that will be included when you copy a message in the chat. E.g. `"This text is AI generated"` -> will add "This text is AI generated" to every message, when copied.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `THREAD_POOL_SIZE`

- Type: `int`
- Default: `0`
- Description: Sets the thread pool size for FastAPI/AnyIO blocking calls. By default (when set to 0) FastAPI/AnyIO use `40` threads. In case of large instances and many concurrent users, it may be needed to increase `THREAD_POOL_SIZE` to prevent blocking.

#### `SHOW_ADMIN_DETAILS`

- Type: `bool`
- Default: `True`
- Description: Toggles whether to show admin user details in the interface.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ADMIN_EMAIL`

- Type: `str`
- Description: Sets the admin email shown by `SHOW_ADMIN_DETAILS`
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENV`

- Type: `str`
- Options:
  - `dev` - Enables the FastAPI API documentation on `/docs`
  - `prod` - Automatically configures several environment variables
- Default:
  - **Backend Default**: `dev`
  - **Docker Default**: `prod`
- Description: Environment setting.

#### `ENABLE_PERSISTENT_CONFIG`

- Type: `bool`
- Default: `True`
- Description: If set to `False`, all `PersistentConfig` variables are treated as regular variables.

#### `CUSTOM_NAME`

- Type: `str`
- Description: Sets `WEBUI_NAME` but polls **api.openwebui.com** for metadata.

#### `WEBUI_NAME`

- Type: `str`
- Default: `Open WebUI`
- Description: Sets the main WebUI name. Appends `(Open WebUI)` if overridden.

#### `PORT`

- Type: `int`
- Default: `8080`
- Description: Sets the port to run Open WebUI from.

:::info
If you're running the application via Python and using the `open-webui serve` command, you cannot set the port using the `PORT` configuration. Instead, you must specify it directly as a command-line argument using the `--port` flag. For example:

```bash
open-webui serve --port 9999
```

This will run the Open WebUI on port `9999`. The `PORT` environment variable is disregarded in this mode.
:::

#### `ENABLE_REALTIME_CHAT_SAVE`

- Type: `bool`
- Default: `False`
- Description: When enabled, the system saves each chunk of streamed chat data to the database in real time to ensure maximum data persistency. This feature provides robust data recovery and allows accurate session tracking. However, the tradeoff is increased latency, as saving to the database introduces a delay. Disabling this feature can improve performance and reduce delays, but it risks potential data loss in the event of a system failure or crash. Use based on your application's requirements and acceptable tradeoffs.

#### `BYPASS_MODEL_ACCESS_CONTROL`

- Type: `bool`
- Default: `False`
- Description: Bypasses model access control.

#### `WEBUI_BUILD_HASH`

- Type: `str`
- Default: `dev-build`
- Description: Used for identifying the Git SHA of the build for releases.

#### `WEBUI_BANNERS`

- Type: `list` of `dict`
- Default: `[]`
- Description: List of banners to show to users. The format for banners are:

```json
[{"id": "string", "type": "string [info, success, warning, error]", "title": "string", "content": "string", "dismissible": false, "timestamp": 1000}]
```

- Persistence: This environment variable is a `PersistentConfig` variable.

:::info

When setting this environment variable in a `.env` file, make sure to escape the quotes by wrapping the entire value in double quotes and using escaped quotes (`\"`) for the inner quotes. Example:

```
WEBUI_BANNERS="[{\"id\": \"1\", \"type\": \"warning\", \"title\": \"Your messages are stored.\", \"content\": \"Your messages are stored and may be reviewed by human people. LLM's are prone to hallucinations, check sources.\", \"dismissible\": true, \"timestamp\": 1000}]"
```

:::

#### `USE_CUDA_DOCKER`

- Type: `bool`
- Default: `False`
- Description: Builds the Docker image with NVIDIA CUDA support. Enables GPU acceleration for local Whisper and embeddings.

#### `EXTERNAL_PWA_MANIFEST_URL`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: When defined as a fully qualified URL (e.g., https://path/to/manifest.webmanifest), requests sent to /manifest.json will use the external manifest file. When not defined, the default manifest.json file will be used.

#### `ENABLE_TITLE_GENERATION`

- Type: `bool`
- Default: `True`
- Description: Enables or disables chat title generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LICENSE_KEY`

- Type: `str`
- Default: `None`
- Description: Specifies the license key to use (for Enterprise users only).
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `SSL_ASSERT_FINGERPRINT`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the SSL assert fingerprint to use.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `DEFAULT_PROMPT_SUGGESTIONS`

- Type: `list` of `dict`
- Default: `[]` (which means to use the built-in default prompt suggestions)
- Description: List of prompt suggestions. The format for prompt suggestions are:

```json
[{"title": ["Title part 1", "Title part 2"], "content": "prompt"}]
```

### AIOHTTP Client

#### `AIOHTTP_CLIENT_TIMEOUT`

- Type: `int`
- Default: `300`
- Description: Specifies the timeout duration in seconds for the AIOHTTP client. This impacts things
such as connections to Ollama and OpenAI endpoints.

:::info

This is the maximum amount of time the client will wait for a response before timing out.
If set to an empty string (' '), the timeout will be set to `None`, effectively disabling the timeout and
allowing the client to wait indefinitely.

:::

#### `AIOHTTP_CLIENT_TIMEOUT_MODEL_LIST`

- Type: `int`
- Default: `10`
- Description: Sets the timeout in seconds for fetching the model list. This can be useful in cases where network latency requires a longer timeout duration to successfully retrieve the model list.

:::note
The AIOHTTP_CLIENT_TIMEOUT_MODEL_LIST is set to 10 seconds by default to help ensure that all necessary connections are available when opening the web UI. This duration allows enough time for retrieving the model list even in cases of higher network latency. You can lower this value if quicker timeouts are preferred, but keep in mind that doing so may lead to some connections being dropped, depending on your network conditions.
:::

#### `AIOHTTP_CLIENT_TIMEOUT_OPENAI_MODEL_LIST`

- Type: `int`
- Description: Sets the timeout in seconds for fetching the model list. This can be useful in cases where network latency requires a longer timeout duration to successfully retrieve the model list.

### Directories

#### `DATA_DIR`

- Type: `str`
- Default: `./data`
- Description: Specifies the base directory for data storage, including uploads, cache, vector database, etc.

#### `FONTS_DIR`

- Type: `str`
- Description: Specifies the directory for fonts.

#### `FRONTEND_BUILD_DIR`

- Type: `str`
- Default: `../build`
- Description: Specifies the location of the built frontend files.

#### `STATIC_DIR`

- Type: `str`
- Default: `./static`
- Description: Specifies the directory for static files, such as the favicon.

### Ollama

#### `ENABLE_OLLAMA_API`

- Type: `bool`
- Default: `True`
- Description: Enables the use of Ollama APIs.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OLLAMA_BASE_URL` (`OLLAMA_API_BASE_URL` is deprecated) {#ollama_base_url}

- Type: `str`
- Default: `http://localhost:11434`
- Docker Default:
  - If `K8S_FLAG` is set: `http://ollama-service.open-webui.svc.cluster.local:11434`
  - If `USE_OLLAMA_DOCKER=True`: `http://localhost:11434`
  - Else `http://host.docker.internal:11434`
- Description: Configures the Ollama backend URL.

#### `OLLAMA_BASE_URLS`

- Type: `str`
- Description: Configures load-balanced Ollama backend hosts, separated by `;`. See
[`OLLAMA_BASE_URL`](#ollama_base_url). Takes precedence over[`OLLAMA_BASE_URL`](#ollama_base_url).
- Example: `http://host-one:11434;http://host-two:11434`
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USE_OLLAMA_DOCKER`

- Type: `bool`
- Default: `False`
- Description: Builds the Docker image with a bundled Ollama instance.

#### `K8S_FLAG`

- Type: `bool`
- Default: `False`
- Description: If set, assumes Helm chart deployment and sets [`OLLAMA_BASE_URL`](#ollama_base_url) to `http://ollama-service.open-webui.svc.cluster.local:11434`

### OpenAI

#### `ENABLE_OPENAI_API`

- Type: `bool`
- Default: `True`
- Description: Enables the use of OpenAI APIs.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OPENAI_API_BASE_URL`

- Type: `str`
- Default: `https://api.openai.com/v1`
- Description: Configures the OpenAI base API URL.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OPENAI_API_BASE_URLS`

- Type: `str`
- Description: Supports balanced OpenAI base API URLs, semicolon-separated.
- Example: `http://host-one:11434;http://host-two:11434`
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OPENAI_API_KEY`

- Type: `str`
- Description: Sets the OpenAI API key.
- Example: `sk-124781258123`
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OPENAI_API_KEYS`

- Type: `str`
- Description: Supports multiple OpenAI API keys, semicolon-separated.
- Example: `sk-124781258123;sk-4389759834759834`
- Persistence: This environment variable is a `PersistentConfig` variable.

### Tasks

#### `TASK_MODEL`

- Type: `str`
- Description: The default model to use for tasks such as title and web search query generation
when using Ollama models.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `TASK_MODEL_EXTERNAL`

- Type: `str`
- Description: The default model to use for tasks such as title and web search query generation
when using OpenAI-compatible endpoints.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `TITLE_GENERATION_PROMPT_TEMPLATE`

- Type: `str`
- Description: Prompt to use when generating chat titles.
- Default: The value of `DEFAULT_TITLE_GENERATION_PROMPT_TEMPLATE` environment variable.



- Persistence: This environment variable is a `PersistentConfig` variable.

#### `TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE`

- Type: `str`
- Description: Prompt to use when calling tools.
- Default: The value of `DEFAULT_TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE` environment variable.



- Persistence: This environment variable is a `PersistentConfig` variable.

### Code Execution

#### `ENABLE_CODE_EXECUTION`

- Type: `bool`
- Default: `True`
- Description: Enables or disables code execution.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_EXECUTION_ENGINE`

- Type: `str`
- Default: `pyodide`
- Description: Specifies the code execution engine to use.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_EXECUTION_JUPYTER_URL`

- Type: `str`
- Default: `None`
- Description: Specifies the Jupyter URL to use for code execution.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_EXECUTION_JUPYTER_AUTH`

- Type: `str`
- Default: `None`
- Description: Specifies the Jupyter authentication method to use for code execution.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_EXECUTION_JUPYTER_AUTH_TOKEN`

- Type: `str`
- Default: `None`
- Description: Specifies the Jupyter authentication token to use for code execution.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_EXECUTION_JUPYTER_AUTH_PASSWORD`

- Type: `str`
- Default: `None`
- Description: Specifies the Jupyter authentication password to use for code execution.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_EXECUTION_JUPYTER_TIMEOUT`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the timeout for Jupyter code execution.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Code Interpreter

#### `ENABLE_CODE_INTERPRETER`

- Type: `bool`
- Default: `True`
- Description: Enables or disables code interpreter.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_INTERPRETER_ENGINE`

- Type: `str`
- Default: `pyodide`
- Description: Specifies the code interpreter engine to use.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_INTERPRETER_PROMPT_TEMPLATE`

- Type: `str`
- Default: `None`
- Description: Specifies the prompt template to use for code interpreter.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_INTERPRETER_JUPYTER_URL`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the Jupyter URL to use for code interpreter.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_INTERPRETER_JUPYTER_AUTH`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the Jupyter authentication method to use for code interpreter.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_INTERPRETER_JUPYTER_AUTH_TOKEN`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the Jupyter authentication token to use for code interpreter.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the Jupyter authentication password to use for code interpreter.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_INTERPRETER_JUPYTER_TIMEOUT`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the timeout for the Jupyter code interpreter.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Direct Connections (OpenAPI/MCPO Tool Servers)

#### `ENABLE_DIRECT_CONNECTIONS`

- Type: `bool`
- Default: `True`
- Description: Enables or disables direct connections.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Autocomplete

#### `ENABLE_AUTOCOMPLETE_GENERATION`

- Type: `bool`
- Default: `True`
- Description: Enables or disables autocomplete generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

:::info

When enabling `ENABLE_AUTOCOMPLETE_GENERATION`, ensure that you also configure `AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH` and `AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE` accordingly.

:::

#### `AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH`

- Type: `int`
- Default: `-1`
- Description: Sets the maximum input length for autocomplete generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE`

- Type: `str`
- Default: The value of the `DEFAULT_AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE` environment variable.



- Description: Sets the prompt template for autocomplete generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Evaluation Arena Model

#### `ENABLE_EVALUATION_ARENA_MODELS`

- Type: `bool`
- Default: `True`
- Description: Enables or disables evaluation arena models.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_MESSAGE_RATING`

- Type: `bool`
- Default: `True`
- Description: Enables message rating feature.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_COMMUNITY_SHARING`

- Type: `bool`
- Default: `True`
- Description: Controls whether users are shown the share to community button.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Tags Generation

#### `ENABLE_TAGS_GENERATION`

- Type: `bool`
- Default: `True`
- Description: Enables or disables tag generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `TAGS_GENERATION_PROMPT_TEMPLATE`

- Type: `str`
- Default: The value of `DEFAULT_TAGS_GENERATION_PROMPT_TEMPLATE` environment variable.



- Description: Sets the prompt template for tag generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

### API Key Endpoint Restrictions

#### `ENABLE_API_KEY`

- Type: `bool`
- Default: `True`
- Description: Enables API key authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_API_KEY_ENDPOINT_RESTRICTIONS`

- Type: `bool`
- Default: `False`
- Description: Enables API key endpoint restrictions for added security and configurability.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `API_KEY_ALLOWED_ENDPOINTS`

- Type: `str`
- Description: Specifies a comma-separated list of allowed API endpoints when API key endpoint restrictions are enabled.
- Persistence: This environment variable is a `PersistentConfig` variable.

:::note

The value of `API_KEY_ALLOWED_ENDPOINTS` should be a comma-separated list of endpoint URLs, such as `/api/v1/messages, /api/v1/channels`.

:::

#### `JWT_EXPIRES_IN`

- Type: `int`
- Default: `-1`
- Description: Sets the JWT expiration time in seconds. Valid time units: `s`, `m`, `h`, `d`, `w` or `-1` for no expiration.
- Persistence: This environment variable is a `PersistentConfig` variable.