## Security Variables

#### `ENABLE_FORWARD_USER_INFO_HEADERS`

- type: `bool`
- Default: `False`
- Description: Forwards user information (name, ID, email, and role) as X-headers to OpenAI API and Ollama API.
If enabled, the following headers are forwarded:
  - `X-OpenWebUI-User-Name`
  - `X-OpenWebUI-User-Id`
  - `X-OpenWebUI-User-Email`
  - `X-OpenWebUI-User-Role`

#### `ENABLE_WEB_LOADER_SSL_VERIFICATION`

- Type: `bool`
- Default: `True`
- Description: Bypass SSL Verification for RAG on Websites.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `WEBUI_SESSION_COOKIE_SAME_SITE`

- Type: `str`
- Options:
  - `lax` - Sets the `SameSite` attribute to lax, allowing session cookies to be sent with
requests initiated by third-party websites.
  - `strict` - Sets the `SameSite` attribute to strict, blocking session cookies from being sent
with requests initiated by third-party websites.
  - `none` - Sets the `SameSite` attribute to none, allowing session cookies to be sent with
requests initiated by third-party websites, but only over HTTPS.
- Default: `lax`
- Description: Sets the `SameSite` attribute for session cookies.

:::warning

When `ENABLE_OAUTH_SIGNUP` is enabled, setting `WEBUI_SESSION_COOKIE_SAME_SITE` to `strict` can cause login failures. This is because Open WebUI uses a session cookie to validate the callback from the OAuth provider, which helps prevent CSRF attacks.

However, a `strict` session cookie is not sent with the callback request, leading to potential login issues. If you experience this problem, use the default `lax` value instead.

:::

#### `WEBUI_SESSION_COOKIE_SECURE`

- Type: `bool`
- Default: `False`
- Description: Sets the `Secure` attribute for session cookies if set to `True`.

#### `WEBUI_AUTH_COOKIE_SAME_SITE`

- Type: `str`
- Options:
  - `lax` - Sets the `SameSite` attribute to lax, allowing auth cookies to be sent with
requests initiated by third-party websites.
  - `strict` - Sets the `SameSite` attribute to strict, blocking auth cookies from being sent
with requests initiated by third-party websites.
  - `none` - Sets the `SameSite` attribute to none, allowing auth cookies to be sent with
requests initiated by third-party websites, but only over HTTPS.
- Default: `lax`
- Description: Sets the `SameSite` attribute for auth cookies.

:::info

If the value is not set, `WEBUI_SESSION_COOKIE_SAME_SITE` will be used as a fallback.

:::

#### `WEBUI_AUTH_COOKIE_SECURE`

- Type: `bool`
- Default: `False`
- Description: Sets the `Secure` attribute for auth cookies if set to `True`.

:::info

If the value is not set, `WEBUI_SESSION_COOKIE_SECURE` will be used as a fallback.

:::

#### `WEBUI_AUTH`

- Type: `bool`
- Default: `True`
- Description: This setting enables or disables authentication.

:::danger

If set to `False`, authentication will be disabled for your Open WebUI instance. However, it's
important to note that turning off authentication is only possible for fresh installations without
any existing users. If there are already users registered, you cannot disable authentication
directly. Ensure that no users are present in the database if you intend to turn off `WEBUI_AUTH`.

:::

#### `WEBUI_SECRET_KEY`

- Type: `str`
- Default: `t0p-s3cr3t`
- Docker Default: Randomly generated on first start
- Description: Overrides the randomly generated string used for JSON Web Token.

:::info

When deploying Open-WebUI in a multiple-node cluster with a load balancer, you must ensure that the WEBUI_SECRET_KEY value is the same across all instances in order to enable users to continue working if a node is recycled or their session is transferred to a different node. Without it, they will need to sign in again each time the underlying node changes.

:::

#### `OFFLINE_MODE`

- Type: `bool`
- Default: `False`
- Description: Enables or disables offline mode.

#### `RESET_CONFIG_ON_START`

- Type: `bool`
- Default: `False`
- Description: Resets the `config.json` file on startup.

#### `SAFE_MODE`

- Type: `bool`
- Default: `False`
- Description: Enables safe mode, which disables potentially unsafe features, deactivating all functions.

#### `CORS_ALLOW_ORIGIN`

- Type: `str`
- Default: `*`
- Description: Sets the allowed origins for Cross-Origin Resource Sharing (CORS).

#### `RAG_EMBEDDING_MODEL_TRUST_REMOTE_CODE`

- Type: `bool`
- Default: `False`
- Description: Determines whether to allow custom models defined on the Hub in their own modeling files.

#### `RAG_RERANKING_MODEL_TRUST_REMOTE_CODE`

- Type: `bool`
- Default: `False`
- Description: Determines whether to allow custom models defined on the Hub in their own.
modeling files for reranking.

#### `RAG_EMBEDDING_MODEL_AUTO_UPDATE`

- Type: `bool`
- Default: `True`
- Description: Toggles automatic update of the Sentence-Transformer model.

#### `RAG_RERANKING_MODEL_AUTO_UPDATE`

- Type: `bool`
- Default: `True`
- Description: Toggles automatic update of the reranking model.