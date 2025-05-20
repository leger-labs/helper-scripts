## RAG Content Extraction Engine

#### `CONTENT_EXTRACTION_ENGINE`

- Type: `str`
- Options:
  - Leave empty to use default
  - `external` - Use external loader
  - `tika` - Use a local Apache Tika server
  - `docling` - Use Docling engine
  - `document_intelligence` - Use Document Intelligence engine
  - `mistral_ocr` - Use Mistral OCR engine
- Description: Sets the content extraction engine to use for document ingestion.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MISTRAL_OCR_API_KEY`

- Type: `str`
- Default: `None`
- Description: Specifies the Mistral OCR API key to use.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `EXTERNAL_DOCUMENT_LOADER_URL`

- Type: `str`
- Default: `None`
- Description: Sets the URL for the external document loader service.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `EXTERNAL_DOCUMENT_LOADER_API_KEY`

- Type: `str`
- Default: `None`
- Description: Sets the API key for authenticating with the external document loader service.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `TIKA_SERVER_URL`

- Type: `str`
- Default: `http://localhost:9998`
- Description: Sets the URL for the Apache Tika server.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `DOCLING_SERVER_URL`

- Type: `str`
- Default: `http://docling:5001`
- Description: Specifies the URL for the Docling server.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `DOCLING_OCR_ENGINE`

- Type: `str`  
- Default: `tesseract`  
- Description: Specifies the OCR engine used by Docling.  
  Supported values include: `tesseract` (default), `easyocr`, `ocrmac`, `rapidocr`, and `tesserocr`.  
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `DOCLING_OCR_LANG`

- Type: `str`  
- Default: `eng,fra,deu,spa` (when using the default `tesseract` engine)  
- Description: Specifies the OCR language(s) to be used with the configured `DOCLING_OCR_ENGINE`.  
  The format and available language codes depend on the selected OCR engine.  
- Persistence: This environment variable is a `PersistentConfig` variable.