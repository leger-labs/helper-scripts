:::info

This page is up-to-date with Open WebUI release version [v0.6.5](https://github.com/open-webui/open-webui/releases/tag/v0.6.5), but is still a work in progress to later include more accurate descriptions, listing out options available for environment variables, defaults, and improving descriptions.

:::

:::note

When launching Open WebUI for the first time, all environment variables are treated equally and can be used to configure the application. However, for environment variables marked as `PersistentConfig`, their values are persisted and stored internally.

After the initial launch, if you restart the container, `PersistentConfig` environment variables will no longer use the external environment variable values. Instead, they will use the internally stored values.

In contrast, regular environment variables will continue to be updated and applied on each subsequent restart.

You can update the values of `PersistentConfig` environment variables directly from within Open WebUI, and these changes will be stored internally. This allows you to manage these configuration settings independently of the external environment variables.

Please note that `PersistentConfig` environment variables are clearly marked as such in the documentation below, so you can be aware of how they will behave.

:::

:::danger

This should **only** ever be set to `False` when [ENABLE_OAUTH_SIGNUP](https://docs.openwebui.com/getting-started/env-configuration/#enable_oauth_signup)
is also being used and set to `True`. Failure to do so will result in the inability to login.

:::

:::info
If you're running the application via Python and using the `open-webui serve` command, you cannot set the port using the `PORT` configuration. Instead, you must specify it directly as a command-line argument using the `--port` flag. For example:

```bash
open-webui serve --port 9999
```

This will run the Open WebUI on port `9999`. The `PORT` environment variable is disregarded in this mode.
:::

:::info

When setting this environment variable in a `.env` file, make sure to escape the quotes by wrapping the entire value in double quotes and using escaped quotes (`\"`) for the inner quotes. Example:

```
WEBUI_BANNERS="[{\"id\": \"1\", \"type\": \"warning\", \"title\": \"Your messages are stored.\", \"content\": \"Your messages are stored and may be reviewed by human people. LLM's are prone to hallucinations, check sources.\", \"dismissible\": true, \"timestamp\": 1000}]"
```

:::

:::info

This is the maximum amount of time the client will wait for a response before timing out.
If set to an empty string (' '), the timeout will be set to `None`, effectively disabling the timeout and
allowing the client to wait indefinitely.

:::

:::note
The AIOHTTP_CLIENT_TIMEOUT_MODEL_LIST is set to 10 seconds by default to help ensure that all necessary connections are available when opening the web UI. This duration allows enough time for retrieving the model list even in cases of higher network latency. You can lower this value if quicker timeouts are preferred, but keep in mind that doing so may lead to some connections being dropped, depending on your network conditions.
:::

:::info

When enabling `ENABLE_AUTOCOMPLETE_GENERATION`, ensure that you also configure `AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH` and `AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE` accordingly.

:::

:::note

The value of `API_KEY_ALLOWED_ENDPOINTS` should be a comma-separated list of endpoint URLs, such as `/api/v1/messages, /api/v1/channels`.

:::

:::warning

When `ENABLE_OAUTH_SIGNUP` is enabled, setting `WEBUI_SESSION_COOKIE_SAME_SITE` to `strict` can cause login failures. This is because Open WebUI uses a session cookie to validate the callback from the OAuth provider, which helps prevent CSRF attacks.

However, a `strict` session cookie is not sent with the callback request, leading to potential login issues. If you experience this problem, use the default `lax` value instead.

:::

:::info

If the value is not set, `WEBUI_SESSION_COOKIE_SAME_SITE` will be used as a fallback.

:::

:::info

If the value is not set, `WEBUI_SESSION_COOKIE_SECURE` will be used as a fallback.

:::

:::danger

If set to `False`, authentication will be disabled for your Open WebUI instance. However, it's
important to note that turning off authentication is only possible for fresh installations without
any existing users. If there are already users registered, you cannot disable authentication
directly. Ensure that no users are present in the database if you intend to turn off `WEBUI_AUTH`.

:::

:::info

When deploying Open-WebUI in a multiple-node cluster with a load balancer, you must ensure that the WEBUI_SECRET_KEY value is the same across all instances in order to enable users to continue working if a node is recycled or their session is transferred to a different node. Without it, they will need to sign in again each time the underlying node changes.

:::

:::info

When configuring `RAG_FILE_MAX_SIZE` and `RAG_FILE_MAX_COUNT`, ensure that the values are reasonable to prevent excessive file uploads and potential performance issues.

:::

:::info

When enabling `GOOGLE_DRIVE_INTEGRATION`, ensure that you have configured `GOOGLE_DRIVE_CLIENT_ID` and `GOOGLE_DRIVE_API_KEY` correctly, and have reviewed Google's terms of service and usage guidelines.

:::

:::info

When using `playwright`, you have two options:

1. If `PLAYWRIGHT_WS_URI` is not set, Playwright with Chromium dependencies will be automatically installed in the Open WebUI container on launch.
2. If `PLAYWRIGHT_WS_URI` is set, Open WebUI will connect to a remote browser instance instead of installing dependencies locally.

:::

:::tip

Using a remote Playwright browser via `PLAYWRIGHT_WS_URL` can be beneficial for:

- Reducing the size of the Open WebUI container
- Using a different browser other than the default Chromium
- Connecting to a non-headless (GUI) browser

:::

:::danger

`ENABLE_LOGIN_FORM` must be set to `False` when `ENABLE_OAUTH_SIGNUP` is set to `True`. Failure to do so will result in the inability to login.

:::

:::info

Supports SQLite and Postgres. Changing the URL does not migrate data between databases.
Documentation on the URL scheme is available available [here](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls).

:::

:::info

More information about this setting can be found [here](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool.params.max_overflow).

:::

:::info

More information about this setting can be found [here](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool.params.timeout).

:::

:::info

More information about this setting can be found [here](https://docs.sqlalchemy.org/en/20/core/pooling.html#setting-pool-recycle).

:::

:::info

When deploying Open-WebUI in a multi-node/worker cluster, you must ensure that the REDIS_URL value is set. Without it, session, persistency and consistency issues in the app-state will occur as the workers would be unable to communicate.

:::

:::info

When deploying Open-WebUI in a multi-node/worker cluster, you must ensure that the ENABLE_WEBSOCKET_SUPPORT value is set. Without it, websocket consistency and persistency issues will occur.

:::

:::info

When deploying Open-WebUI in a multi-node/worker cluster, you must ensure that the WEBSOCKET_MANAGER value is set and a key-value NoSQL database like Redis is used. Without it, websocket consistency and persistency issues will occur.

:::

:::info

When deploying Open-WebUI in a multi-node/worker cluster, you must ensure that the WEBSOCKET_REDIS_URL value is set and a key-value NoSQL database like Redis is used. Without it, websocket consistency and persistency issues will occur.

:::

:::info

When deploying in orchestrated environments like Kubernetes or using Helm charts, it's recommended to keep UVICORN_WORKERS set to 1. Container orchestration platforms already provide their own scaling mechanisms through pod replication, and using multiple workers inside containers can lead to resource allocation issues and complicate horizontal scaling strategies.

If you use UVICORN_WORKERS, you also need to ensure that related environment variables for scalable multi-instance setups are set accordingly.

:::