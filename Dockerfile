FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl git build-essential bash && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
COPY . .

RUN uv venv /venv && \
    uv pip install --python /venv/bin/python --upgrade "langgraph-cli[inmem]" && \
    uv pip install --python /venv/bin/python -e .

ENV PATH="/venv/bin:$PATH"

CMD ["langgraph", "dev"]
