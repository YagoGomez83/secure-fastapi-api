# Secure FastAPI DevSecOps API

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![CI](https://github.com/YagoGomez83/secure-fastapi-api/actions/workflows/ci.yml/badge.svg)
![Security](https://img.shields.io/badge/SAST-Bandit-red)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

REST API built with **FastAPI** following a clean layered architecture, with Docker support, security best practices, and a ready-to-extend structure.

> **Current status:** MVP with modular architecture ready for expansion. Core layers (models, services, repositories, security) are scaffolded and actively being implemented.

---

## Why this project matters

This project demonstrates practical **DevSecOps** skills applied to a real backend API:

- **Secure API development** — input validation, non-root containers, no hardcoded secrets
- **Clean architecture** — layered separation: endpoints → services → repositories → models
- **Security scanning** — static analysis with Bandit on every run
- **Test automation** — Pytest with coverage reporting
- **Docker hardening** — non-root user, slim base image, environment-based config
- **CI/CD ready** — structured for GitHub Actions pipeline integration

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.136 + Uvicorn |
| Validation | Pydantic v2 + pydantic-settings |
| Database | SQLAlchemy 2.0 · PostgreSQL (psycopg2) · SQLite async (aiosqlite) |
| Security | bcrypt · Argon2 · Passlib · Bandit |
| Testing | Pytest · pytest-asyncio · pytest-cov |
| Containerization | Docker · Docker Compose |

---

## Project Structure

```
secure-fastapi-api/
├── app/
│   ├── main.py                  # Application entry point
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── user.py      # User endpoints
│   ├── core/
│   │   ├── config.py            # Settings via pydantic-settings
│   │   ├── logging.py           # Logging configuration
│   │   └── security.py          # Auth utilities
│   ├── models/
│   │   └── user.py              # SQLAlchemy models
│   ├── schemas/
│   │   └── user.py              # Pydantic schemas (request/response)
│   ├── repositories/
│   │   └── user_repository.py   # Database access layer
│   └── services/
│       └── user_service.py      # Business logic layer
├── tests/
│   └── test_users.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL 12+ *(or SQLite for local development)*
- Docker & Docker Compose *(optional)*

### Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YagoGomez83/secure-fastapi-api.git
   cd secure-fastapi-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Linux/macOS
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your values:
   ```env
   APP_NAME=Secure API
   APP_ENV=dev
   APP_PORT=8000
   DEBUG=true
   ```

5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

   API available at `http://localhost:8000`

---

### Docker

```bash
docker-compose up --build
```

API available at `http://localhost:8001`

> The container runs as a non-root user for added security.

---

## API Reference

### Health

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Returns API status and environment |

**Response:**
```json
{
  "status": "ok",
  "env": "dev"
}
```

### Users — `/api/v1`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/users` | List all users |
| `GET` | `/api/v1/users/{user_id}` | Get user by ID |

Interactive docs available at:
- Swagger UI → `http://localhost:8000/docs`
- ReDoc → `http://localhost:8000/redoc`

---

## Screenshots

> Add screenshots here once the API is running with real data.

| Swagger UI | Health endpoint | Docker logs |
|---|---|---|
| *(coming soon)* | *(coming soon)* | *(coming soon)* |

---

## Testing

Run the full test suite:
```bash
pytest
```

With coverage report:
```bash
pytest --cov=app --cov-report=term-missing
```

---

## Security

- Passwords hashed with **bcrypt** and **Argon2** via Passlib
- Static analysis with **Bandit**
- Docker image runs as **non-root user**
- All settings loaded from environment variables — no hardcoded secrets
- Input validation enforced by **Pydantic v2** on all request bodies

---

## License

MIT © [YagoGomez83](https://github.com/YagoGomez83)
