#!/bin/bash

echo "Building and starting the service..."

docker-compose down

docker-compose up --build

docker-compose ps

echo "Service is running at http://localhost:5000"
