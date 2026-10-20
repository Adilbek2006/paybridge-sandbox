# 10. Project Management and Risks

## 10.1 Tools and links

| Item | Link |
|---|---|
| Git repository | `https://github.com/Adilbek2006/paybridge-sandbox` |
| Submitted version (probation period 1) | tag `prob-period-1` → `https://github.com/Adilbek2006/paybridge-sandbox/tree/prob-period-1` |
| YouTrack project | `https://paybridge-se2406.youtrack.cloud/projects/DIP` (agile board "PayBridge") |
| Backlog source (importable) | `project/youtrack-tasks.csv` |
| Git workflow rules | `project/git-workflow.md` |

## 10.2 Way of working

- **One YouTrack task per meaningful work item** (`DIP-<n>`), with assignee, priority,
  due date, expected outcome and acceptance criteria. Status flow:
  `Open → In Progress → Review → Done`; a task is moved to *Done* only when its acceptance
  criteria are met and its PR is merged.
- **Branches** `DIP-<n>-short-name`; **commits** `DIP-<n>: <imperative summary>`.
- **Every change goes through a Pull Request** to `main`; the PR references the task,
  explains the change *in the author's own words*, and states how it was checked.
  The other team member reviews every PR before merge.
- Each student commits only from **their own GitHub account** with their own name/e-mail.
- Weekly team sync (Monday, 30 min); supervisor meeting every two weeks (Section 11).
- Pre-defense versions are tagged (`prob-period-1`, `pre-defense-1`, `pre-defense-2`,
  `final-pre-defense`); tags are never moved.

## 10.3 Allocation of responsibilities

The allocation was revised compared with the initial project application ("Adilbek —
frontend and reports; Nurbol — backend and microservices"). In an API-centric project the
backend is the core, so both students now own a substantial and separately assessable part
of the backend, and documentation is split evenly. Planned effort is balanced
(≈115 h vs ≈112 h in the current backlog).

| Area | Responsible (R) | Reviewer |
|---|---|---|
| Payment domain, state machine, idempotency, auth, data model | Adilbek | Nurbol |
| Stripe adapter, refunds | Adilbek | Nurbol |
| Admin dashboard, reports, CSV | Adilbek | Nurbol |
| PayPal adapter, mock provider | Nurbol | Adilbek |
| Inbound webhooks, outbox worker, retries | Nurbol | Adilbek |
| Docker, CI, load and fault-injection tests | Nurbol | Adilbek |
| Docs: Sections 1, 3, 6, 7, 10 | Adilbek | Nurbol |
| Docs: Sections 2, 4, 5, 8, 9 | Nurbol | Adilbek |
| Supervisor communication, Section 11, submissions | Adilbek (team representative) | Nurbol |

## 10.4 Milestones

Dates of pre-defenses are aligned with the official department schedule; the dates below are
the team's internal targets.

| Milestone | Target date | Content | Tag |
|---|---|---|---|
| MS0 Probation period 1 | 24.10.2026 | Analysis, requirements, architecture, API contract, prototype, plans | `prob-period-1` |
| MS1 Core platform | 21.11.2026 | PostgreSQL, Docker, CI, auth, idempotency, mock async webhooks, webhook ingest | — |
| MS2 Provider integrations | 19.12.2026 | Outbox worker, Stripe and PayPal adapters, refunds, dashboard | `pre-defense-1` (if scheduled) |
| MS3 Evaluation | 27.02.2027 | Reports, fault-injection and load tests, baseline clients, security checklist | `pre-defense-2` |
| MS4 Final | 04.2027 | Usability study, final report and explanatory note, demo | `final-pre-defense` |

## 10.5 Risks

| ID | Risk | Prob. | Impact | Mitigation / contingency | Owner |
|---|---|---|---|---|---|
| R1 | Stripe test-mode account cannot be opened from Kazakhstan or has limited features | Medium | High | Check in week 1 (DIP-27 starts with a spike). Fallback: official `stripe-mock` server and Stripe CLI fixtures; the adapter interface stays the same | Adilbek |
| R2 | PayPal sandbox limitations or regional restrictions | Medium | High | Create developer account early; fallback: second open sandbox provider with the same adapter interface | Nurbol |
| R3 | Providers change their APIs or webhook formats | Low | Medium | Pin SDK and API versions; contract tests per adapter | Both |
| R4 | Webhooks need a public HTTPS URL during local development | High | Low | Stripe CLI `listen --forward-to`, ngrok tunnel; mock provider for automated tests | Nurbol |
| R5 | Code generated with AI assistants is not fully understood by its author | Medium | High | Every PR description explains the code in the author's words; reviewer asks at least one question; short weekly "explain your PR" session | Both |
| R6 | Uneven contribution / one member unavailable (illness, exams) | Medium | High | Balanced backlog, weekly sync, YouTrack visibility; tasks re-assigned if a due date slips > 1 week; supervisor informed | Adilbek |
| R7 | Scope creep (extra providers, subscriptions) | Medium | Medium | MoSCoW priorities; Kazakhstani PSP adapter is explicitly *Won't* for this release | Adilbek |
| R8 | Committee cannot access repository or YouTrack | Low | High | Repository public (or committee added); access checked from a non-member account before every submission | Adilbek |
| R9 | Secrets (API keys) committed to Git | Low | High | `.gitignore`, `.env.example` with placeholders, gitleaks in CI; rotate any leaked sandbox key immediately | Nurbol |
| R10 | Too few interview participants | Medium | Medium | Contact list prepared from internship companies and alumni; online interviews allowed | Nurbol |

## 10.6 Dependencies

| Type | Dependency | Needed by |
|---|---|---|
| External | Stripe account (test mode), Stripe CLI | DIP-27 |
| External | PayPal developer account with sandbox business/personal accounts | DIP-28 |
| External | GitHub (repo, Actions), YouTrack instance | all |
| External | Interview participants | DIP-4 |
| External | Supervisor availability for reviews | DIP-15 and each milestone |
| Internal | DIP-20 (schema) → DIP-22, DIP-23; DIP-25 (ingest) → DIP-26 (outbox), DIP-28 (PayPal); DIP-26 → DIP-30 (dashboard deliveries); DIP-28 → DIP-33 (baseline client) | see `project/youtrack-tasks.csv` |

## 10.7 Status at probation period 1

**Completed:** proposal and scope, literature review (13 scientific + 18 technical sources),
comparison of 4 existing systems, technology comparison (4 decisions), requirements (20 FR,
8 NFR), architecture with 6 diagrams and 3 ADRs, OpenAPI 3.1 contract, runnable prototype
(24 passing tests), verification plan, backlog of 35 tasks.

**Known limitations:** in-memory storage; only the mock provider is wired; inbound webhooks
and the delivery worker are designed but not implemented; interview evidence is being
collected.

**Next steps:** MS1 tasks DIP-20 … DIP-25.
