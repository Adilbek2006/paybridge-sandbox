# 1. Project Proposal

## 1.1 Project title

PayBridge: REST API Service for Payment System Integration (Sandbox Environment)

## 1.2 Problem statement

Integrating payment providers (Stripe, PayPal, local PSPs) into a web application
requires dealing with different APIs, authentication flows, webhook formats and
retry logic for each provider separately. Small development teams spend significant
time re-implementing the same patterns — idempotency, signature verification,
delivery retries — for every new project.

## 1.3 Proposed solution

A self-hosted sandbox service with a single REST API that abstracts provider
differences. Developers test their integration once against PayBridge and switch
providers by changing one configuration value. The sandbox includes a deterministic
mock provider for automated testing without network calls.

## 1.4 Scope

In scope:

- Unified REST API for initiating payments, refunds and cancellations
- Idempotency-Key support on all state-changing endpoints
- Outbound webhook delivery with HMAC-SHA256 signatures and automatic retries
- Adapters for Stripe (test mode) and PayPal (sandbox)
- Deterministic mock provider for automated tests
- Admin dashboard for transaction monitoring
- OpenAPI 3.1 specification

Out of scope:

- Production deployment and real money processing
- Card data storage (PCI DSS scope is avoided by using provider-hosted pages)
- Kazakhstani local PSP adapters (planned for future work)

## 1.5 Expected outcomes

1. A running FastAPI service with passing automated tests
2. OpenAPI specification covering all endpoints
3. Verified integration with Stripe test mode and PayPal sandbox
4. Load test results showing baseline performance metrics
