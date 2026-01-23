#!/bin/zsh

docker stop media-cloud-db
docker remove media-cloud-db

docker run --name media-cloud-db --env-file db.env -p 5434:5432 postgres:alpine
