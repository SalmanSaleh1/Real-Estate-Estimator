#!/bin/bash

# Set the image name
IMAGE_NAME="ree"
CONTAINER_NAME="ree_container"

# Delete the existing Docker container if it exists
docker rm -f $CONTAINER_NAME

# Delete the existing Docker image
docker rmi -f $IMAGE_NAME

# Build the new Docker image
docker build -t $IMAGE_NAME .

# Run the Docker container
docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME
