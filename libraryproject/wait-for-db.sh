#!/bin/sh

# Define the MongoDB host and port directly
DB_HOST="localhost" # Replace with your actual MongoDB host
DB_PORT="27017" # Replace with your actual MongoDB port
DB_USER="" # Replace with your actual MongoDB user (if authentication is enabled)
DB_PASS="" # Replace with your actual MongoDB password (if authentication is enabled)

# Check if the MongoDB is up by trying to connect to it
echo "Waiting for MongoDB to be ready..."

until mongo --host "$DB_HOST" --port "$DB_PORT" --eval "db.adminCommand('ping')" --quiet > /dev/null 2>&1; do
  sleep 1
done

echo "MongoDB is ready. Starting Django..."
