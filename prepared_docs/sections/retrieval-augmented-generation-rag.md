## Retrieval Augmented Generation (RAG)

#### `RAG_EMBEDDING_ENGINE`

- Type: `str`
- Options:
  - Leave empty for `Default (SentenceTransformers)` - Uses SentenceTransformers for embeddings.
  - `ollama` - Uses the Ollama API for embeddings.
  - `openai` - Uses the OpenAI API for embeddings.
- Description: Selects an embedding engine to use for RAG.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_EMBEDDING_MODEL`

- Type: `str`
- Default: `sentence-transformers/all-MiniLM-L6-v2`
- Description: Sets a model for embeddings. Locally, a Sentence-Transformer model is used.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_RAG_HYBRID_SEARCH`

- Type: `bool`
- Default: `False`
- Description: Enables the use of ensemble search with `BM25` + `ChromaDB`, with reranking using
`sentence_transformers` models.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_TOP_K`

- Type: `int`
- Default: `3`
- Description: Sets the default number of results to consider for the embedding when using RAG.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_TOP_K_RERANKER`

- Type: `int`
- Default: `3`
- Description: Sets the default number of results to consider for the reranker when using RAG.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_RELEVANCE_THRESHOLD`

- Type: `float`
- Default: `0.0`
- Description: Sets the relevance threshold to consider for documents when used with reranking.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_TEMPLATE`

- Type: `str`
- Default: The value of `DEFAULT_RAG_TEMPLATE` environment variable.



- Description: Template to use when injecting RAG documents into chat completion
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_TEXT_SPLITTER`

- Type: `str`
- Options:
  - `character`
  - `token`
- Default: `character`
- Description: Sets the text splitter for RAG models.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `TIKTOKEN_CACHE_DIR`

- Type: `str`
- Default: `{CACHE_DIR}/tiktoken`
- Description: Sets the directory for TikToken cache.

#### `TIKTOKEN_ENCODING_NAME`

- Type: `str`
- Default: `cl100k_base`
- Description: Sets the encoding name for TikToken.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CHUNK_SIZE`

- Type: `int`
- Default: `1000`
- Description: Sets the document chunk size for embeddings.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CHUNK_OVERLAP`

- Type: `int`
- Default: `100`
- Description: Specifies how much overlap there should be between chunks.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `PDF_EXTRACT_IMAGES`

- Type: `bool`
- Default: `False`
- Description: Extracts images from PDFs using OCR when loading documents.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_FILE_MAX_SIZE`

- Type: `int`
- Description: Sets the maximum size of a file in megabytes that can be uploaded for document ingestion.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_FILE_MAX_COUNT`

- Type: `int`
- Description: Sets the maximum number of files that can be uploaded at once for document ingestion.
- Persistence: This environment variable is a `PersistentConfig` variable.

:::info

When configuring `RAG_FILE_MAX_SIZE` and `RAG_FILE_MAX_COUNT`, ensure that the values are reasonable to prevent excessive file uploads and potential performance issues.

:::

#### `RAG_ALLOWED_FILE_EXTENSIONS`

- Type: `list` of `str`
- Default: `[]` (which means all supported file types are allowed)
- Description: Specifies which file extensions are permitted for upload. 

```json
["pdf,docx,txt"]
```

- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_RERANKING_MODEL`

- Type: `str`
- Description: Sets a model for reranking results. Locally, a Sentence-Transformer model is used.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_OPENAI_API_BASE_URL`

- Type: `str`
- Default: `${OPENAI_API_BASE_URL}`
- Description: Sets the OpenAI base API URL to use for RAG embeddings.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_OPENAI_API_KEY`

- Type: `str`
- Default: `${OPENAI_API_KEY}`
- Description: Sets the OpenAI API key to use for RAG embeddings.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_EMBEDDING_OPENAI_BATCH_SIZE`

- Type: `int`
- Default: `1`
- Description: Sets the batch size for OpenAI embeddings.

#### `RAG_EMBEDDING_BATCH_SIZE`

- Type: `int`
- Default: `1`
- Description: Sets the batch size for embedding in RAG (Retrieval-Augmented Generator) models.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_OLLAMA_API_KEY`

- Type: `str`
- Description: Sets the API key for Ollama API used in RAG models.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_OLLAMA_BASE_URL`

- Type: `str`
- Description: Sets the base URL for Ollama API used in RAG models.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_RETRIEVAL_QUERY_GENERATION`

- Type: `bool`
- Default: `True`
- Description: Enables or disables retrieval query generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `QUERY_GENERATION_PROMPT_TEMPLATE`

- Type: `str`
- Default: The value of `DEFAULT_QUERY_GENERATION_PROMPT_TEMPLATE` environment variable.



- Description: Sets the prompt template for query generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `BYPASS_EMBEDDING_AND_RETRIEVAL`

- Type: `bool`
- Default: `False`
- Description: Bypasses the embedding and retrieval process.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `DOCUMENT_INTELLIGENCE_ENDPOINT`

- Type: `str`
- Default: `None`
- Description: Specifies the endpoint for document intelligence.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `DOCUMENT_INTELLIGENCE_KEY`

- Type: `str`
- Default: `None`
- Description: Specifies the key for document intelligence.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_RAG_LOCAL_WEB_FETCH`

- Type: `bool`
- Default: `False`
- Description: Enables or disables local web fetch for RAG.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_EMBEDDING_CONTENT_PREFIX`

- Type: `str`
- Default: `None`
- Description: Specifies the prefix for the RAG embedding content.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_EMBEDDING_PREFIX_FIELD_NAME`

- Type: `str`
- Default: `None`
- Description: Specifies the field name for the RAG embedding prefix.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_EMBEDDING_QUERY_PREFIX`

- Type: `str`
- Default: `None`
- Description: Specifies the prefix for the RAG embedding query.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RAG_FULL_CONTEXT`

- Type: `bool`
- Default: `False`
- Description: Specifies whether to use the full context for RAG.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Google Drive

#### `ENABLE_GOOGLE_DRIVE_INTEGRATION`

- Type: `bool`
- Default: `False`
- Description: Enables or disables Google Drive integration. If set to true, and `GOOGLE_DRIVE_CLIENT_ID` & `GOOGLE_DRIVE_API_KEY` are both configured, Google Drive will appear as an upload option in the chat UI.
- Persistence: This environment variable is a `PersistentConfig` variable.

:::info

When enabling `GOOGLE_DRIVE_INTEGRATION`, ensure that you have configured `GOOGLE_DRIVE_CLIENT_ID` and `GOOGLE_DRIVE_API_KEY` correctly, and have reviewed Google's terms of service and usage guidelines.

:::

#### `GOOGLE_DRIVE_CLIENT_ID`

- Type: `str`
- Description: Sets the client ID for Google Drive (client must be configured with Drive API and Picker API enabled).
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GOOGLE_DRIVE_API_KEY`

- Type: `str`
- Description: Sets the API key for Google Drive integration.
- Persistence: This environment variable is a `PersistentConfig` variable.

### OneDrive

#### `ENABLE_ONEDRIVE_INTEGRATION`

- Type: `bool`
- Default: `False`
- Description: Enables or disables OneDrive integration.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ONEDRIVE_CLIENT_ID`

- Type: `str`
- Default: `None`
- Description: Specifies the client ID for OneDrive integration.
- Persistence: This environment variable is a `PersistentConfig` variable.