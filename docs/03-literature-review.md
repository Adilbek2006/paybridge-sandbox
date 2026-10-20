# 3. Literature Review

## 3.1 Method

Sources searched in IEEE Xplore, ACM Digital Library, SpringerLink and Google Scholar.
Keywords: REST API design, idempotency, payment gateway, microservices vs monolith, API testing.
Criteria: relevant to project decisions, peer-reviewed or official standard, published 2021-2026
(except foundational works). Result: 13 scientific sources, 18 technical sources.

## 3.2 Theme A — REST API design

Fielding (2000) defines REST constraints: statelessness, uniform interface, resource identification.
Kotstein and Bogner (2021) surveyed 8 experts on 82 REST rules — 28 rated highly important
for usability and maintainability. Bogner et al. (2023) showed that violating these rules
reduces API understandability in a controlled experiment. Coblenz et al. (2023) found that
design-first OpenAPI specs reduce integration errors.

Impact on PayBridge: API contract written first in OpenAPI 3.1, plural noun resource names,
correct HTTP status codes, errors in RFC 9457 Problem Details format.

## 3.3 Theme B — Idempotency and reliability

Helland (2012) argues all distributed operations must be idempotent because retries are
unavoidable. IETF Idempotency-Key draft standardizes the header. Garcia-Molina and Salem (1987)
introduced sagas for long-lived transactions with compensating actions. Laigner et al. (2021)
found teams avoid distributed commits and use async events instead, causing inconsistency.

Impact on PayBridge: Idempotency-Key required on all state-changing endpoints, payment modelled
as a state machine, outbox pattern for reliable webhook delivery.

## 3.4 Theme C — Architecture style

Blinowski et al. (2022) compared monolith vs microservices — monolith performed better on
single machine, microservices not suitable for small systems. Laigner et al. (2021) add that
data management across services is the hardest microservices problem.

Impact on PayBridge: modular monolith + separate worker instead of microservices.
Keeps system manageable for a two-person team while maintaining clear module boundaries.

## 3.5 Theme D — API testing

Golmohammadi et al. (2023) surveyed 92 papers — external dependencies are the main testing
obstacle. Kim et al. (2022) compared 10 test tools on 20 services — coverage still limited.

Impact on PayBridge: providers isolated behind interfaces, replaced by deterministic mock
provider in tests. Hand-written acceptance tests derived from requirements.

## 3.6 Theme E — Payment APIs and security

OWASP API Security Top 10 (2023): broken auth, object-level auth, SSRF through callback URLs
are most relevant risks for PayBridge. PCI DSS v4.0 requires cardholder data protection —
avoided by using provider-hosted payment pages, PayBridge never receives card numbers.

## 3.7 Summary table

| # | Source | Key finding | Use in PayBridge |
|---|---|---|---|
| S1 | Fielding (2000) | REST architectural constraints | API design basis |
| S2 | Kotstein & Bogner (2021) | 28 REST rules highly important | Naming and status codes |
| S3 | Bogner et al. (2023) | Rule violations reduce understandability | OpenAPI review checklist |
| S4 | Coblenz et al. (2023) | Design-first specs reduce errors | Design-first approach |
| S5 | Golmohammadi et al. (2023) | External deps hinder testing | Mock provider |
| S6 | Kim et al. (2022) | Tool coverage still limited | Hand-written acceptance tests |
| S7 | Laigner et al. (2021) | Async events cause inconsistency | Outbox pattern |
| S8 | Blinowski et al. (2022) | Monolith better for small systems | Modular monolith |
| S9 | Daraghmi et al. (2022) | Enhanced saga higher throughput | Compensation logic |
| S10 | Garcia-Molina & Salem (1987) | Saga pattern | Payment workflow |
| S11 | Helland (2012) | Idempotence is a design requirement | Idempotency-Key |
| S12 | Rastogi et al. (2023) | Open banking APIs support inclusion | Relevance argument |
| S13 | Adireddy (2024) | Keys + reconciliation reduce duplicates | Supporting evidence |
