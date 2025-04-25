#!/bin/bash

DB_USER="$1"
DB_PASS="$2"
DB_HOST="${3:-localhost}"
DB_PORT="${4:-3306}"
DB_NAME="chaintales"

if [[ -z "$DB_USER" || -z "$DB_PASS" ]]; then
  echo "Usage: $0 <db_user> <db_pass> [db_host] [db_port]"
  exit 1
fi

mysql -u "$DB_USER" -p"$DB_PASS" -h "$DB_HOST" -P "$DB_PORT" <<EOF
DROP DATABASE IF EXISTS $DB_NAME;
CREATE DATABASE $DB_NAME;
EOF

echo "Database '$DB_NAME' dropped and recreated successfully on $DB_HOST:$DB_PORT."
