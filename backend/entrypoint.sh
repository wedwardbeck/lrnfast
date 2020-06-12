#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z psql 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

exec "$@"