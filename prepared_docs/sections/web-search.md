## Web Search

#### `ENABLE_WEB_SEARCH`

- Type: `bool`
- Default: `False`
- Description: Enable web search toggle.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_SEARCH_QUERY_GENERATION`

- Type: `bool`
- Default: `True`
- Description: Enables or disables search query generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `WEB_SEARCH_TRUST_ENV`

- Type: `bool`
- Default: `False`
- Description: Enables proxy set by `http_proxy` and `https_proxy` during web search content fetching.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `WEB_SEARCH_RESULT_COUNT`

- Type: `int`
- Default: `3`
- Description: Maximum number of search results to crawl.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `WEB_SEARCH_CONCURRENT_REQUESTS`

- Type: `int`
- Default: `10`
- Description: Number of concurrent requests to crawl web pages returned from search results.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `WEB_SEARCH_ENGINE`

- Type: `str`
- Options:
  - `searxng` - Uses the [SearXNG](https://github.com/searxng/searxng) search engine.
  - `google_pse` - Uses the [Google Programmable Search Engine](https://programmablesearchengine.google.com/about/).
  - `brave` - Uses the [Brave search engine](https://brave.com/search/api/).
  - `kagi` - Uses the [Kagi](https://www.kagi.com/) search engine.
  - `mojeek` - Uses the [Mojeek](https://www.mojeek.com/) search engine.
  - `bocha` - Uses the Bocha search engine.
  - `serpstack` - Uses the [Serpstack](https://serpstack.com/) search engine.
  - `serper` - Uses the [Serper](https://serper.dev/) search engine.
  - `serply` - Uses the [Serply](https://serply.io/) search engine.
  - `searchapi` - Uses the [SearchAPI](https://www.searchapi.io/) search engine.
  - `serpapi` - Uses the [SerpApi](https://serpapi.com/) search engine.
  - `duckduckgo` - Uses the [DuckDuckGo](https://duckduckgo.com/) search engine.
  - `tavily` - Uses the [Tavily](https://tavily.com/) search engine.
  - `jina` - Uses the [Jina](https://jina.ai/) search engine.
  - `bing` - Uses the [Bing](https://www.bing.com/) search engine.
  - `exa` - Uses the [Exa](https://exa.ai/) search engine.
  - `perplexity` - Uses the [Perplexity AI](https://www.perplexity.ai/) search engine.
  - `sougou` - Uses the [Sougou](https://www.sogou.com/) search engine.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `BYPASS_WEB_SEARCH_EMBEDDING_AND_RETRIEVAL`

- Type: `bool`
- Default: `False`
- Description: Bypasses the web search embedding and retrieval process.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `SEARXNG_QUERY_URL`

- Type: `str`
- Description: The [SearXNG search API](https://docs.searxng.org/dev/search_api.html) URL supporting JSON output. `<query>` is replaced with
the search query. Example: `http://searxng.local/search?q=<query>`
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GOOGLE_PSE_API_KEY`

- Type: `str`
- Description: Sets the API key for the Google Programmable Search Engine (PSE) service.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GOOGLE_PSE_ENGINE_ID`

- Type: `str`
- Description: The engine ID for the Google Programmable Search Engine (PSE) service.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `BRAVE_SEARCH_API_KEY`

- Type: `str`
- Description: Sets the API key for the Brave Search API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `KAGI_SEARCH_API_KEY`

- Type: `str`
- Description: Sets the API key for Kagi Search API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MOJEEK_SEARCH_API_KEY`

- Type: `str`
- Description: Sets the API key for Mojeek Search API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `SERPSTACK_API_KEY`

- Type: `str`
- Description: Sets the API key for Serpstack search API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `SERPSTACK_HTTPS`

- Type: `bool`
- Default: `True`
- Description: Configures the use of HTTPS for Serpstack requests. Free tier requests are restricted to HTTP only.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `SERPER_API_KEY`

- Type: `str`
- Description: Sets the API key for Serper search API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `SERPLY_API_KEY`

- Type: `str`
- Description: Sets the API key for Serply search API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `SEARCHAPI_API_KEY`

- Type: `str`
- Description: Sets the API key for SearchAPI.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `SEARCHAPI_ENGINE`

- Type: `str`
- Description: Sets the SearchAPI engine.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `TAVILY_API_KEY`

- Type: `str`
- Description: Sets the API key for Tavily search API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `JINA_API_KEY`

- Type: `str`
- Description: Sets the API key for Jina.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `BING_SEARCH_V7_ENDPOINT`

- Type: `str`
- Description: Sets the endpoint for Bing Search API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `BING_SEARCH_V7_SUBSCRIPTION_KEY`

- Type: `str`
- Default: `https://api.bing.microsoft.com/v7.0/search`
- Description: Sets the subscription key for Bing Search API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `BOCHA_SEARCH_API_KEY`

- Type: `str`
- Default: `None`
- Description: Sets the API key for Bocha Search API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `EXA_API_KEY`

- Type: `str`
- Default: `None`
- Description: Sets the API key for Exa search API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `SERPAPI_API_KEY`

- Type: `str`
- Default: `None`
- Description: Sets the API key for SerpAPI.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `SERPAPI_ENGINE`

- Type: `str`
- Default: `None`
- Description: Specifies the search engine to use for SerpAPI.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `SOUGOU_API_SID`

- Type: `str`
- Default: `None`
- Description: Sets the Sogou API SID.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `SOUGOU_API_SK`

- Type: `str`
- Default: `None`
- Description: Sets the Sogou API SK.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `TAVILY_EXTRACT_DEPTH`

- Type: `str`
- Default: `basic`
- Description: Specifies the extract depth for Tavily search results.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Web Loader Configuration

#### `WEB_LOADER_ENGINE`

- Type: `str`
- Default: `safe_web`
- Description: Specifies the loader to use for retrieving and processing web content.
- Options:
  - `requests` - Uses the Requests module with enhanced error handling.
  - `playwright` - Uses Playwright for more advanced web page rendering and interaction.
- Persistence: This environment variable is a `PersistentConfig` variable.

:::info

When using `playwright`, you have two options:

1. If `PLAYWRIGHT_WS_URI` is not set, Playwright with Chromium dependencies will be automatically installed in the Open WebUI container on launch.
2. If `PLAYWRIGHT_WS_URI` is set, Open WebUI will connect to a remote browser instance instead of installing dependencies locally.

:::

#### `PLAYWRIGHT_WS_URL`

- Type: `str`
- Default: `None`
- Description: Specifies the WebSocket URI of a remote Playwright browser instance. When set, Open WebUI will use this remote browser instead of installing browser dependencies locally. This is particularly useful in containerized environments where you want to keep the Open WebUI container lightweight and separate browser concerns. Example: `ws://playwright:3000`
- Persistence: This environment variable is a `PersistentConfig` variable.

:::tip

Using a remote Playwright browser via `PLAYWRIGHT_WS_URL` can be beneficial for:

- Reducing the size of the Open WebUI container
- Using a different browser other than the default Chromium
- Connecting to a non-headless (GUI) browser

:::

#### `FIRECRAWL_API_BASE_URL`

- Type: `str`
- Default: `https://api.firecrawl.dev`
- Description: Sets the base URL for Firecrawl API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `FIRECRAWL_API_KEY`

- Type: `str`
- Default: `None`
- Description: Sets the API key for Firecrawl API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `PERPLEXITY_API_KEY`

- Type: `str`
- Default: `None`
- Description: Sets the API key for Perplexity API.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `PLAYWRIGHT_TIMEOUT`

- Type: `int`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the timeout for Playwright requests.
- Persistence: This environment variable is a `PersistentConfig` variable.

### YouTube Loader

#### `YOUTUBE_LOADER_PROXY_URL`

- Type: `str`
- Description: Sets the proxy URL for YouTube loader.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `YOUTUBE_LOADER_LANGUAGE`

- Type: `str`
- Default: `en`
- Description: Comma-separated list of language codes to try when fetching YouTube video transcriptions, in priority order.
- Example: If set to `es,de`, Spanish transcriptions will be attempted first, then German if Spanish was not available, and lastly English. Note: If none of the specified languages are available and `en` was not in your list, the system will automatically try English as a final fallback.
- Persistence: This environment variable is a `PersistentConfig` variable.