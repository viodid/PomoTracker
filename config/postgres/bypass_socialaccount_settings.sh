#!/bin/bash

DB_NAME="pomotracker"
DB_USER="postgres"


SQL_COMMANDS="
INSERT INTO socialaccount_socialapp (id, provider, name, client_id, secret, settings, key, provider_id)
VALUES (2, 'google', 'google', 1, 123, '{}', 1, 1);

INSERT INTO socialaccount_socialapp_sites (id, site_id, socialapp_id)
VALUES (1, 2, 2);
"

# echo "$SQL_COMMANDS" | psql -U $DB_USER -d $DB_NAME
psql -U $DB_USER -d $DB_NAME -c "$SQL_COMMANDS"

echo "SQL commands executed successfully."

