# 11. Supervisor Feedback

**Supervisor:** Kamila Islyamovna Tanyrbergenova, Senior Lecturer.
Feedback is collected at review meetings and in GitHub PR comments. Each comment is recorded
with the team's decision and a link to the resulting change.

## 11.1 Review meetings

| # | Date | Format | Deliverables reviewed | Participants |
|---|---|---|---|---|
| 1 | 21.10.2026, 10:00 | In person, room 1.3.251 | Materials for the first submission: proposal and scope, role allocation, requirements, architecture and ADRs, API contract, prototype, YouTrack board; answers for the submission form | Supervisor, Adilbek, Nurbol |

## 11.2 Feedback log and decisions

| # | Deliverable | Supervisor's comment | Decision | Resulting change | YouTrack |
|---|---|---|---|---|---|
| 1 | Materials for the first submission (meeting 1) | No remarks were given. | The team continues with the plan in Section 10. | None required | DIP-15 |

Further comments from the next review meetings and from PR reviews will be added to this
table.

## 11.3 Topics for the next review

1. Is the scope (Stripe + PayPal sandbox + mock provider, no live payments) sufficient in
   engineering complexity for a two-person diploma project?
2. Is the revised allocation of responsibilities (Section 10.3) acceptable, given that it
   differs from the initial project application?
3. Is replacing "microservice architecture" with a modular monolith + worker (ADR-001)
   acceptable, given the evidence in [S7, S8]?
4. Are the evaluation metrics and the direct-integration baseline (Section 9) convincing?
5. Should a Kazakhstani payment provider be added as a stretch goal?
6. Progress of the user interviews (Section 2.3).
