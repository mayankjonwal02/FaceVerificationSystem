# Use the official MongoDB base image
FROM mongo:latest

# # Copy initialization script to the appropriate directory
# COPY init.js /docker-entrypoint-initdb.d/

# Set environment variables for MongoDB
ENV MONGO_INITDB_DATABASE=LibraryUsers
ENV MONGO_INITDB_ROOT_USERNAME=root
ENV MONGO_INITDB_ROOT_PASSWORD=password

# Expose MongoDB default port
EXPOSE 27017
