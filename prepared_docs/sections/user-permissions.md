## User Permissions

### Chat Permissions

#### `USER_PERMISSIONS_CHAT_CONTROLS`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to access chat controls.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_FILE_UPLOAD`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to upload files to chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_DELETE`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to delete chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_EDIT`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to edit chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_STT`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to use Speech-to-Text in chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_TTS`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to use Text-to-Speech in chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_CALL`

- Type: `str`
- Default: `True`
- Description: Enables or disables user permission to make calls in chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_MULTIPLE_MODELS`

- Type: `str`
- Default: `True`
- Description: Enables or disables user permission to use multiple models in chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_TEMPORARY`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to create temporary chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_TEMPORARY_ENFORCED`

- Type: `str`
- Default: `False`
- Description: Enables or disables enforced temporary chats for users.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Feature Permissions

#### `USER_PERMISSIONS_FEATURES_DIRECT_TOOL_SERVERS`

- Type: `str`
- Default: `False`
- Description: Enables or disables user permission to access direct tool servers.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_FEATURES_WEB_SEARCH`

- Type: `str`
- Default: `True`
- Description: Enables or disables user permission to use the web search feature.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_FEATURES_IMAGE_GENERATION`

- Type: `str`
- Default: `True`
- Description: Enables or disables user permission to use the image generation feature.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_FEATURES_CODE_INTERPRETER`

- Type: `str`
- Default: `True`
- Description: Enables or disables user permission to use code interpreter feature.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Workspace Permissions

#### `USER_PERMISSIONS_WORKSPACE_MODELS_ACCESS`

- Type: `bool`
- Default: `False`
- Description: Enables or disables user permission to access workspace models.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_WORKSPACE_KNOWLEDGE_ACCESS`

- Type: `bool`
- Default: `False`
- Description: Enables or disables user permission to access workspace knowledge.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_WORKSPACE_PROMPTS_ACCESS`

- Type: `bool`
- Default: `False`
- Description: Enables or disables user permission to access workspace prompts.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_WORKSPACE_TOOLS_ACCESS`

- Type: `bool`
- Default: `False`
- Description: Enables or disables user permission to access workspace tools.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_WORKSPACE_MODELS_ALLOW_PUBLIC_SHARING`

- Type: `str`
- Default: `False`
- Description: Enables or disables public sharing of workspace models.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_WORKSPACE_KNOWLEDGE_ALLOW_PUBLIC_SHARING`

- Type: `str`
- Default: `False`
- Description: Enables or disables public sharing of workspace knowledge.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_WORKSPACE_PROMPTS_ALLOW_PUBLIC_SHARING`

- Type: `str`
- Default: `False`
- Description: Enables or disables public sharing of workspace prompts.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_WORKSPACE_TOOLS_ALLOW_PUBLIC_SHARING`

- Type: `str`
- Default: `False`
- Description: Enables or disables public sharing of workspace tools.
- Persistence: This environment variable is a `PersistentConfig` variable.