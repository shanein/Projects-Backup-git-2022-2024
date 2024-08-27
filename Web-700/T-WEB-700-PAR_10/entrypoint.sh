#!/bin/bash

set -e

cd crypto_api
# Ensure the app's dependencies are installed
mix deps.get

# Wait until Postgres is ready
while ! pg_isready -q -h $PGHOST -p $PGPORT -U $PGUSER
do
  echo "$(date) - waiting for database to start"
  sleep 2
done

# Create, migrate, and seed database if it doesn't exist.
if [[ -z `psql -Atqc "\\list $PGDATABASE"` ]]; then
  echo "Database $PGDATABASE does not exist. Creating..."
  createdb $PGDATABASE
  mix ecto.create
  mix ecto.migrate
  mix run priv/repo/seeds.exs
  echo "Database $PGDATABASE created."
fi

mix phx.server
.gitignore
