# PayBridge

Diploma project — REST API service for payment system integration (sandbox environment).

## About

PayBridge provides a unified REST API to work with multiple payment providers (Stripe, PayPal).
The goal is to simplify payment integration for developers by handling idempotency,
webhook delivery and provider differences in one place.

This is a sandbox — no real money is involved.

## Team

| Name | Group | Role |
|---|---|---|
| Adilbek Zhetpyspayev | SE-2406 | Payment core, API, database, Stripe |
| Nurbol Amangeldinov | SE-2406 | PayPal, webhooks, Docker, CI, load tests |

Supervisor: Kamila Islyamovna Tanyrbergenova, Senior Lecturer

## Tech stack

- Python 3.12 + FastAPI
- PostgreSQL 16
- SQLAlchemy + Alembic
- Docker Compose
- GitHub Actions (CI)

## Project management

Tasks tracked in YouTrack (project DIP).
Git workflow rules: see project/git-workflow.md

## Quick start

```bash
cp .env.example .env
# fill in your credentials in .env
pip install -e .
uvicorn paybridge.main:app --reload
```

API docs available at http://localhost:8000/docs
