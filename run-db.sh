#!/bin/sh


docker stop media-cloud-db
docker remove media-cloud-db

docker run --name media-cloud-db --env-file .env --network dev-network -p 5434:5432 postgres:alpine
