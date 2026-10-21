# 2. Evidence of Relevance

The requirements of PayBridge are based on three kinds of evidence. Each finding below is
marked as **Verified** (supported by a cited source or by recorded interviews) or
**Assumption** (a hypothesis that the interviews or the evaluation must confirm or reject).

## 2.1 Analysis of available data: provider documentation

The team compared the official developer documentation of the two providers that will be
integrated. The differences below are what a client developer must handle separately when
integrating each provider directly.

| Aspect | Stripe (test mode) | PayPal (sandbox) | Consequence for a client developer |
|---|---|---|---|
| Idempotent retries | `Idempotency-Key` header on POST requests; keys up to 255 characters; keys may be pruned after at least 24 hours; reusing a key with different parameters returns an error [G1] | `PayPal-Request-Id` header; retention period varies by API and must be checked per endpoint [G4] | Two different retry mechanisms and lifetimes to understand and implement |
| Webhook authenticity | HMAC-SHA256 signature in the `Stripe-Signature` header with a timestamp; libraries use a default 5-minute tolerance to prevent replay attacks; raw body required [G2] | Either CRC32-based signature verification with a certificate, or a call to PayPal's verify-signature endpoint [G3] | Two different cryptographic verification procedures |
| Webhook retries | Up to three days with exponential back-off in live mode; in a sandbox only three retries over a few hours [G2] | Up to 25 attempts over 3 days, then the event is marked "Failed" [G3] | Different failure windows; sandbox behaviour differs from production |
| Ordering / duplicates | Delivery order is not guaranteed; the same event can be delivered more than once; event IDs must be tracked [G2] | Retries imply that duplicates are possible [G3] | The client must de-duplicate and must not rely on order |

**Finding F1 (Verified):** two widely used providers differ in every reliability-related
mechanism (retries, signatures, delivery windows). A developer who integrates both must
implement and test these mechanisms twice.

**Finding F2 (Verified):** Stripe's sandbox retries webhooks only three times over a few
hours, whereas live mode retries for three days [G2]. Sandbox testing therefore does not
reproduce production failure behaviour, which supports the need for a controllable mock
provider.

**Finding F3 (Verified):** card payments in Kazakhstan are now mostly cashless (cash
withdrawals ≈12.9% of card turnover in 2025, versus more than 50% in 2019) [G12], so
the number of businesses that must accept online payments is growing.

## 2.2 Analysis of the literature

- Practitioners avoid distributed transactions between services and instead coordinate state
  with asynchronous events written by application code, which is error-prone [S7].
- Idempotency must be designed explicitly into any system where messages can be retried [S11].
- Missing or outdated API specifications are a recurring problem for API consumers; a
  design-first OpenAPI contract helps [S4].

## 2.3 Discussions with potential users (interviews)

**Plan.** 3–5 semi-structured interviews (20–30 minutes each) with:

| # | Role (target user group) | Organisation type | Status |
|---|---|---|---|
| I1 | Backend developer who has integrated a payment provider | E-commerce / fintech company | Not yet conducted |
| I2 | Backend or full-stack developer | Small SaaS / startup | Not yet conducted |
| I3 | QA engineer who tests payment flows | IT company | Not yet conducted |
| I4 | Owner or IT person of a small online shop | Small business | Not yet conducted |
| I5 (optional) | Instructor of a backend / web development course | University | Optional, not yet conducted |

The interview guide and the record template are in `docs/evidence/interview-guide.md`.
Each interview is recorded as a separate file `docs/evidence/interview-I<n>.md`
(anonymised, with the participant's consent).

**Status on 21.10.2026.** No interviews have been conducted yet. The interview guide and
the record template are ready. Interviews I1–I4 are planned for 22.10–20.11.2026 (YouTrack
DIP-4, risk R10 in Section 10). Their results — one anonymised record per participant and a
table showing, for each hypothesis H1–H5, whether it was confirmed — will be reported at
Milestone 1 (21.11.2026).

Hypotheses to be tested by the interviews:

| Hypothesis | Related assumption |
|---|---|
| H1. Integrating a second provider takes as much effort as the first | A1 |
| H2. Duplicate charges / duplicate orders on retry have happened or are a real concern | A2 |
| H3. Missed or delayed webhooks have caused incorrect order statuses | A3 |
| H4. Reproducing declines / timeouts in provider sandboxes is difficult | A4 |
| H5. A single dashboard of transactions and webhook deliveries would be useful | — |

Until the interviews are completed, A1–A4 remain **assumptions**. Section 2.5 shows which
evidence each requirement relies on: FR-08…FR-13 are already supported by verified findings
F1, F2 and F4, so they do not depend on the interview results.

## 2.4 Verified findings vs. assumptions

| ID | Statement | Status | Evidence |
|---|---|---|---|
| F1 | Providers differ in retry, signature and webhook mechanisms | **Verified** | [G1–G4] |
| F2 | Sandbox webhook retries do not match production behaviour | **Verified** | [G2] |
| F3 | Card payments in Kazakhstan are predominantly cashless and the share keeps growing | **Verified** | [G12] |
| F4 | Event-based consistency is hard to implement correctly in application code | **Verified** (literature) | [S7, S9] |
| A1 | Developers spend significant effort on each additional provider | Assumption → H1 | Interviews |
| A2 | Duplicate charges on retries are a real risk for small teams | Assumption → H2 | Interviews |
| A3 | Lost webhooks cause wrong order statuses | Assumption → H3 | Interviews |
| A4 | A deterministic mock provider is valuable for QA | Assumption → H4 | Interviews |
| A5 | A unified API reduces client integration code by ≥40% | Assumption → metric M5 | Evaluation (Section 9) |

## 2.5 How the evidence informs the requirements

| Evidence | Requirement(s) |
|---|---|
| F1, A1 | FR-01…FR-06 (unified payment API), FR-07 (provider selection) |
| F1, A2, [S11] | FR-08 (idempotency keys), NFR-02 |
| F1, A3, F4 | FR-10…FR-13 (verified inbound webhooks, outbound notifications with retries) |
| F2, A4 | FR-09 (deterministic mock provider scenarios) |
| A5 | Evaluation metric M5 |
