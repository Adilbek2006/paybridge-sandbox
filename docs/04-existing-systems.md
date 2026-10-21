# 4. Analysis of Existing Systems

## 4.1 Method

Four systems were selected for comparison: Stripe, PayPal, Hyperswitch and Active Merchant.
Selection criteria: widely used in industry, publicly documented API, available sandbox.
Each system is evaluated against 8 criteria relevant to PayBridge goals.

## 4.2 Systems overview

Stripe — cloud payment platform with REST API, excellent documentation and test mode.
Handles idempotency, webhooks and retries internally but requires Stripe-hosted infrastructure.

PayPal — global payment platform with REST API and sandbox environment.
Supports standard payment flows; webhooks use a different, certificate-based
signature scheme and a different retry policy than Stripe [G3].

Hyperswitch — open-source payment orchestration layer (Juspay, 2023).
Supports 50+ connectors but is complex to self-host for a small team.

Active Merchant — Ruby library for payment abstraction (Shopify).
Client-side only, no webhook delivery, no idempotency built in.

## 4.3 Comparison table

| Criterion | Stripe | PayPal | Hyperswitch | Active Merchant |
|---|---|---|---|---|
| Unified API across providers | No | No | Yes | Partial |
| Built-in idempotency | Yes | Partial | Yes | No |
| Signed webhook delivery | Yes | Partial | Yes | No |
| Sandbox / mock for testing | Yes | Yes | Yes | No |
| Self-hostable | No | No | Yes | Yes (lib) |
| Open source | No | No | Yes | Yes |
| Small team setup complexity | Low | Low | High | Low |
| API documentation quality | Excellent | Good | Good | Fair |

## 4.4 Baseline: direct integration

The alternative to PayBridge is integrating each provider directly.
Each integration requires separate idempotency logic, webhook parsing and retry handling.
For two providers this doubles the implementation effort and creates inconsistent error handling.

## 4.5 Gap

No existing system combines: self-hosted + open source + sandbox-first + built-in idempotency
+ signed webhooks + small team setup. PayBridge fills this gap for the sandbox stage.
