# 9. Verification and Evaluation Plan

## 9.1 What must be demonstrated

The project aim (Section 1.4) is achieved if PayBridge (a) lets a client use three providers
through one API, (b) never creates duplicate payments on retries, (c) never loses a status
notification, (d) rejects forged webhooks, and (e) reduces client integration effort compared
with direct integration — at acceptable performance.

## 9.2 Test levels

| Level | Tool | Scope | Owner |
|---|---|---|---|
| Unit | pytest | State machine, status mapping tables, signature functions, back-off schedule | author of each module |
| Acceptance (API) | pytest + httpx/TestClient | One or more tests per Must requirement (Section 6), run in CI on every PR | Adilbek (FR-01…08, 14), Nurbol (FR-09…13, 18) |
| Integration with providers | pytest marked `@sandbox`, Stripe CLI `stripe trigger`, PayPal sandbox accounts | Real sandbox round-trip for create → pay → webhook → refund | Adilbek (Stripe), Nurbol (PayPal) |
| Fault injection | Custom receiver that returns 5xx/timeouts; `docker kill` of worker | FR-13, NFR-02, NFR-04 | Nurbol |
| Load | Locust (`tests/load/locustfile.py`) | NFR-01 | Nurbol |
| Security | OWASP API Top 10 checklist, tampered-signature tests, gitleaks in CI | NFR-03 | both |
| Usability | Timed "first payment" walkthrough with 3–5 developers + short questionnaire | NFR-06, M6 | both |

Current status (prob-period-1): 24 automated tests pass on the prototype
(unit + acceptance for FR-02, FR-03, FR-04, FR-06, FR-08, FR-09, FR-14); line coverage 96%.

## 9.3 Outcome metrics

| ID | Metric | Target | How measured |
|---|---|---|---|
| M1 | Share of Must requirements whose acceptance tests pass | 100% | CI report |
| M2 | Duplicate payments created in the idempotency stress test (100 keys × 10 concurrent retries) | 0 | Count of payments per key in the DB |
| M3 | Lost outbound events in the fault-injection test (1 000 events, receiver fails 30% of requests at random, worker killed twice) | 0 lost; ≥ 99% delivered within 5 min after the receiver recovers | Compare `outbox_events` with events logged by the receiver |
| M4 | Forged/tampered webhooks accepted | 0 of 100 | Security test suite |
| M5 | Client integration effort to support Stripe + PayPal: lines of client code and number of distinct integration concepts (endpoints, signature schemes, status vocabularies) | ≥ 40% less than baseline | Two reference client apps (see 9.5), counted with `cloc` |
| M6 | Time for a new developer to make the first sandbox payment using the README | ≤ 15 min (median) | Walkthrough with 3–5 participants |
| M7 | p95 latency of `POST /v1/payments` (mock provider) at 50 req/s for 5 min; error rate | ≤ 300 ms; < 1% | Locust report |
| M8 | Line coverage of domain + provider modules | ≥ 70% | pytest-cov in CI |

## 9.4 Measurement conditions

- **Reference machine:** a team laptop (to be recorded: CPU, RAM, OS) running
  `docker compose` with API (2 Uvicorn workers), worker (1 process) and PostgreSQL 16;
  Locust runs on the same machine. Each load test is repeated 3 times; the median is reported.
- **Provider latency is excluded** from M7 by using the mock provider; sandbox round-trips
  are measured separately and reported for information only.
- Fault-injection uses a fixed random seed so results are reproducible.
- All measurements are taken on the commit tagged for the corresponding pre-defense.

## 9.5 Baseline for comparison

**Baseline = direct integration.** The team will build two minimal reference "shop" clients
with identical functionality (create payment, receive status, refund) for Stripe and PayPal:

1. **Baseline client:** calls Stripe and PayPal APIs directly and implements both webhook
   verifications, both status mappings and its own retry/de-duplication logic.
2. **PayBridge client:** calls only the PayBridge API and verifies one signature.

M5 compares the two clients. M2–M4 are also run against the baseline client to show which
failure modes the baseline does not handle (e.g. the baseline without idempotency keys
creates duplicates under concurrent retries).

## 9.6 Evaluation report

Results will be presented in a table "metric — target — achieved — evidence link (CI run,
Locust report, test file)" at pre-defense 2 (partial) and at the final pre-defense (full).
