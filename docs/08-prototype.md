# 8. UX / Prototype

PayBridge is an API-first service: its main "users" are client systems. The prototype
therefore consists of (1) the design-first **OpenAPI 3.1 contract**, (2) **examples of API
requests and responses** produced by the running prototype, (3) the **outbound webhook
format**, and (4) a **low-fidelity mockup** of the admin dashboard.

| Prototype material | Location |
|---|---|
| OpenAPI 3.1 specification (validated with `openapi-spec-validator`) | `api/openapi.yaml` |
| Runnable prototype (FastAPI, in-memory storage, mock provider) | `src/paybridge/` — run with `uvicorn paybridge.main:app --app-dir src` |
| Interactive documentation of the prototype | `http://localhost:8000/docs` |
| Dashboard mockup | `docs/prototype/dashboard-mockup.html` / `.png` |

## 8.1 Key scenario 1 — create a payment

```http
POST /v1/payments HTTP/1.1
Authorization: Bearer pb_test_demo_key_123
Idempotency-Key: 7c2f0a4e-9a1b-4f55-8f0e-2d6b1c3e9a10
Content-Type: application/json

{ "amount": 150000, "currency": "KZT", "provider": "mock",
  "description": "Order #1042", "return_url": "https://shop.example/return",
  "metadata": { "order_id": "1042" } }
```

Response `201 Created` (actual output of the prototype):

```json
{
  "id": "pay_E6NM1O1NN8DWZHD8923AEPRDOT",
  "object": "payment",
  "status": "succeeded",
  "amount": 150000,
  "currency": "KZT",
  "amount_refunded": 0,
  "provider": "mock",
  "provider_payment_id": "mock_pay_E6NM1O1NN8DWZHD8923AEPRDOT",
  "checkout_url": null,
  "description": "Order #1042",
  "metadata": { "order_id": "1042" },
  "created_at": "2026-10-20T08:28:34.650552Z",
  "updated_at": "2026-10-20T08:28:34.650648Z"
}
```

With `"provider": "stripe"` or `"paypal"` the response has `status: "requires_action"`
and a `checkout_url` to which the client redirects the payer (see the example in
`api/openapi.yaml`). The client code is identical for all providers.

## 8.2 Key scenario 2 — safe retry (idempotency)

Sending **the same request with the same key** again returns `201` with **the same
payment ID** — no second payment is created. Reusing the key with a **different body**:

```json
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json

{ "type": "https://paybridge.dev/errors/idempotency-key-reused",
  "title": "Idempotency key reused with different parameters",
  "status": 422,
  "detail": "The key '7c2f0a4e…' was used for a request with a different body" }
```

## 8.3 Key scenario 3 — payment status and history

`GET /v1/payments/pay_E6NM1O1NN8DWZHD8923AEPRDOT` returns the payment plus its timeline:

```json
"status_history": [
  { "from_status": null,              "to_status": "requires_action", "source": "api" },
  { "from_status": "requires_action", "to_status": "processing",      "source": "provider" },
  { "from_status": "processing",      "to_status": "succeeded",       "source": "provider" }
]
```

## 8.4 Key scenario 4 — refund and illegal operation

```http
POST /v1/payments/pay_E6NM1O1NN8DWZHD8923AEPRDOT/refunds
Idempotency-Key: d1e2f3a4-0000-4000-8000-000000000001
{ "amount": 50000 }
```
→ `201 { "payment_id": "pay_E6NM…", "status": "partially_refunded", "amount_refunded": 50000 }`

Trying to cancel this payment afterwards →
`409 { "title": "Invalid state transition", "detail": "Cannot move payment from partially_refunded to canceled" }`

## 8.5 Key scenario 5 — QA test with the mock provider

| `mock_scenario` | HTTP result | Final status | Purpose |
|---|---|---|---|
| `success` | 201 | `succeeded` | Happy path |
| `decline` | 201 | `failed` | Declined card |
| `delayed_success` | 201 | `processing` → `succeeded` via simulated webhook (next stage) | Asynchronous confirmation |
| `timeout` | 502 | — | Provider unavailable |
| `duplicate_webhook` | 201 | `succeeded`; the same webhook is sent twice (next stage) | De-duplication check |

## 8.6 Outbound notification to the merchant (contract)

```http
POST https://shop.example/paybridge/webhook
Content-Type: application/json
PayBridge-Signature: t=1792491402,v1=5f0c…e9a1

{ "id": "evt_01JB7ZB4F0S8Q6M2W1X3Y5Z7AB",
  "type": "payment.succeeded",
  "created_at": "2026-10-20T10:16:42Z",
  "data": { "payment": { "id": "pay_01JB7Z6Q…", "status": "succeeded",
            "amount": 150000, "currency": "KZT", "provider": "stripe",
            "metadata": { "order_id": "1042" } } } }
```

The merchant verifies `v1 = HMAC-SHA256(signing_secret, "<t>.<raw body>")`, rejects
timestamps older than 5 minutes, de-duplicates by `id`, and replies `2xx` within 10 s.
Otherwise PayBridge retries (ADR-003).

## 8.7 Admin dashboard mockup (FR-16, FR-17)

![Dashboard mockup](prototype/dashboard-mockup.png)

The dashboard shows key indicators, filters, the payment list, the status timeline of a
selected payment with the source of every change, and the delivery history with a
"Resend" action.

## 8.8 Prototype limitations at this stage

- Storage is in memory (PostgreSQL, Alembic migrations — next milestone).
- Only the mock provider is wired; the Stripe and PayPal adapters are planned tasks.
- Inbound webhooks and the outbox worker are specified in the contract but not yet implemented.
