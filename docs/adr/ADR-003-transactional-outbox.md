# ADR-003: Transactional outbox for outbound notifications

- **Status:** Accepted (2026-10-20)
- **Context:** A payment status change must always result in a notification to the merchant
  (FR-12, NFR-02). Writing to the DB and calling the merchant (or a broker) in the same
  request is a dual write that can lose events if the process crashes between the two [S7].
- **Decision:** On every status change, insert an `outbox_events` row in the same
  transaction. A worker selects due rows with `FOR UPDATE SKIP LOCKED`, sends a signed HTTP
  POST, records a `delivery_attempts` row and reschedules failures with exponential back-off
  (30 s, 2 min, 10 min, 30 min, 1 h, 3 h, 6 h, 12 h; 8 attempts ≈ 24 h).
- **Consequences:** + no lost events; + no message broker to operate; – at-least-once
  delivery, so merchants must de-duplicate by `event.id` (documented in the API guide).
