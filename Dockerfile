FROM ghcr.io/astral-sh/uv:python3.13-alpine

COPY . /api
WORKDIR /api
RUN uv sync --locked

ENV PATH=/api/.venv/bin:$PATH

EXPOSE 8000

CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000"]
