#!/bin/sh

# This script is used to run the application in a Docker container.
# It waits for the database to be ready, runs migrations, and then starts the server.

# The Render deployment environment will have the DATABASE_URL set,
# but the local docker-compose setup uses PGHOST, PGUSER, etc.
if [ -n "$DATABASE_URL" ]; then
    # In Render, we don't need to wait for the DB as it's managed.
    echo "Render environment detected. Skipping DB wait."
else
    # For local docker-compose, wait for the database to be ready.
    # The postgres container will have these env vars set.
    echo "Waiting for postgres..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

# Run database migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# The "$@" CMD from the Dockerfile will be executed here
exec "$@"
