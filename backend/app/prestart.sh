#! /usr/bin/env bash

echo "Waiting for postgres..."

while ! nc -z psql 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

exec "$@"

# Let the DB start
python ./app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python ./app/initial_data.py