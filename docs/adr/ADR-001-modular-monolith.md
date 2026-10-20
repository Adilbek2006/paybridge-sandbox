# ADR-001: Modular monolith with a separate worker

- **Status:** Accepted (2026-10-20)
- **Context:** The original project application described a "microservice architecture".
  The system has one bounded context (payments), a two-person team, and sandbox-level load.
  Benchmarks show monoliths outperform microservices on a single machine and that
  microservices are not the best fit for small systems [S8]; distributed data management is a
  major source of complexity [S7].
- **Decision:** Build one deployable API application with strict internal modules
  (auth, payments, refunds, providers, webhooks, notifications, admin) and one separate worker
  process. Modules communicate through Python interfaces, not HTTP.
- **Consequences:** + local ACID transactions, simpler testing and deployment; + module
  boundaries allow extracting the notification worker or adapters into services later;
  – the API and worker scale together with the database.
