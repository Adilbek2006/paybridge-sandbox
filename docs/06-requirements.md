# 6. Requirements Specification

Priorities use MoSCoW: **M** — Must (mandatory for the diploma), **S** — Should,
**C** — Could, **W** — Won't (this release). Every Must requirement has an acceptance
criterion that is checked by an automated test (`tests/acceptance/…`) or by a documented
manual check. "Owner" is the team member responsible for implementation; the other member
reviews.

## 6.1 Actors

| Actor | Description |
|---|---|
| Merchant developer (client system) | Calls the PayBridge API with a test API key |
| Customer (payer) | Pays on the provider-hosted checkout page (sandbox) |
| Administrator | Manages merchants and monitors transactions in the dashboard |
| Payment provider | Stripe (test mode), PayPal (sandbox), Mock provider |
| Merchant webhook endpoint | Receives PayBridge notifications |

## 6.2 Functional requirements

| ID | Requirement | Pri. | Acceptance criterion | Owner |
|---|---|---|---|---|
| FR-01 | The administrator can create a merchant and issue a test API key. The key is shown once and stored only as a hash. | M | After creation the plaintext key appears in the response exactly once; the database contains only its hash; a request with the key is authenticated. | Adilbek |
| FR-02 | All `/v1` endpoints require `Authorization: Bearer <key>`; a merchant can access only its own resources. | M | Request without a key → `401`; request for another merchant's payment → `404`; test covers both. | Adilbek |
| FR-03 | The client can create a payment (`POST /v1/payments`) with amount (minor units), currency, provider, description, return URL and metadata. | M | Valid request → `201` with `id`, `status=requires_action`, `checkout_url`; invalid amount/currency → `422` in RFC 9457 format. | Adilbek |
| FR-04 | The client can retrieve a payment by ID. | M | `GET /v1/payments/{id}` returns the current status and the list of status transitions. | Adilbek |
| FR-05 | The client can list payments with filters (status, provider, date range) and cursor pagination. | S | Filters return only matching records; `next_cursor` returns the next page without duplicates. | Adilbek |
| FR-06 | The client can cancel a payment that has not succeeded. | S | Cancel in `requires_action` → `canceled`; cancel in `succeeded` → `409`. | Adilbek |
| FR-07 | The client selects the provider per request (`stripe`, `paypal`, `mock`) or the merchant's default provider is used. | M | The same request body works with all three providers; the provider is recorded in the payment. | Adilbek |
| FR-08 | All `POST` endpoints require an `Idempotency-Key` header. Same key + same body → the stored response is returned; same key + different body → `422`; concurrent requests with one key create only one payment. | M | Test: 10 parallel identical requests → exactly 1 payment and 10 identical responses; changed body → `422`. | Adilbek |
| FR-09 | The mock provider supports deterministic scenarios: `success`, `decline`, `timeout`, `delayed_success`, `duplicate_webhook`. | M | For each scenario the final status and the number of webhooks match the scenario table in the test suite. | Nurbol |
| FR-10 | PayBridge receives Stripe and PayPal webhooks and verifies their signatures before processing. | M | Valid signed event → `200` and status update; tampered body or wrong signature → `400`, no state change, event logged as rejected. | Nurbol |
| FR-11 | Provider statuses are mapped to the unified state machine; illegal transitions are rejected and logged; duplicate provider events (same event ID) are ignored. | M | Mapping table unit-tested for every provider status; replaying the same event twice changes state once. | Nurbol (mapping), Adilbek (state machine) |
| FR-12 | A merchant registers a webhook URL; every payment status change produces an event that is delivered with an HMAC-SHA256 signature header `PayBridge-Signature: t=<ts>,v1=<sig>`. | M | The receiver in the test suite verifies the signature with the shared secret; event body follows the documented schema. | Nurbol |
| FR-13 | Failed deliveries are retried with exponential back-off (up to 8 attempts within 24 h); after that the delivery is marked `failed` and can be resent manually. | M | Fault-injection test with a receiver that fails 3 times → delivered on the 4th attempt; every attempt recorded with HTTP status and latency. | Nurbol |
| FR-14 | The client can make full and partial refunds (`POST /v1/payments/{id}/refunds`); the total refunded cannot exceed the payment amount. | M | Partial refund → `partially_refunded`; full → `refunded`; over-refund → `422`. Verified with mock and Stripe. | Adilbek (API, rules), Nurbol (PayPal refund call) |
| FR-15 | Every state change is written to an audit log (time, actor, old/new status, source). | S | Each transition in a test scenario has exactly one audit record. | Adilbek |
| FR-16 | The administrator can view payments, a payment timeline and webhook deliveries in a web dashboard and resend a failed delivery. | S | Manual check script `docs/manual-checks.md` passes; resend creates a new delivery attempt. | Adilbek |
| FR-17 | The dashboard shows daily totals by provider and status and exports payments to CSV. | S | CSV export for a date range contains exactly the payments returned by the API for the same filters. | Adilbek |
| FR-18 | `GET /health` (liveness) and `GET /ready` (database reachable) endpoints exist. | M | `/ready` returns `503` when the database is stopped. | Nurbol |
| FR-19 | A reconciliation job polls the provider for payments that stay in `processing` longer than 15 minutes. | C | A payment whose webhook was dropped reaches its final status through polling. | Nurbol |
| FR-20 | Adapter for a Kazakhstani provider (e.g. Freedom Pay, Halyk ePay). | W | — (future work) | — |

## 6.3 Non-functional requirements

| ID | Category | Requirement | Pri. | Acceptance criterion / measurement |
|---|---|---|---|---|
| NFR-01 | Performance | p95 latency of `POST /v1/payments` with the mock provider ≤ 300 ms at 50 requests/s for 5 min | M | Locust test on the reference machine (Section 9.3) |
| NFR-02 | Reliability | No duplicate payments under retries; no lost outbound events when the worker or the receiver fails | M | Metrics M2 and M3 equal 0 in the fault-injection test |
| NFR-03 | Security | API keys hashed; secrets only in environment variables; no card data stored; webhook signatures verified; merchant webhook URLs to private/loopback IP ranges rejected (SSRF, OWASP API7) | M | Security checklist in `docs/security-checklist.md` (OWASP API Top 10 2023) passes; secret-scanning in CI finds nothing |
| NFR-04 | Durability | Pending notifications survive a restart of the API or worker | M | Kill the worker during delivery → all events are delivered after restart |
| NFR-05 | Maintainability | A new provider is added by implementing one `PaymentProvider` interface without changing the payment module; line coverage of domain and provider modules ≥ 70% | M | Code review + coverage report in CI |
| NFR-06 | Usability / documentation | Interactive OpenAPI docs at `/docs`; a new developer can create a first sandbox payment within 15 minutes using the README | S | Timed walkthrough with ≥ 3 participants |
| NFR-07 | Portability | Runs with `docker compose up` on Windows, macOS and Linux | M | CI job builds and starts the stack; manual check on two OSes |
| NFR-08 | Observability | Structured JSON logs with request ID; every outbound delivery attempt is logged | S | Log sample shows request ID propagated from API to worker |

## 6.4 Unified payment state machine (used by FR-04, FR-06, FR-11, FR-14)

`requires_action → processing → succeeded → partially_refunded → refunded`;
`requires_action | processing → failed`; `requires_action → canceled`.
All other transitions are illegal. See the state diagram in Section 7.

## 6.5 Traceability (requirement → evidence → test)

| Requirement | Evidence (Section 2/3) | Test |
|---|---|---|
| FR-03…FR-07 | F1, A1 | `tests/acceptance/test_payments.py` |
| FR-08, NFR-02 | F1, A2, [S11] | `tests/acceptance/test_idempotency.py` |
| FR-09 | F2, A4 | `tests/acceptance/test_mock_scenarios.py` |
| FR-10…FR-13 | F1, A3, F4, [S7] | `tests/acceptance/test_webhooks.py`, fault-injection suite |
| NFR-01 | [S8] | `tests/load/locustfile.py` |
| NFR-03 | [G5, G7] | `docs/security-checklist.md` |
