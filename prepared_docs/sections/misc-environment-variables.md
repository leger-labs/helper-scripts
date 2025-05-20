## Misc Environment Variables

These variables are not specific to Open WebUI but can still be valuable in certain contexts.

### Cloud Storage

#### `STORAGE_PROVIDER`

- Type: `str`
- Options:
  - `s3` - uses the S3 client library and related environment variables mentioned in [Amazon S3 Storage](#amazon-s3-storage)
  - `gcs` - uses the GCS client library and related environment variables mentioned in [Google Cloud Storage](#google-cloud-storage)
  - `azure` - uses the Azure client library and related environment variables mentioned in [Microsoft Azure Storage](#microsoft-azure-storage)
- Default: empty string (' '), which defaults to `local`
- Description: Sets the storage provider.

#### Amazon S3 Storage

#### `S3_ACCESS_KEY_ID`

- Type: `str`
- Description: Sets the access key ID for S3 storage.

#### `S3_ADDRESSING_STYLE`

- Type: `str`
- Default: `None`
- Description: Specifies the addressing style to use for S3 storage (e.g., 'path', 'virtual').

#### `S3_BUCKET_NAME`

- Type: `str`
- Description: Sets the bucket name for S3 storage.

#### `S3_ENDPOINT_URL`

- Type: `str`
- Description: Sets the endpoint URL for S3 storage.

#### `S3_KEY_PREFIX`

- Type: `str`
- Description: Sets the key prefix for a S3 object.

#### `S3_REGION_NAME`

- Type: `str`
- Description: Sets the region name for S3 storage.

#### `S3_SECRET_ACCESS_KEY`

- Type: `str`
- Description: Sets the secret access key for S3 storage.

#### `S3_USE_ACCELERATE_ENDPOINT`

- Type: `str`
- Default: `False`
- Description: Specifies whether to use the accelerated endpoint for S3 storage.

#### `S3_ENABLE_TAGGING`

- Type: `str`
- Default: `False`
- Description: Enables S3 object tagging after uploads for better organization, searching, and integration with file management policies. Always set to `False` when using Cloudflare R2, as R2 does not support object tagging.

#### Google Cloud Storage

#### `GOOGLE_APPLICATION_CREDENTIALS_JSON`

- Type: `str`
- Description: Contents of Google Application Credentials JSON file.
  - Optional - if not provided, credentials will be taken from the environment. User credentials if run locally and Google Metadata server if run on a Google Compute Engine.
  - A file can be generated for a service account following this [guide.](https://developers.google.com/workspace/guides/create-credentials#service-account)

#### `GCS_BUCKET_NAME`

- Type: `str`
- Description: Sets the bucket name for Google Cloud Storage. Bucket must already exist.

#### Microsoft Azure Storage

#### `AZURE_STORAGE_ENDPOINT`

- Type: `str`
- Description: Sets the endpoint URL for Azure Storage.

#### `AZURE_STORAGE_CONTAINER_NAME`

- Type: `str`
- Description: Sets the container name for Azure Storage.

#### `AZURE_STORAGE_KEY`

- Type: `str`
- Description: Set the access key for Azure Storage.
  - Optional - if not provided, credentials will be taken from the environment. User credentials if run locally and Managed Identity if run in Azure services.

### Database Pool

#### `DATABASE_URL`

- Type: `str`
- Default: `sqlite:///${DATA_DIR}/webui.db`
- Description: Specifies the database URL to connect to.

:::info

Supports SQLite and Postgres. Changing the URL does not migrate data between databases.
Documentation on the URL scheme is available available [here](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls).

:::

#### `DATABASE_SCHEMA`

- Type: `str`
- Default: `None`
- Description: Specifies the database schema to connect to.

#### `DATABASE_POOL_SIZE`

- Type: `int`
- Default: `0`
- Description: Specifies the size of the database pool. A value of `0` disables pooling.

#### `DATABASE_POOL_MAX_OVERFLOW`

- Type: `int`
- Default: `0`
- Description: Specifies the database pool max overflow.

:::info

More information about this setting can be found [here](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool.params.max_overflow).

:::

#### `DATABASE_POOL_TIMEOUT`

- Type: `int`
- Default: `30`
- Description: Specifies the database pool timeout in seconds to get a connection.

:::info

More information about this setting can be found [here](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool.params.timeout).

:::

#### `DATABASE_POOL_RECYCLE`

- Type: `int`
- Default: `3600`
- Description: Specifies the database pool recycle time in seconds.

:::info

More information about this setting can be found [here](https://docs.sqlalchemy.org/en/20/core/pooling.html#setting-pool-recycle).

:::

### Redis

#### `REDIS_URL`

- Type: `str`
- Example: `redis://localhost:6379/0`
- Description: Specifies the URL of the Redis instance for the app-state.

:::info

When deploying Open-WebUI in a multi-node/worker cluster, you must ensure that the REDIS_URL value is set. Without it, session, persistency and consistency issues in the app-state will occur as the workers would be unable to communicate.

:::

#### `REDIS_SENTINEL_HOSTS`

- Type: `str`
- Description: Comma-separated list of Redis Sentinels for app state. If specified, the "hostname" in `REDIS_URL` will be interpreted as the Sentinel service name.

#### `REDIS_SENTINEL_PORT`

- Type: `int`
- Default: `26379`
- Description: Sentinel port for app state Redis.

#### `ENABLE_WEBSOCKET_SUPPORT`

- Type: `bool`
- Default: `True`
- Description: Enables websocket support in Open WebUI.

:::info

When deploying Open-WebUI in a multi-node/worker cluster, you must ensure that the ENABLE_WEBSOCKET_SUPPORT value is set. Without it, websocket consistency and persistency issues will occur.

:::

#### `WEBSOCKET_MANAGER`

- Type: `str`
- Default: `redis`
- Description: Specifies the websocket manager to use (in this case, Redis).

:::info

When deploying Open-WebUI in a multi-node/worker cluster, you must ensure that the WEBSOCKET_MANAGER value is set and a key-value NoSQL database like Redis is used. Without it, websocket consistency and persistency issues will occur.

:::

#### `WEBSOCKET_REDIS_URL`

- Type: `str`
- Default: `${REDIS_URL}`
- Description: Specifies the URL of the Redis instance for websocket communication. It is distinct from `REDIS_URL` and in practice, it is recommended to set both.

:::info

When deploying Open-WebUI in a multi-node/worker cluster, you must ensure that the WEBSOCKET_REDIS_URL value is set and a key-value NoSQL database like Redis is used. Without it, websocket consistency and persistency issues will occur.

:::

#### `WEBSOCKET_SENTINEL_HOSTS`

- Type: `str`
- Description: Comma-separated list of Redis Sentinels for websocket. If specified, the "hostname" in `WEBSOCKET_REDIS_URL` will be interpreted as the Sentinel service name.

#### `WEBSOCKET_SENTINEL_PORT`

- Type: `int`
- Default: `26379`
- Description: Sentinel port for websocket Redis.

### Uvicorn Settings

#### `UVICORN_WORKERS`

- Type: `int`
- Default: `1`
- Description: Controls the number of worker processes that Uvicorn spawns to handle requests. Each worker runs its own instance of the application in a separate process.

:::info

When deploying in orchestrated environments like Kubernetes or using Helm charts, it's recommended to keep UVICORN_WORKERS set to 1. Container orchestration platforms already provide their own scaling mechanisms through pod replication, and using multiple workers inside containers can lead to resource allocation issues and complicate horizontal scaling strategies.

If you use UVICORN_WORKERS, you also need to ensure that related environment variables for scalable multi-instance setups are set accordingly.

:::

### Proxy Settings

Open WebUI supports using proxies for HTTP and HTTPS retrievals. To specify proxy settings,
Open WebUI uses the following environment variables:

#### `http_proxy`

- Type: `str`
- Description: Sets the URL for the HTTP proxy.

#### `https_proxy`

- Type: `str`
- Description: Sets the URL for the HTTPS proxy.

#### `no_proxy`

- Type: `str`
- Description: Lists domain extensions (or IP addresses) for which the proxy should not be used,
separated by commas. For example, setting no_proxy to '.mit.edu' ensures that the proxy is
bypassed when accessing documents from MIT.

### Install Required Python Packages

Open WebUI provides environment variables to customize the pip installation process. Below are the environment variables used by Open WebUI for adjusting package installation behavior:

#### `PIP_OPTIONS`

- Type: `str`
- Description: Specifies additional command-line options that pip should use when installing packages. For example, you can include flags such as `--upgrade`, `--user`, or `--no-cache-dir` to control the installation process.

#### `PIP_PACKAGE_INDEX_OPTIONS`

- Type: `str`
- Description: Defines custom package index behavior for pip. This can include specifying additional or alternate index URLs (e.g., `--extra-index-url`), authentication credentials, or other parameters to manage how packages are retrieved from different locations.