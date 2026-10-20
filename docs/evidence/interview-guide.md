# Interview Guide — PayBridge

**Duration:** 20–30 minutes. **Format:** online call or in person.
**Interviewer:** one team member; the other takes notes (alternate roles).

## Before the interview
- Explain the purpose: "We are building a diploma project — a service that lets developers
  integrate several payment providers through one API in a test environment."
- Ask for consent to take notes. No company secrets, no real customer data.
- Record only the role, experience and organisation type. Do not record personal data.

## Questions

**A. Background**
1. What is your role, and how many years of experience do you have?
2. Which payment providers have you integrated or tested (Stripe, PayPal, Kaspi, Halyk ePay,
   Freedom Pay, CloudPayments, etc.)?

**B. Integration effort (H1)**
3. How long did the first integration take? And the second provider?
4. What parts were the most time-consuming (authentication, statuses, webhooks, refunds, testing)?

**C. Reliability (H2, H3)**
5. Have you seen a payment or order created twice because of a retry or double click? How was it handled?
6. Have you had webhooks that were missed, delayed or delivered twice? What was the effect?
7. Do you verify webhook signatures? Was it difficult?

**D. Testing (H4)**
8. How do you test declined cards, timeouts and refunds? What is hard to reproduce in a sandbox?

**E. Monitoring (H5)**
9. How do you find out the current status of a payment and whether a notification was delivered?

**F. Solution feedback**
10. (Show the API example from Section 8.) Would one API for several providers be useful to you? What is missing?
11. Which three features would matter most to you?

---

# Interview record template (copy to `interview-I<n>.md`)

| Field | Value |
|---|---|
| Interview ID | I_ |
| Date | __.10.2026 |
| Interviewer / note-taker | |
| Participant role | |
| Experience (years) | |
| Organisation type | |
| Providers used | |

**Key answers (short notes per question block A–F):**

**Quotes worth citing (anonymised):**

**Hypotheses:** H1 ☐ confirmed ☐ rejected ☐ unclear · H2 ☐ ☐ ☐ · H3 ☐ ☐ ☐ · H4 ☐ ☐ ☐ · H5 ☐ ☐ ☐

**Impact on requirements (new / changed / reprioritised):**
