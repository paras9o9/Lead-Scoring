
# HobbyFi Copilot: AI-CRM Assistant for Vendor Portal
### AI Engineer Intern Assessment — Submitted by Paras Sharma

---

## 1. Architecture Overview

The HobbyFi Copilot is designed as a **router-based multi-agent system** rather than a single monolithic agent, since vendor queries span two fundamentally different risk profiles: read-only information retrieval and write operations that mutate CRM data. Separating these into distinct agents backed by typed, scoped tools ensures the LLM decides *what* the vendor wants, while deterministic code decides *how* it is executed — a critical safety property given the requirement that "write access is only executed on vendor approval."

**Core components:**

- **Intent Router Agent** — Classifies incoming vendor queries into READ or WRITE, and further into specific sub-intents (e.g., `read_revenue`, `read_trial_users`, `write_extend_trial`). This layer combines a lightweight ML classifier (TF-IDF + LinearSVC, calibrated) with LLM-based entity extraction for parameters like `vendor_id`, `sport`, `date_range`, and `user_id`.
- **Query Agent (read-only)** — Invokes scoped tools such as `getRevenue(vendorId, dateRange)` or `listTrialUsers(vendorId, sport)` against read-optimized views, always injecting `vendor_id` from the authenticated session rather than trusting it from the LLM output.
- **Action Agent (write)** — Builds a structured change payload (e.g., `updateMembershipDate`, `extendTrial`, `cancelSubscription`) but never executes directly. It hands the payload to a workflow that requires explicit vendor approval before execution.
- **Guardrail Layer** — Sits between LLM output and tool execution, validating scope, business rules, and confidence thresholds before any action proceeds.
- **Response Formatter** — Converts raw tool outputs into natural, concise vendor-facing language, citing record counts/IDs where relevant.

**High-level flow:**

```
Vendor Query → Intent Router Agent → [READ path] → Query Agent → Tool Call → Formatted Response
                                    → [WRITE path] → Action Agent → Guardrail Checks → Approval Workflow (suspend) → Vendor Approves → Tool Execution → Audit Log → Response
```

This design keeps the LLM's role narrow (intent understanding, entity extraction, natural language generation) while all business-critical logic — data access, mutation, and approval — remains in code, which is easier to test, audit, and reason about than a single agent generating and executing SQL directly.

---

## 2. Tools & Frameworks

Since HobbyFi has standardized on **Mastra**, the architecture is built natively on its primitives rather than introducing a second framework like LangChain or LlamaIndex on top, which would add redundant complexity without clear benefit.

| Layer | Choice | Rationale |
|---|---|---|
| Agent orchestration | Mastra (agents, tools, workflows) | Native TypeScript framework already in use at HobbyFi; provides agents, tools, memory, and workflows in one stack |
| LLM provider | OpenAI/Anthropic via Mastra's model router | Model-agnostic; easy to swap for cost/latency tuning |
| Intent pre-classifier | TF-IDF + LinearSVC (calibrated) | Lightweight, fast, interpretable classifier for the 8 core intents; runs before the LLM to reduce hallucination risk in tool selection |
| Vector store (semantic memory) | LibSQL / pgvector | Integrates directly with Mastra's memory module for semantic recall across sessions |
| Primary data store | PostgreSQL (mock CRM schema) | Relational integrity for vendors, users, memberships, and transactions |
| Observability | Mastra Studio / built-in tracing | Inspect agent runs, memory state, and tool calls during development and demos |

**Why not LangChain/LlamaIndex:** Mastra already ships RAG, memory, and workflow primitives comparable to these frameworks. Stacking an additional framework on top would duplicate functionality and increase maintenance surface without a corresponding capability gain — a deliberate simplicity choice, not an oversight.

**Mock Data Schema** (used to ground tool definitions and guardrail logic):

- `vendors(vendor_id, name, sport_category, city)`
- `users(user_id, name, vendor_id, signup_date, status)`
- `memberships(membership_id, user_id, vendor_id, start_date, end_date, plan_type)`
- `trials(trial_id, user_id, vendor_id, trial_start, trial_end, sport)`
- `transactions(txn_id, vendor_id, user_id, amount, date)`
- `audit_log(action_id, vendor_id, actor, action_type, payload, approved_by, timestamp)`

Every tool takes `vendor_id` as a mandatory, session-injected parameter — never an LLM-controlled field — which is the first layer of defense against cross-tenant data leakage.

---

## 3. Memory Strategy

The Copilot uses Mastra's layered memory system: **working memory** for active-session state, and **semantic/long-term memory** for cross-session recall.

- **Thread-scoped memory:** Each vendor's conversation is isolated by `vendor_id` as the thread key, preventing memory bleed between different vendors sharing the platform.
- **Working memory:** Holds transient state such as "pending trial extension for user X awaiting approval," so context isn't lost mid-approval-flow across turns.
- **Semantic recall:** Embeds past queries and resolutions so the Copilot can handle follow-ups like "same as last time" without replaying full conversation history.
- **Retention policy:** Old session data is pruned on a TTL basis, and sensitive PII (e.g., raw payment details) is explicitly excluded from long-term embedding storage to limit exposure in semantic search results.

This layered approach balances conversational continuity (which vendors expect from a "copilot") against the data-isolation requirements inherent to a multi-tenant CRM.

---

## 4. Guardrails Framework

Guardrails are organized into three layers — input, execution, and output — mapping directly to where risk enters the system.

**Input validation:**
- Reject or flag cross-vendor access attempts (e.g., "show me vendor Y's revenue") via a scope check before the LLM reasons about the query.
- An intent-classification confidence gate: queries are pre-classified using a calibrated TF-IDF + LinearSVC model; if confidence falls below a tuned threshold, the system responds with a clarification request instead of guessing the intent.

**Execution validation (business rules):**
- Hard-coded constraints enforced in code, not left to LLM judgment — e.g., trial extensions capped at 30 days, membership dates cannot be backdated.
- Human-in-the-loop for all writes: every write action generates a diff/preview (e.g., "Extend trial for user Alex from 7 to 14 days — approve?") and executes only after explicit vendor confirmation.

**Output guardrails:**
- Redact PII not relevant to the specific query.
- Constrain responses strictly to the requesting vendor's own data, even if an underlying tool call somehow returns broader results.
- All write actions are logged to `audit_log` with actor, payload, and approver for full traceability.

**Empirical validation of the confidence-gating guardrail:** A prototype intent classifier was built and tested (TF-IDF + LinearSVC, calibrated via `CalibratedClassifierCV` with sigmoid scaling) on a labeled dataset of 160-200 sample vendor queries across the 8 core intents.

- Baseline (uncalibrated) confidence scores from LinearSVC's raw decision function were found to be unreliable for threshold-based gating, since SVM margins are not true probabilities. This caused valid queries to be incorrectly flagged for clarification.
- After calibration, the model achieved ~92-97% accuracy (varying with dataset balance) with properly scaled confidence scores, allowing a meaningful threshold (tuned between 0.3-0.5 depending on desired friction) to separate genuine queries from ambiguous or nonsensical ones.
- A threshold-sensitivity analysis showed a direct tradeoff: lower thresholds (0.3-0.4) reduce vendor friction but risk occasional misrouted actions, while higher thresholds (0.6-0.7) are safer but increase clarification prompts. This is treated as a business decision, not purely an accuracy optimization.

This experiment demonstrates that "guardrails" in this system are not just prompt instructions, but a measurable, tunable ML component with quantified precision/recall per intent — directly addressing the evaluation criterion on guardrails with empirical evidence rather than description alone.

---

## 5. Workflow Orchestration

Write operations are modeled as a **Mastra Workflow with a suspend/resume step**, since a write action cannot complete within a single conversational turn — it must pause for vendor approval and resume upon confirmation.

**Workflow steps:**

1. Receive vendor query; run Intent Router Agent (calibrated classifier + entity extraction).
2. If **READ**: invoke the corresponding scoped read tool, format the result, respond immediately.
3. If **WRITE**: Action Agent constructs the change payload; guardrails validate business rules and confidence; workflow generates a human-readable confirmation prompt and **suspends** execution.
4. Vendor approves or rejects the action via the portal UI; the workflow **resumes** based on this signal.
5. On approval: execute the tool call, write an entry to `audit_log`, and respond with confirmation. On rejection: discard the payload and respond accordingly, with no data mutation.

This suspend/resume pattern is a first-class primitive in Mastra workflows, and using it explicitly (rather than simulating approval with ad-hoc prompt engineering) ensures the approval gate is enforced structurally, not just suggested to the LLM — making it far harder to bypass through prompt injection or unusual phrasing.

---

## 6. Limitations & Future Work

- The current intent classifier was validated on a synthetic dataset (160-200 queries); production deployment would require real vendor query logs to retrain and validate against actual usage patterns and vocabulary.
- Two intents (`read_membership_status` and `read_transactions`) showed higher confusion due to overlapping vocabulary ("show," "list," "members"); this was partially mitigated with additional labeled examples, though a more robust fix would involve keyword-weighted features or a larger, rebalanced dataset.
- For significantly higher accuracy at scale, a fine-tuned lightweight transformer (e.g., DistilBERT) could replace the TF-IDF/SVM classifier, trading some latency and deployment simplicity for improved generalization on unseen phrasing.
- A full RAG layer for unstructured vendor FAQs or class descriptions was scoped but not implemented in this assessment; Mastra's native retrieval primitives would be the natural extension point.

---

*Supporting artifacts: intent classifier notebook, labeled query dataset (160-200 samples), confusion matrix, and calibration comparison are available as a notebook link [https://colab.research.google.com/drive/1b_HCPfXUB0NpP1YdzOt2_xcCtLgQ783H?usp=sharing].*
