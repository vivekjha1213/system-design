#!/bin/bash

# Script to restart Docker containers

# Set the name of your Docker Compose project if needed
PROJECT_NAME="shortener_app"

# Navigate to the directory containing docker-compose.yml
cd ~/Desktop/shortener_app || { echo "Directory not found"; exit 1; }

# Stop and remove all running containers
echo "Stopping and removing containers..."
docker-compose -p $PROJECT_NAME down

# Remove any stopped containers and unused networks
echo "Removing stopped containers and unused networks..."
docker system prune -f

# Rebuild and start the containers
echo "Rebuilding and starting containers..."
docker-compose -p $PROJECT_NAME up --build -d

# Check the status of the containers
echo "Checking container status..."
docker-compose -p $PROJECT_NAME ps

echo "Restart complete."
