#!/bin/bash

echo "Building and starting the service..."

docker-compose down

docker-compose up --build -d

docker-compose ps

echo "Service is running at http://localhost:5000"
