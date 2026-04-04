FROM ghcr.io/astral-sh/uv:python3.13-alpine

# Install dependecy for python-magic library
RUN apk update && apk add libmagic

COPY . /api
WORKDIR /api

# Define env variable for storage path based on docker compose env file
ARG STORAGE_PATH
ENV CONTAINER_STORAGE_PATH=${STORAGE_PATH}

RUN mkdir -p ${CONTAINER_STORAGE_PATH}
RUN uv sync --locked

ENV PATH=/api/.venv/bin:$PATH

EXPOSE 8000

CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "1", "-b", "0.0.0.0:8000"]
