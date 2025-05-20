## Vector Database

#### `VECTOR_DB`

- Type: `str`
- Options:
- `chroma`, `elasticsearch`, `milvus`, `opensearch`, `pgvector`, `qdrant`, `pinecone`
- Default: `chroma`
- Description: Specifies which vector database system to use. This setting determines which vector storage system will be used for managing embeddings.

### ChromaDB

#### `CHROMA_TENANT`

- Type: `str`
- Default: The value of `chromadb.DEFAULT_TENANT` (a constant in the `chromadb` module)
- Description: Sets the tenant for ChromaDB to use for RAG embeddings.

#### `CHROMA_DATABASE`

- Type: `str`
- Default: The value of `chromadb.DEFAULT_DATABASE` (a constant in the `chromadb` module)
- Description: Sets the database in the ChromaDB tenant to use for RAG embeddings.

#### `CHROMA_HTTP_HOST`

- Type: `str`
- Description: Specifies the hostname of a remote ChromaDB Server. Uses a local ChromaDB instance if not set.

#### `CHROMA_HTTP_PORT`

- Type: `int`
- Default: `8000`
- Description: Specifies the port of a remote ChromaDB Server.

#### `CHROMA_HTTP_HEADERS`

- Type: `str`
- Description: A comma-separated list of HTTP headers to include with every ChromaDB request.
- Example: `Authorization=Bearer heuhagfuahefj,User-Agent=OpenWebUI`.

#### `CHROMA_HTTP_SSL`

- Type: `bool`
- Default: `False`
- Description: Controls whether or not SSL is used for ChromaDB Server connections.

#### `CHROMA_CLIENT_AUTH_PROVIDER`

- Type: `str`
- Description: Specifies an authentication provider for remote ChromaDB Server.
- Example: `chromadb.auth.basic_authn.BasicAuthClientProvider`

#### `CHROMA_CLIENT_AUTH_CREDENTIALS`

- Type: `str`
- Description: Specifies auth credentials for remote ChromaDB Server.
- Example: `username:password`

### Elasticsearch

#### `ELASTICSEARCH_API_KEY`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the Elasticsearch API key.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ELASTICSEARCH_CA_CERTS`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the path to the CA certificates for Elasticsearch.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ELASTICSEARCH_CLOUD_ID`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the Elasticsearch cloud ID.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ELASTICSEARCH_INDEX_PREFIX`

- Type: `str`
- Default: `open_webui_collections`
- Description: Specifies the prefix for the Elasticsearch index.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ELASTICSEARCH_PASSWORD`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the password for Elasticsearch.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ELASTICSEARCH_URL`

- Type: `str`
- Default: `https://localhost:9200`
- Description: Specifies the URL for the Elasticsearch instance.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ELASTICSEARCH_USERNAME`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the username for Elasticsearch.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Milvus

#### `MILVUS_URI`

- Type: `str`
- Default: `${DATA_DIR}/vector_db/milvus.db`
- Description: Specifies the URI for connecting to the Milvus vector database. This can point to a local or remote Milvus server based on the deployment configuration.

#### `MILVUS_DB`

- Type: `str`
- Default: `default`
- Description: Specifies the database to connect to within a Milvus instance.

#### `MILVUS_TOKEN`

- Type: `str`
- Default: `None`
- Description: Specifies an optional connection token for Milvus.

#### `MILVUS_INDEX_TYPE`

- Type: `str`
- Default: `HNSW`
- Options: `AUTOINDEX`, `FLAT`, `IVF_FLAT`, `HNSW`
- Description: Specifies the index type to use when creating a new collection in Milvus. `AUTOINDEX` is generally recommended for Milvus standalone. `HNSW` may offer better performance but typically requires a clustered Milvus setup.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MILVUS_METRIC_TYPE`

- Type: `str`
- Default: `COSINE`
- Options: `COSINE`, `IP`, `L2`
- Description: Specifies the metric type for vector similarity search in Milvus.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MILVUS_HNSW_M`

- Type: `int`
- Default: `16`
- Description: Specifies the `M` parameter for the HNSW index type in Milvus. This influences the number of bi-directional links created for each new element during construction. Only applicable if `MILVUS_INDEX_TYPE` is `HNSW`.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MILVUS_HNSW_EFCONSTRUCTION`

- Type: `int`
- Default: `100`
- Description: Specifies the `efConstruction` parameter for the HNSW index type in Milvus. This influences the size of the dynamic list for the nearest neighbors during index construction. Only applicable if `MILVUS_INDEX_TYPE` is `HNSW`.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MILVUS_IVF_FLAT_NLIST`

- Type: `int`
- Default: `128`
- Description: Specifies the `nlist` parameter for the IVF_FLAT index type in Milvus. This is the number of cluster units. Only applicable if `MILVUS_INDEX_TYPE` is `IVF_FLAT`.
- Persistence: This environment variable is a `PersistentConfig` variable.

### OpenSearch

#### `OPENSEARCH_CERT_VERIFY`

- Type: `bool`
- Default: `False`
- Description: Enables or disables OpenSearch certificate verification.

#### `OPENSEARCH_PASSWORD`

- Type: `str`
- Default: `None`
- Description: Sets the password for OpenSearch.

#### `OPENSEARCH_SSL`

- Type: `bool`
- Default: `True`
- Description: Enables or disables SSL for OpenSearch.

#### `OPENSEARCH_URI`

- Type: `str`
- Default: `https://localhost:9200`
- Description: Sets the URI for OpenSearch.

#### `OPENSEARCH_USERNAME`

- Type: `str`
- Default: `None`
- Description: Sets the username for OpenSearch.

### PGVector

#### `PGVECTOR_DB_URL`

- Type: `str`
- Default: The value of the `DATABASE_URL` environment variable
- Description: Sets the database URL for model storage.

#### `PGVECTOR_INITIALIZE_MAX_VECTOR_LENGTH`

- Type: `str`
- Default: `1536`
- Description: Specifies the maximum vector length for PGVector initialization.

### Qdrant

#### `QDRANT_API_KEY`

- Type: `str`
- Description: Sets the API key for Qdrant.

#### `QDRANT_URI`

- Type: `str`
- Description: Sets the URI for Qdrant.

#### `QDRANT_ON_DISK`

- Type: `bool`
- Default: `False`
- Description: Enable the usage of memmap(also known as on-disk) storage

#### `QDRANT_PREFER_GRPC`

- Type: `bool`
- Default: `False`
- Description: Use gPRC interface whenever possible

#### `QDRANT_GRPC_PORT`

- Type: `int`
- Default: `6334`
- Description: Sets the gRPC port number for Qdrant.

#### `ENABLE_QDRANT_MULTITENANCY_MODE`

- Type: `bool`
- Default: `False`
- Description: Enables multitenancy pattern for Qdrant collections management, which significantly reduces RAM usage and computational overhead by consolidating similar vector data structures. Recommend turn on

:::info

This will disconect all Qdrant collections created in the previous pattern, which is non-multitenancy. Go to  `Admin Settings` > `Documents` > `Reindex Knowledge Base` to migrate existing knowledges.

The Qdrant collections created in the previous pattern will still take resources.

Currently, there is no button on the UI for only reset vector DB, if you want to migrate knowledges to multitenancy:
- Remove all collections with `open_webui-knowledge` prefix (or `open_webui` prefix to remove all collections related to Open WebUI) with native Qdrant Client
- Go to  `Admin Settings` > `Documents` > `Reindex Knowledge Base` to migrate existing knowledges

`Reindex Knowledge Base` will ONLY migrate knowledges

:::

:::danger

When you decided to use multitenancy pattern as your default and you don't need to migrate old knowledge, go to `Admin Settings` > `Documents` to reset vector and knowledge, which will delete all collections with `open_webui` prefix and knowledges.

:::

### Pinecone

When using Pinecone as the vector store, the following environment variables are used to control its behavior. Make sure to set these variables in your `.env` file or deployment environment.

#### `PINECONE_API_KEY`

- Type: `str`
- Default: `None`
- Description: Sets the API key used to authenticate with the Pinecone service.

#### `PINECONE_ENVIRONMENT`

- Type: `str`
- Default: `None`
- Description: Specifies the Pinecone environment to connect to (e.g., `us-west1-gcp`, `gcp-starter`, etc.).

#### `PINECONE_INDEX_NAME`

- Type: `str`
- Default: `open-webui-index`
- Description: Defines the name of the Pinecone index that will be used to store and query vector embeddings.

#### `PINECONE_DIMENSION`

- Type: `int`
- Default: `1536`
- Description: The dimensionality of the vector embeddings. Must match the dimension expected by the index (commonly 768, 1024, 1536, or 3072 based on model used).

#### `PINECONE_METRIC`

- Type: `str`
- Default: `cosine`
- Options: `cosine`, `dotproduct`, `euclidean`
- Description: Specifies the similarity metric to use for vector comparisons within the Pinecone index.

#### `PINECONE_CLOUD`

- Type: `str`
- Default: `aws`
- Options: `aws`, `gcp`, `azure`
- Description: Specifies the cloud provider where the Pinecone index is hosted.