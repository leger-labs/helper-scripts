## OAuth

#### `ENABLE_OAUTH_SIGNUP`

- Type: `bool`
- Default: `False`
- Description: Enables account creation when signing up via OAuth. Distinct from `ENABLE_SIGNUP`.
- Persistence: This environment variable is a `PersistentConfig` variable.

:::danger

`ENABLE_LOGIN_FORM` must be set to `False` when `ENABLE_OAUTH_SIGNUP` is set to `True`. Failure to do so will result in the inability to login.

:::

#### `OAUTH_MERGE_ACCOUNTS_BY_EMAIL`

- Type: `bool`
- Default: `False`
- Description: If enabled, merges OAuth accounts with existing accounts using the same email
address. This is considered unsafe as not all OAuth providers will verify email addresses and can lead to potential account takeovers.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_UPDATE_PICTURE_ON_LOGIN`

- Type: `bool`
- Default: `False`
- Description: If enabled, updates the local user profile picture with the OAuth-provided picture on login.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `WEBUI_AUTH_TRUSTED_EMAIL_HEADER`

- Type: `str`
- Description: Defines the trusted request header for authentication. See [SSO docs](/features/sso).

#### `WEBUI_AUTH_TRUSTED_NAME_HEADER`

- Type: `str`
- Description: Defines the trusted request header for the username of anyone registering with the
`WEBUI_AUTH_TRUSTED_EMAIL_HEADER` header. See [SSO docs](/features/sso).

### Google

See https://support.google.com/cloud/answer/6158849?hl=en

#### `GOOGLE_CLIENT_ID`

- Type: `str`
- Description: Sets the client ID for Google OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GOOGLE_CLIENT_SECRET`

- Type: `str`
- Description: Sets the client secret for Google OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GOOGLE_OAUTH_SCOPE`

- Type: `str`
- Default: `openid email profile`
- Description: Sets the scope for Google OAuth authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GOOGLE_REDIRECT_URI`

- Type: `str`
- Default: `<backend>/oauth/google/callback`
- Description: Sets the redirect URI for Google OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Microsoft

See https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app

#### `MICROSOFT_CLIENT_ID`

- Type: `str`
- Description: Sets the client ID for Microsoft OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MICROSOFT_CLIENT_SECRET`

- Type: `str`
- Description: Sets the client secret for Microsoft OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MICROSOFT_CLIENT_TENANT_ID`

- Type: `str`
- Description: Sets the tenant ID for Microsoft OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MICROSOFT_OAUTH_SCOPE`

- Type: `str`
- Default: `openid email profile`
- Description: Sets the scope for Microsoft OAuth authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MICROSOFT_REDIRECT_URI`

- Type: `str`
- Default: `<backend>/oauth/microsoft/callback`
- Description: Sets the redirect URI for Microsoft OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

### GitHub

See https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps

#### `GITHUB_CLIENT_ID`

- Type: `str`
- Description: Sets the client ID for GitHub OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GITHUB_CLIENT_SECRET`

- Type: `str`
- Description: Sets the client secret for GitHub OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GITHUB_CLIENT_SCOPE`

- Type: `str`
- Default: `user:email`
- Description: Specifies the scope for GitHub OAuth authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GITHUB_CLIENT_REDIRECT_URI`

- Type: `str`
- Default: `<backend>/oauth/github/callback`
- Description: Sets the redirect URI for GitHub OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

### OpenID (OIDC)

#### `OAUTH_CLIENT_ID`

- Type: `str`
- Description: Sets the client ID for OIDC.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_CLIENT_SECRET`

- Type: `str`
- Description: Sets the client secret for OIDC.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OPENID_PROVIDER_URL`

- Type: `str`
- Description: Path to the `.well-known/openid-configuration` endpoint
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OPENID_REDIRECT_URI`

- Type: `str`
- Default: `<backend>/oauth/oidc/callback`
- Description: Sets the redirect URI for OIDC
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_SCOPES`

- Type: `str`
- Default: `openid email profile`
- Description: Sets the scope for OIDC authentication. `openid` and `email` are required.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_CODE_CHALLENGE_METHOD`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the code challenge method for OAuth authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_PROVIDER_NAME`

- Type: `str`
- Default: `SSO`
- Description: Sets the name for the OIDC provider.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_USERNAME_CLAIM`

- Type: `str`
- Default: `name`
- Description: Set username claim for OpenID.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_EMAIL_CLAIM`

- Type: `str`
- Default: `email`
- Description: Set email claim for OpenID.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_PICTURE_CLAIM`

- Type: `str`
- Default: `picture`
- Description: Set picture (avatar) claim for OpenID.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_GROUP_CLAIM`

- Type: `str`
- Default: `groups`
- Description: Specifies the group claim for OAuth authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_OAUTH_ROLE_MANAGEMENT`

- Type: `bool`
- Default: `False`
- Description: Enables role management for OAuth delegation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_OAUTH_GROUP_MANAGEMENT`

- Type: `bool`
- Default: `False`
- Description: Enables or disables OAuth group management.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_ROLES_CLAIM`

- Type: `str`
- Default: `roles`
- Description: Sets the roles claim to look for in the OIDC token.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_ALLOWED_ROLES`

- Type: `str`
- Default: `user,admin`
- Description: Sets the roles that are allowed access to the platform.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_ADMIN_ROLES`

- Type: `str`
- Default: `admin`
- Description: Sets the roles that are considered administrators.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_ALLOWED_DOMAINS`

- Type: `str`
- Default: `*`
- Description: Specifies the allowed domains for OAuth authentication. (e.g. "example1.com,example2.com").
- Persistence: This environment variable is a `PersistentConfig` variable.