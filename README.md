# Nestbot

A Telegram bot with long-term user memory, powered by PostgreSQL + `pgvector`, LLMs served through Ollama, and local image OCR via EasyOCR.

The bot:

- replies to text messages in Polish,
- stores durable facts about the user,
- retrieves saved memories semantically,
- can save text extracted from PDFs and images as document memory.

## How It Works

For each conversation, the bot:

1. retrieves saved user facts and document chunks from the database,
2. builds a context for the LLM,
3. generates a response,
4. tries to extract new, durable facts from the user's message and save them,
5. stores embeddings in PostgreSQL for later semantic retrieval.

## Stack

- Python 3.12+
- `python-telegram-bot`
- SQLAlchemy + Alembic
- PostgreSQL with `pgvector`
- LangChain
- Ollama
- EasyOCR

## Features

- User profile memory extracted from chat messages.
- Document memory created from PDFs.
- OCR for images using EasyOCR (`pl` + `en`, CPU by default).
- Access restriction for selected Telegram accounts through `ALLOWED_TELEGRAM_IDS`.
- Simple developer scripts for checking the database and memory flow.

## Requirements

Before getting started, make sure you have:

- Python 3.12+
- `uv`
- Docker and Docker Compose
- Ollama running locally at `http://localhost:11434`
- a Telegram bot token

## Quick Start

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure environment variables

Copy the example environment file and fill in the values:

```bash
cp .env.example .env
```

At minimum, configure:

- `TELEGRAM_BOT_TOKEN`
- `POSTGRES_PASSWORD`
- `DATABASE_URL`
- `PGVECTOR_CONNECTION_STRING`
- `LLM_MODEL`
- `EMBEDDING_MODEL`
- `LLM_EXTRACTOR_MODEL`

Example local configuration:

```env
APP_ENV=dev
APP_DEBUG=true
LOG_LEVEL=INFO

POSTGRES_DB=assistant_db
POSTGRES_USER=assistant
POSTGRES_PASSWORD=change_me
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

DATABASE_URL=postgresql+psycopg://assistant:change_me@localhost:5432/assistant_db
PGVECTOR_CONNECTION_STRING=postgresql+psycopg://assistant:change_me@localhost:5432/assistant_db

LLM_PROVIDER=ollama
LLM_MODEL=qwen3:8b
EMBEDDING_MODEL=nomic-embed-text
LLM_BASE_URL=http://localhost:11434
LLM_EXTRACTOR_MODEL=llama3.2:1b

TELEGRAM_BOT_TOKEN=your_token_here
ALLOWED_TELEGRAM_IDS=123456789
```

If `ALLOWED_TELEGRAM_IDS` is empty, the bot will respond to any user.

### 3. Start PostgreSQL with pgvector

```bash
docker compose up -d postgres
```

The container enables the `vector` extension using [`postgres/init.sql`](/home/masingneckstage/PycharmProjects/nestbot/postgres/init.sql).

### 4. Run database migrations

```bash
uv run alembic upgrade head
```

### 5. Pull the required Ollama models

For example:

```bash
ollama pull qwen3:8b
ollama pull nomic-embed-text
ollama pull llama3.2:1b
```

The model names must match the values in your `.env` file.

### 6. Run the bot

```bash
uv run python main.py
```

The bot runs in polling mode.

## Telegram Commands

- `/start` - shows a short help message
- `/memories` - displays saved memories about the user
- `/forget` - currently only returns a message; deletion through the bot is not implemented yet

## File Handling

- Sending a PDF splits the document into chunks and stores them as `document` memory.
- Sending an image runs local OCR through EasyOCR and stores the extracted text as document memory.

## Helpful Scripts

Check database connectivity:

```bash
uv run python scripts/check_db.py
```

Test memory creation:

```bash
uv run python scripts/test_memory_flow.py
```

Test memory retrieval:

```bash
uv run python scripts/test_memory_retrieval.py
```

## Project Structure

```text
.
├── main.py               # Telegram application entry point
├── config.py             # configuration loaded from .env
├── handlers/             # Telegram handlers
├── services/             # chat, memory, document, and embedding logic
├── llm/                  # model integrations and fact extraction
├── models/               # SQLAlchemy models
├── repositories/         # data access layer
├── db/                   # SQLAlchemy/PostgreSQL setup
├── domain/               # domain types
├── prompts/              # system prompts
├── alembic/              # database migrations
├── postgres/             # database initialization
└── scripts/              # helper scripts
```

## Limitations and Notes

- The project assumes Ollama is running locally.
- Image OCR is handled locally by EasyOCR instead of an Ollama vision model.
- The bot is instructed to answer only from stored memory context; if the information is missing, it should say so directly.
- The `/forget` command is not yet connected to actual memory deletion in Telegram.
- Document memory stores text chunks rather than full document structure.
