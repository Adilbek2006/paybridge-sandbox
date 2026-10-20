# ADR-002: Python 3.12 + FastAPI and PostgreSQL 16

- **Status:** Accepted (2026-10-20)
- **Context:** Requirements NFR-05/06 (maintainability, OpenAPI documentation), FR-08
  (concurrency-safe idempotency), FR-12 (atomic outbox). Alternatives: Spring Boot, NestJS;
  MySQL, MongoDB (see Section 5).
- **Decision:** FastAPI with Pydantic models; SQLAlchemy 2 + Alembic migrations; PostgreSQL 16.
- **Consequences:** + the OpenAPI document is generated from the same models used for
  validation; + `INSERT … ON CONFLICT`, `SKIP LOCKED`, JSONB in one engine;
  – Python is slower than Java for CPU-bound work (not a bottleneck: the service is I/O-bound).
