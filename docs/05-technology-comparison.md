# 5. Technology Comparison

## 5.1 Decision 1 — Server platform

Options considered: Python/FastAPI, Node.js/Express, Go/Gin, Java/Spring Boot.

| Criterion | FastAPI | Express | Go/Gin | Spring Boot |
|---|---|---|---|---|
| Development speed | High | High | Medium | Low |
| Auto OpenAPI generation | Yes | No | No | Partial |
| Async support | Yes | Yes | Yes | Yes |
| Team familiarity | High | Medium | Low | Low |
| Ecosystem for payments | Good | Good | Limited | Good |

Decision: Python + FastAPI (ADR-002). Fastest to prototype, built-in OpenAPI generation,
good ecosystem. Sufficient performance for sandbox load.

## 5.2 Decision 2 — Data storage

Options: PostgreSQL, MySQL, SQLite, MongoDB.

| Criterion | PostgreSQL | MySQL | SQLite | MongoDB |
|---|---|---|---|---|
| ACID transactions | Yes | Yes | Yes | Partial |
| JSON support | Yes | Partial | No | Yes |
| Idempotency constraints | Yes | Yes | Yes | No |
| Production readiness | High | High | Low | High |

Decision: PostgreSQL 16 (ADR-002). Best ACID guarantees, supports unique constraints for
idempotency keys, widely used in payment systems.

## 5.3 Decision 3 — Component interaction (ADR-003)

Options: synchronous HTTP calls, message queue (RabbitMQ/Kafka), transactional outbox.

Synchronous delivery fails silently if the merchant webhook endpoint is down.
Message queues add infrastructure complexity for a two-person team.
Transactional outbox writes notifications to the same database transaction as the
state change — no message is lost even if delivery fails.

Decision: transactional outbox pattern with a separate worker process.

## 5.4 Decision 4 — Architecture style (ADR-001)

Options: microservices, modular monolith, single-module monolith.

Single module becomes unmaintainable quickly. Microservices require separate
deployments, distributed tracing and service discovery — too complex for two people.
Modular monolith keeps clear internal boundaries (could become services later)
while staying simple to run and test.

Decision: modular monolith + separate worker for outbox delivery.
Justified by Blinowski et al. (2022) and Laigner et al. (2021).
