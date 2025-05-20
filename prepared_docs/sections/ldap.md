## LDAP

#### `ENABLE_LDAP`

- Type: `bool`
- Default: `False`
- Description: Enables or disables LDAP authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_SERVER_LABEL`

- Type: `str`
- Description: Sets the label of the LDAP server.
- Persistence: This environment variable is a `PersistentConfig` variable.


#### `LDAP_SERVER_HOST`

- Type: `str`
- Default: `localhost`
- Description: Sets the hostname of the LDAP server.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_SERVER_PORT`

- Type: `int`
- Default: `389`
- Description: Sets the port number of the LDAP server.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_ATTRIBUTE_FOR_MAIL`

- Type: `str`
- Description: Sets the attribute to use as mail for LDAP authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_ATTRIBUTE_FOR_USERNAME`

- Type: `str`
- Description: Sets the attribute to use as a username for LDAP authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_APP_DN`

- Type: `str`
- Description: Sets the distinguished name for the LDAP application.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_APP_PASSWORD`

- Type: `str`
- Description: Sets the password for the LDAP application.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_SEARCH_BASE`

- Type: `str`
- Description: Sets the base to search for LDAP authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_SEARCH_FILTER`

- Type: `str`
- Default: `None`
- Description: Sets a single filter to use for LDAP search. Alternative to `LDAP_SEARCH_FILTERS`.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_SEARCH_FILTERS`

- Type: `str`
- Description: Sets the filter to use for LDAP search.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_USE_TLS`

- Type: `bool`
- Default: `True`
- Description: Enables or disables TLS for LDAP connection.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_CA_CERT_FILE`

- Type: `str`
- Description: Sets the path to the LDAP CA certificate file.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_VALIDATE_CERT`

- Type: `bool`
- Description: Sets whether to validate the LDAP CA certificate.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_CIPHERS`

- Type: `str`
- Default: `ALL`
- Description: Sets the ciphers to use for LDAP connection.
- Persistence: This environment variable is a `PersistentConfig` variable.