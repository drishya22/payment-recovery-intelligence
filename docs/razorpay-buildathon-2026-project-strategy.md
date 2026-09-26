# Razorpay AI Buildathon 2026 — Project Strategy Report
**Prepared for:** 10–11 day build window, deadline Sept 5, 2026
**Posture:** Skeptical senior product/fintech advisor. Verified facts are marked (V), my inference/analysis is marked (I), my recommendation is marked (R).

---

## 0. Executive Conclusion

**(R)** Kill your Dispute Investigator idea as originally scoped. Keep Reconciliation Investigator as a strong, safe second choice. But my top recommendation is a **third idea that sits inside Track 3 (AI Revenue Recovery)**: a **Payment Degradation → Root Cause → Bounded Recovery Agent** — literally the first example Razorpay lists under that track. It is less saturated than dispute automation, more architecturally ambitious than plain reconciliation matching, and it maps almost line-for-line onto the official "bar" language Razorpay published for the track.

This isn't a hunch — it's grounded in the actual competition page (fetched directly, not summarized secondhand) and in competitive research across ~15 real products. Details below.

---

## 1. Competition Analysis — verified facts (V)

I fetched `razorpay.com/buildathon` directly. Key facts that change your framing:

- **This is a hiring funnel, not a generic hackathon.** It selects Razorpay's next "AI Builder Interns" — ₹75,000/month, 6 or 12 months, in-person Bangalore from September. Submission = public GitHub repo + 5-minute pitch video + architecture write-up + "what broke and how you recovered." Shortlisted builders go straight to a panel — no aptitude test, no GD.
- **Judging signals explicitly named** (from secondary sources describing the panel rubric, consistent with the track "bar" language): *AI Judgment* — was AI/LLM/agent usage appropriate, not forced — and *Failure Recovery* — how you found and handled a real runtime failure. This means your pitch video needs an honest "here's what broke" moment. Don't hide it — it's a scored dimension.
- **Track bars, verbatim intent, per track:**
  - **Track 1 (Growth & Agentic Commerce):** "Every money action explainable, bounded and gated. Show the audit trail and one failure handled gracefully."
  - **Track 2 (Risk Manager):** "Honest metrics including false-positive cost. Strictly defense-only: anything offense-capable is disqualified."
  - **Track 3 (Revenue Recovery):** "Don't just identify the problem. Show measured money recovered across a batch, with compliant escalation, stopping rules, and an audit trail." Explicit example #1: *"Payment degradation → root cause → recovery action."*
  - **Track 4 (Finance Controller):** "Throughput plus measured accuracy plus an honest exception list. One cherry-picked match proves nothing." Requirement: close one finance-ops loop across a **50+ record batch of synthetic data**, reporting match rate and unresolved exceptions. Razorpay's own stated rationale: *"verification capacity, not generation speed, is the bottleneck. Reconciliation, settlement and forecasting are still done by hand."*
  - **Track 5 (Open):** same bar for execution, reliability, depth — no leniency for being "creative."

**(I) What this tells you about judging:** every track bar rewards the same three things — (1) an audit trail for every automated action, (2) honest, held-out evaluation (not cherry-picked demos), (3) a bounded/gated action space with explicit stopping rules. This is a much stronger and more specific signal than "build something cool with AI." Whatever you pick, your differentiator should be **rigor of evaluation and gating**, not feature count.

---

## 2. Competitive Landscape — what I actually found

### A. Dispute / chargeback automation (your idea D) — **mature, well-funded, hard to differentiate**

**Justt** (V): AI-native chargeback platform, $100M+ raised, named a Forbes Fintech 50 company in 2026, serves 250+ enterprise merchants and 80,000+ SMBs. It already does the *entire* pipeline you described for idea D and further: pulls data from 500+ sources and 50+ PSPs, does entity/context enrichment (IP, device ID, order history), uses "Dynamic Arguments" to auto-select the strongest evidence per case, A/B-tests argument phrasing across millions of prior disputes for continuous improvement, integrates pre-chargeback alert networks (Ethoca/Verifi) to stop disputes before filing, and fully automates submission — not just recommendation. It just added an integration with Recurly (Aug 2026) specifically to pull subscription context automatically.

**Chargeflow, Chargeback Gurus, Chargebacks911, Justt's other competitors** (I, based on general market structure): occupy the same automated-evidence-collection-and-representment space at varying scale.

**(I) Verdict on D as originally scoped:** Your instinct to be suspicious was correct. The "investigate evidence, recommend contest/accept, produce structured evidence package, require human approval" pipeline is *already Justt's core product*, done at a scale (500+ data sources, millions of historical disputes for A/B-tested phrasing) a 10-day student build cannot approach. Building a worse, thinner version of an existing $100M product is a weak hackathon story, and it's a weak "I understood the problem" story too — because the real hard part (data enrichment breadth, phrasing optimization, issuer-specific tailoring) isn't something you can meaningfully attempt in the time you have.

**(I) Where a narrower version could still work:** Track 2's official bar wants "a working detector, verifier or auto-responder for one class of loss, with measured precision and recall on a held-out test set." That's a classifier problem, not an investigation-and-narrative problem. If you still want the Risk track, the defensible move is to build a **"should we even contest this chargeback" triage classifier** (accept / contest / escalate-to-human) evaluated with precision/recall/false-positive cost on a labeled synthetic set — not an evidence-writing engine. That's honest, measurable, and doesn't compete with Justt's actual moat (representment quality at scale).

### B. Reconciliation / financial investigation (your idea C) — **more room than you'd guess, but not empty**

**Razorpay's own reconciliation tooling** (V, from razorpay.com and third-party breakdowns): Razorpay already gives merchants transaction-level settlement reports keyed by `settlement_id`, refund/fee breakdowns, and (via RazorpayX Smart Collect) automated matching of *inbound bank-transfer collections* to customer identifiers, reportedly saving "60+ man-hours per week" for some merchants. **Critically, this reconciles Razorpay's own settlement batches against itself** — it does not reconcile across a merchant's *other* systems (ERP/Tally, multiple PSPs, marketplace payouts, GST/TDS filings, bank statement idiosyncrasies). That gap is real and is the one your idea should target — but it's not an undiscovered gap.

**HighRadius** (V): enterprise Record-to-Report platform, 200+ "R2R agents," 95%+ auto-match rates, targets SAP/Oracle/NetSuite-scale companies. This is GL/bank reconciliation for large enterprises — not payment-gateway-specific, not India-compliance-specific, not aimed at your buildathon's synthetic-data / SMB-merchant framing.

**Recko** (V): Bangalore-founded (2017), built exactly the "multi-source payment reconciliation" product you're describing — ingesting payment gateways, marketplaces, logistics, ERPs, and payout processors to automate matching and exception detection. Customers included Deliveroo, Meesho, PharmEasy. **Acquired by Stripe in 2021** specifically to add this capability to Stripe's product stack. This is strong evidence the problem is real *and* that a well-executed version of it is acquisition-worthy — but also proof the "generic multi-source reconciliation" framing has already been built, sold, and folded into a $95B company.

**TransactIG and ReconPe** (V, both current 2026 India-specific products): This is the part you most need to see. These are *live products right now* doing almost exactly what you sketched for idea C:
- TransactIG explicitly reconciles Razorpay/PayU/Amazon Pay/Flipkart/Zomato/Swiggy settlements against order records, plus India-specific logic (TDS section-level matching under 194C/194J/194H/194Q, GSTR-2B vs purchase register, NACH batch disaggregation). Customer-reported results: match rates moving from 51% to 88% automated within 90 days, cycle time from 3 weeks to 3 days.
- ReconPe uses AI to *propose* a matching rule set from raw data, and for every flagged exception generates a plain-language explanation of the likely cause plus a severity/financial-impact score — i.e., almost exactly your "evidence for the finance operator" and "prioritize exceptions" requirements.

**(I) Verdict on C:** Kill the *generic* "AI-powered reconciliation investigation engine" framing — it now has direct, current, India-specific competitors doing this commercially. But don't fully kill the category, because Track 4's bar is explicitly written around this exact workflow (50+ record batch, match rate, honest exception list) — Razorpay is *asking* for this. The right move is not "avoid reconciliation," it's "don't pitch it as a novel market discovery — pitch it as executing Razorpay's own stated ask better than a typical entrant would, with real rigor on the exception-explanation and audit-trail side, which is where even the commercial tools (per their own marketing) still lean on human judgment."

### C. Revenue recovery (your idea A/B) — **the least saturated of your original four, and it's the track's headline example**

**Butter Payments** (V): $ series-funded SF startup, focuses specifically on *subscription* involuntary-churn recovery — ML-optimized retry timing/routing for failed recurring card payments, claims up to 5%+ ARR impact for subscription merchants, cites $440B/year industry-wide cost of involuntary churn. Just launched a "Payments Score" and "Outreach" product (Jan 2026) with 8–10% uplift.

**FlyCode** (V, per a 2026 comparison source): positions itself against Butter/Stripe's own recovery logic by training per-merchant ML models rather than one fixed retry schedule, and layers coordinated outreach (timed emails) on top of retries.

**(I) Key structural difference from Justt/reconciliation space:** Butter, FlyCode, and Stripe's built-in recovery logic are almost entirely about **card-network-level retry optimization for recurring/subscription payments** — a narrow, mature sub-problem with a data moat (billions of historical retry outcomes) a student cannot replicate. They are *not* generally building the broader "detect payment degradation anywhere in the funnel → diagnose root cause → choose and execute the right one of several intervention types → prove money recovered" system that Razorpay's track literally names as its lead example. That broader diagnostic-and-orchestration layer — spanning checkout drop-off, failed subscriptions, B2B receivables, mandate retries — is genuinely less commoditized than either dispute automation or reconciliation matching.

### D. Agentic commerce (Track 1) — genuinely new, but immature and riskier for a 10-day build

**(V)** NPCI is developing a Unified Agent Protocol (UAP) for AI-agent-initiated UPI payments; Razorpay and NPCI already ran a live pilot enabling agentic UPI payments inside Claude in Feb 2026, with Zomato, Swiggy, and Zepto as initial merchant partners, using one-time consent plus per-merchant spending limits instead of PIN/OTP per transaction. Globally, protocols like OpenAI's ACP, Google's AP2/UCP, and Coinbase's x402 are competing to standardize agent checkout/authorization/settlement. One industry participant, quoted in coverage of NPCI's UAP effort, explicitly flagged that **chargeback and dispute-management flows for agent-initiated transactions are not yet solved** — "existing systems for user-initiated payment flows... should be in place in the agentic world... how do we control a machine going rogue?"

**(I) Verdict:** This is a real, live, and *not yet productized* gap — dispute/reversal/audit tooling for agent-initiated payments. It's intellectually the most novel option in your whole document. I'm not recommending it as your primary pick because: (a) it requires you to build against protocols that are still specs-in-motion, with no stable test harness guaranteed by Sept 5; (b) it doesn't play to your stated skill base (ML/NLP/full-stack) as directly as a data-and-decision system does; (c) the failure mode if the underlying protocol assumptions are wrong is a demo that doesn't actually run. Flagging it so you know it exists, but see Part 8 for why I'm not making it the primary recommendation.

---

## 3. Actual pain evidence (not generic claims)

You asked me not to accept "reconciliation is tedious" at face value. Here's what's actually documented:

- **Who:** Indian D2C/e-commerce finance-ops teams reconciling COD orders, marketplace payouts (Amazon/Flipkart), and gateway settlements against internal order records.
- **What exactly, manually:** matching a single lumped NEFT credit (net of MDR, GST-on-MDR, refund deductions) back to hundreds of individual orders using `settlement_id`; separately matching TDS deductions in Form 26AS against books at the *section level* (194C/194J/194H/194Q) — where a ₹10,000 "gap" is often correct-but-unmatched TDS, not a real discrepancy, and a naive tool wrongly flags it.
- **How often / cost:** One India-focused reconciliation vendor's own case data reports finance teams moving from 3-week reconciliation cycles to 3 days after adopting purpose-built India-aware matching — implying the baseline manual cycle really does run to weeks per period, not hours. A separate source estimates COD/RTO-heavy D2C brands can silently lose 8–12% of monthly revenue to unnoticed ops-finance mismatches before detection.
- **Why existing generic tools fail:** "A generic bank reconciliation tool does not understand that a bank credit of ₹90,000 against an invoice of ₹1,00,000 is a TDS match — not an amount mismatch." Generic (non-India-aware) tools require manual workarounds for TDS, GSTR-2B, and NACH batch disaggregation.
- **What decision the human actually needs to make, per exception:** is this a timing difference (settle later), a fee/tax component I should already expect, or a genuine loss requiring escalation — and if genuine, who do I chase (bank, gateway, courier, marketplace)?

**(I)** This evidence is strong for reconciliation-as-a-category, but note it's evidence *for the vendors who already sell this* (TransactIG, ReconPe) — i.e., it proves the pain is real, not that it's unclaimed.

For revenue recovery, the equivalent evidence is Butter's own claim of $440B/year industry-wide cost of involuntary churn — real but vendor-sourced, and specific to *subscription* churn, not the broader "any payment degrades somewhere in the funnel" framing Track 3 actually asks for. I did not find equally strong third-party pain evidence for the broader multi-cause revenue-recovery framing; that's partly *because* it's less mapped territory — which cuts both ways: bigger opportunity, thinner existing validation.

---

## 4. Direct verdicts on C and D

### C — Reconciliation Investigator: **not dead, but reposition it**
- Kill: the "we discovered an underserved gap" framing — TransactIG/ReconPe/Recko/HighRadius all occupy exactly this space, with ReconPe's rule-proposal + exception-explanation-with-severity-score feature being nearly identical to what you described.
- Keep, if you go this route: the exact Track 4 framing (50+ record synthetic batch, honest match rate, unresolved-exception list, audit trail) is what Razorpay is *asking for by name*. This is the safest, most gradeable, most feasible-in-10-days option on your list. Its weakness is that it will likely be the single most common submission in Track 4, since it's the literal first example given.

### D — Dispute Investigator: **kill as scoped; narrow if you insist**
- Kill: full evidence-gathering → recommendation → structured evidence package, because Justt already does this at a scale and data-breadth (500+ sources, millions of historical disputes for phrasing optimization) you cannot approach or meaningfully differentiate from in 10 days.
- If you still want Track 2: pivot to a bounded **triage classifier** (accept/contest/escalate) scored on precision/recall/false-positive cost — that's a genuinely different, smaller, gradeable problem that doesn't try to out-build Justt's core product.

---

## 5. Problem Opportunity Matrix

Scored 1–10. Reasoning is compressed but every score is defensible from the research above.

| Criterion | C. Reconciliation Investigator | D. Dispute Investigator (as scoped) | **A/B. Payment Degradation → RCA → Recovery** | Chargeback Triage Classifier (narrow D) |
|---|---|---|---|---|
| Severity of pain | 8 | 7 | 7 | 6 |
| Frequency | 9 (every settlement cycle) | 4 (chargebacks are rarer events) | 8 (failures happen daily at scale) | 4 |
| Economic value per instance | 6 | 8 (chargebacks are costly per case) | 7 | 7 |
| # potential customers | 8 | 6 | 8 | 6 |
| Willingness to pay | 7 | 8 (Justt's success proves this) | 7 | 6 |
| Competition intensity | 7 (high — TransactIG/ReconPe/Recko) | 9 (very high — Justt/Chargeflow etc.) | 4 (mostly subscription-niche players) | 5 |
| Existing solution quality | 7 (India-specific tools are mature) | 9 (Justt is excellent) | 5 (mostly narrow retry-optimization) | 6 |
| Differentiation opportunity for a student | 4 | 2 | 7 | 6 |
| AI leverage (is AI actually necessary here) | 6 (rules do most of the work; LLM helps explain) | 6 (LLM needed for phrasing/evidence synthesis) | 8 (needs anomaly detection + causal ranking + generation) | 5 (mostly classic ML) |
| Technical depth achievable in 10 days | 6 | 5 | 8 | 6 |
| Data availability (can you simulate it well) | 9 (synthetic order/payment/settlement data is easy to generate realistically) | 6 (dispute + evidence data is harder to simulate credibly) | 8 | 7 |
| Evaluation feasibility | 9 (match rate is objective) | 5 (contest/accept "correctness" needs a ground truth you must invent) | 7 (need to define "recovered" clearly, but doable) | 8 (precision/recall is clean) |
| MVP feasibility by Sept 5 | 8 | 5 | 6 | 8 |
| Demo potential | 6 (matching is visually undramatic) | 7 | 8 (detect → explain → act → prove is a strong live demo arc) | 5 |
| Razorpay competition fit | 9 (literally the named example) | 7 (named example, but a harder sub-bar to hit) | 9 (literally the named example) | 7 |
| Hiring/interview signal | 7 | 6 | 9 (touches detection, causal reasoning, decisioning, execution, evaluation — broadest engineering surface) | 6 |
| Potential to become a real product | 6 | 4 (crowded) | 7 | 5 |

**(I) Reading the matrix:** Reconciliation and the RCA-recovery idea are statistically close, but the RCA-recovery idea wins specifically on differentiation opportunity, AI leverage (it actually needs the ML/anomaly-detection + LLM-reasoning combination you want to learn, rather than being solvable by rules plus a thin LLM veneer), demo potential, and hiring signal — because it forces you to design four distinct engineered stages (detect, diagnose, decide, act) rather than one matching stage.

---

## 6. Top 5 opportunities, ranked

1. **Payment Degradation → Root Cause → Bounded Recovery Agent** (Track 3) — my recommendation, detailed in Part 8.
2. **Multi-source Reconciliation Investigator, India-compliance-aware** (Track 4) — strong, safe fallback; do this if you want the lowest-risk path to a clean, gradeable submission.
3. **Chargeback Triage Classifier with honest precision/recall/FP-cost reporting** (Track 2) — smallest scope, cleanest evaluation story, good if you want to minimize build risk in the time remaining.
4. **B2B receivables / promise-to-pay tracker** (Track 3 sub-variant) — genuinely underexplored in my research (I found far less competitive material here than for subscription dunning), but I could not find strong third-party pain evidence for it either, so treat this as higher-uncertainty, not fully validated.
5. **Agent-initiated-payment dispute/audit layer** (Track 1 adjacent) — most novel, least mature, highest execution risk given an 10-day window; worth a paragraph in your pitch as "future direction" even if you build #1.

---

## 7. Hybrid consideration

Your document allows combining ideas if there's a coherent user relationship. The strongest coherent hybrid I found: **reconciliation-derived anomaly detection feeding a recovery/root-cause action**, i.e., idea C's detection layer feeding idea A/B's decision layer. This isn't "combine features to look big" — it's a real pipeline: you cannot decide the right recovery action for a "missing ₹21,460" without first doing some of the matching work reconciliation does. My Part 8 recommendation actually folds a lightweight version of this in (see Data & Architecture) rather than treating them as separate products.

---

## 8. Recommended project

### Product name
**Reconcile & Recover** (working title) — an agent that watches a merchant's payment funnel, explains *why* revenue is degrading in one place, and executes a bounded recovery action while proving how much money it recovered.

### One-sentence problem
Merchants can see *that* a payment failed, a checkout was abandoned, or a settlement came in short — but nothing in their stack tells them *why*, ranks it by revenue at risk, and safely acts on it without a human doing that triage by hand every time.

### Target customer
A mid-size Indian D2C/subscription merchant on Razorpay (or Razorpay test-mode equivalent) — someone with enough transaction volume that manual triage of every failed/degraded payment is no longer feasible, but not enterprise-scale enough to have bought HighRadius/TransactIG-class tooling.

### User persona
A finance-ops or growth lead who currently opens the Razorpay dashboard once a day, eyeballs a drop in success rate or a settlement shortfall, and manually decides "is this worth chasing, and how."

### Existing workflow
Check dashboards/CSV exports for failed payments and settlement variance → manually segment by bank/method/geography to guess a cause → decide case-by-case whether to retry, email the customer, or escalate → no systematic record of what was tried or what worked.

### Why current solutions are insufficient
Razorpay's own dashboard reports *what happened* (per-transaction status, settlement breakdown) but not *why a whole segment is failing* or *what to do about it*. Butter/FlyCode-style tools optimize *retry timing* for recurring subscription card failures specifically — they don't diagnose root cause across the full funnel (routing, bank-specific decline spikes, checkout abandonment, B2B receivables) or handle non-recurring payment types. Nothing in the researched landscape ties detection → diagnosis → bounded action → proof-of-recovery into one auditable loop for the *general* payment-degradation case Razorpay's track describes.

### Proposed solution
An event-driven pipeline over synthetic (or Razorpay test-mode) payment data that:
1. Continuously monitors success-rate and settlement metrics segmented by dimension (bank, payment method, geography, merchant category).
2. Detects statistically meaningful degradation (not just "payments failed today").
3. Ranks candidate root causes using a mix of rules (known failure codes, bank outage patterns) and an LLM-assisted reasoning step that reads structured evidence (error codes, timing, segment) and produces a ranked, evidenced explanation.
4. Selects one of a small, explicitly bounded set of recovery actions (retry with backoff, alternate payment method suggestion, customer nudge, escalate-to-human) based on the diagnosed cause and defined business rules — never an unbounded/free-form action.
5. Executes the action, logs every step to an audit trail, and reports batch-level "money recovered" plus an honest list of cases it could not resolve.

### Core user journey
Dashboard shows a degradation alert → click in → see ranked root-cause explanation with the evidence behind it → see the recovery action the agent took (or is proposing, if it required approval) → see the outcome and running recovered-revenue total → see the exception list for anything the agent explicitly could not resolve.

### Exact functionality (MVP)
- Synthetic data generator producing realistic payment events (success/fail codes, bank, method, geography, timestamps) with injected degradation scenarios (e.g., one bank's UPI success rate craters for 6 hours).
- Detection: rolling-window anomaly detection per segment (a standard statistical method — e.g., z-score or CUSUM on success rate — is enough; you don't need a novel model here).
- Diagnosis: rule-based first pass (known decline-code → known-cause mapping) + LLM step that only runs when rules are inconclusive, constrained to select from a fixed taxonomy of causes and cite the evidence rows it used.
- Decision: a small decision table (cause → allowed actions), never an open-ended LLM decision — this is what makes it "bounded and gated," which is literally the Track 3/Track 1 bar.
- Action: simulated execution (retry queue, notification stub) with idempotency and a stopping rule (e.g., max 3 retries, then escalate).
- Reporting: batch summary — detection count, correctly diagnosed (against your injected ground truth), money recovered, cases escalated, full audit log.

### What AI does
- Anomaly *ranking* and root-cause *narrative generation*, grounded in retrieved evidence rows (this is the one place an LLM adds real value over a lookup table — synthesizing a coherent explanation across multiple correlated signals).
- Optionally, a small classifier (not necessarily deep learning — gradient boosting is fine and easier to evaluate) for "will this specific failed payment recover if retried," trained on your synthetic data's known ground truth.

### What AI should NOT do
- Should not autonomously choose or invent recovery actions outside the fixed decision table.
- Should not execute financial actions above a configured value threshold without human approval — build this in explicitly, it's a direct match to the Track 1 "bounded and gated" and Track 3 "compliant escalation, stopping rules" bars.
- Should not fabricate root causes without citing the underlying evidence rows it used.

### Data required / what you can realistically simulate
Order, payment attempt, and settlement event streams; bank/method/geography dimensions; injected failure scenarios with known ground-truth causes (so you can score your own diagnosis accuracy honestly — this is exactly what "one cherry-picked match proves nothing" is warning you against). Razorpay test-mode APIs can supply the real payment-lifecycle shapes even if volume is synthetic.

### System architecture (brief — expand in your repo's architecture doc)
- **Ingestion:** event stream (can be a simple queue or even batched Postgres inserts for a 10-day build) from synthetic generator / Razorpay test-mode webhooks.
- **Detection service:** stateless job computing rolling segment-level metrics; stores anomaly events.
- **Diagnosis service:** rules engine first; LLM call (structured-output JSON, constrained cause taxonomy) only on rule-engine "unknown."
- **Decision engine:** deterministic lookup table, versioned and testable independent of the LLM.
- **Action executor:** idempotent, logged, with a dry-run/approval mode for anything above threshold.
- **Audit store:** append-only log of every detection → diagnosis → decision → action, queryable for the "honest exception list."
- **Dashboard:** FastAPI + Vue (matches your existing stack) rendering the user journey above.

### ML models
Simple, defensible choices: statistical anomaly detection (no training needed, fully explainable) for detection; gradient-boosted classifier (e.g., LightGBM) for "will retry succeed," evaluated with precision/recall on a held-out synthetic split — this is exactly the kind of "worked numerical example" evaluation style you already prefer.

### LLM usage
Root-cause narrative generation and ambiguous-case diagnosis, always constrained to structured output over a fixed taxonomy with cited evidence — never free-form financial decision-making.

### Database/storage
Postgres is enough; you don't need a vector database or graph database for the MVP — don't add either unless a specific requirement forces it (see Part 9 on justifying every component).

### Retrieval system if needed
Not needed for MVP. If you have time left, a small retrieval step over historical resolved cases ("have we seen this pattern before and what worked") is a legitimate, justified use of embeddings — because *that* specific sub-problem (find similar past incidents) is genuinely a semantic-similarity problem, unlike your first draft's blanket embeddings.

### Agent/workflow design if needed
A bounded state machine (detect → diagnose → decide → act → verify → close/escalate) is enough — you do not need a general-purpose autonomous agent framework. Justify this explicitly in your write-up: "we chose a constrained state machine over a free-form agent because every state transition needs to be auditable and the action space needs to be bounded — an unconstrained agent loop would violate the track's own gating requirement."

### Evaluation metrics
- Detection: precision/recall against injected anomalies (you control ground truth).
- Diagnosis: top-1/top-3 accuracy against the injected true cause.
- Recovery: batch-level money recovered vs. money at risk; % resolved automatically vs. escalated; false-positive cost (acting when nothing was actually wrong).

### Failure modes
LLM misdiagnoses a novel pattern → mitigate with confidence thresholds that force escalation instead of action. Action executor double-fires → mitigate with idempotency keys. Detector flags normal seasonal variation as anomaly → mitigate by baselining against day-of-week/time-of-day patterns, not a flat threshold.

### Human-in-the-loop points
Any action above a configured revenue threshold; any diagnosis below a confidence threshold; anything the rules engine and LLM disagree on.

### Security/safety considerations
No real payment credentials in the demo; all financial "actions" against Razorpay test-mode only; rate-limit and cap the LLM's action-proposing role so it can never itself trigger a live transaction.

### Audit trail
Every detection, diagnosis (with cited evidence and confidence), decision, and action, append-only, timestamped, exportable — this is your single strongest "AI Judgment" and "Failure Recovery" story for the panel.

### Razorpay test-mode integration
Use test-mode payment/order/refund/settlement webhooks to get realistic event shapes; layer your synthetic-scenario generator on top to control ground truth for evaluation (pure production data would give you no ground truth to score against).

### What can realistically be built by September 5
Detection + rules-based diagnosis + decision table + simulated action + audit log + dashboard, with LLM diagnosis for the "unknown cause" branch only. This is a complete, honestly-evaluated loop.

### What should explicitly NOT be built in the MVP
Multi-processor support, real bank/PSP integrations beyond Razorpay test-mode, a general-purpose agent framework, a vector DB / RAG layer (unless time remains), voice/Hinglish recovery (interesting per the track's own example list, but a distinct NLP subsystem you don't have time to build well alongside everything else).

---

## 9. Teaching the engineering — deriving the architecture

Worked example, per your request:

> **User requirement:** "Finance/growth lead needs to know why revenue is degrading and get it fixed without babysitting every case."
> → **System requirement:** continuously detect abnormal segments, explain the most likely cause with evidence, and act only within pre-approved bounds.
> → **Technical property needed:** (a) statistical baseline-deviation detection per segment, (b) evidence-grounded explanation generation, (c) deterministic, auditable decisioning, (d) idempotent execution.
> → **Possible implementations for each:** (a) z-score/CUSUM vs. a full anomaly-detection model — a simple statistical method is *sufficient* because your segments are low-cardinality and the pattern (a step change in success rate) is not subtle; a heavier model would be unjustified complexity. (b) template-only explanation vs. LLM-generated explanation — a template can't compose evidence from multiple correlated signals into a coherent human-readable narrative, which is the actual property an LLM buys you here; that's the honest justification, not "LLMs are cool." (c) LLM-decided action vs. lookup-table action — the track's own bar (*bounded and gated*) is a hard requirement that rules out a free-form LLM decision here; use the LLM only where its output is checked against a fixed taxonomy. (d) fire-and-forget action vs. idempotent action with a stopping rule — payment retries fired twice cause real financial harm, so idempotency isn't optional polish, it's the difference between a safe and unsafe system.

**On embeddings specifically:** you do not need them for the MVP, because none of your MVP sub-problems require *semantic* similarity — matching a decline code to a cause is a lookup, not a retrieval problem. The one place embeddings would be honestly justified is the optional "has this incident pattern happened before" retrieval extension, because *that* specific question ("is this new incident semantically similar to a past one, even if worded/shaped differently") is a genuine nearest-neighbor-over-meaning problem.

**On graphs:** not needed for the MVP either. A graph is justified when *relationships between many entity types* are the object of investigation (which is why reconciliation-style products do use entity graphs across order/payment/refund/settlement). Your recovery-agent MVP's core object is a segment-level time series, not a multi-entity relationship graph — so don't add one just because it sounds sophisticated.

**On the ML classifier:** the prediction is binary ("will a retry of this specific failed payment succeed"), evaluable directly against your synthetic ground truth with precision/recall/F1 — a small gradient-boosted model is preferable to a deep model here because you have limited, synthetic, tabular data with clear structured features; a deep model would be unjustified complexity and harder to explain to the panel.

**On the agent/state-machine:** a normal fixed pipeline is insufficient *only* insofar as the diagnosis step is genuinely ambiguous and needs a reasoning step over multiple weak evidence signals — that's the one place "agentic" reasoning earns its keep. Everything else in the loop (detect, decide, act, log) should be deterministic code, not agent reasoning, both for auditability and because it's simply the right tool for a deterministic sub-problem.

---

## 10. Brutally honest final take

**What I would build if I were you:** the Payment Degradation → Root Cause → Bounded Recovery Agent (Part 8). It is Razorpay's own named example, it is less saturated than either of your original C or D ideas, and its four-stage architecture (detect/diagnose/decide/act) gives you the broadest, most defensible "I understood the system and chose each component for a reason" story — which is exactly what you said you wanted to be able to say honestly.

**What I would NOT build:** the Dispute Investigator as originally scoped (Justt's moat is too deep to meaningfully differentiate from in 10 days), and I would not build a generic "AI reconciliation platform" pitched as if it were a novel discovery (TransactIG/ReconPe/Recko already occupy that framing) — if you do pursue reconciliation, pitch it honestly as "executing Razorpay's own stated Track 4 ask well," not as market discovery.

**Is your Dispute Investigator idea strong enough?** No, not as scoped. Narrowed to a triage classifier, it's viable but is your weakest of the options analyzed here on differentiation and demo potential.

**Is your Reconciliation Investigator idea stronger?** Yes, stronger than Dispute Investigator, and it's the lowest-risk path to a clean, complete, honestly-evaluated submission if you want to minimize build risk. It is not stronger than the Revenue Recovery hybrid on differentiation or hiring signal.

**Is there a third idea that's substantially better?** Yes — see Part 8. It's substantially better mainly because it forces genuine system design across four distinct engineered stages rather than one matching stage, and because the competitive field behind it (subscription-dunning ML shops) doesn't actually cover the general funnel-wide root-cause framing Razorpay is asking for.

**Are you trying to build something too ambitious for the deadline?** Your original document — reconciliation *and* dispute investigation, each with entity resolution, graphs, RAG, and human-in-the-loop workflows — was too ambitious for 10 days. The recommendation in Part 8, scoped to its explicit MVP boundary (Part 8, "what can realistically be built by Sept 5"), is achievable: detection and rules-based diagnosis are a few days of solid engineering; the LLM diagnosis branch, decision table, and audit log are another few days; the dashboard and evaluation reporting round it out. The discipline is in *not* adding the vector DB, the graph, the multi-processor support, or the voice/Hinglish layer — all of which are legitimate ideas you should explicitly say you scoped out, not things you silently forgot.

**What would make this look like a genuine engineering product rather than a hackathon demo:** the audit trail, the honest exception/escalation list (don't hide the cases it couldn't solve — showcase them), the injected-ground-truth evaluation methodology, and a documented "what broke and how I fixed it" story in your pitch video — all four map directly to stated panel criteria.

---

## 11. 10-day implementation plan (compressed)

- **Days 1–2:** Synthetic data generator (orders/payments/settlements + injectable degradation scenarios with known ground truth); Razorpay test-mode account and API familiarization.
- **Days 3–4:** Detection service (segment-level rolling anomaly detection) + evaluation harness against your injected ground truth.
- **Days 5–6:** Rules-based diagnosis + decision table + idempotent action executor + audit log (get the deterministic backbone solid and tested before adding the LLM).
- **Day 7:** LLM diagnosis branch for rule-engine "unknown" cases, constrained structured output, evidence citation.
- **Day 8:** Dashboard (FastAPI + Vue) showing the full user journey from Part 8.
- **Day 9:** End-to-end batch run, honest metrics (detection precision/recall, diagnosis accuracy, money recovered, escalation list), fix the failure you find (this becomes your "what broke" story).
- **Day 10–11:** Architecture write-up, README, 5-minute pitch video, buffer for the inevitable last-day bug.

---

## 12. Biggest risks

- **Scope creep back toward your original 4-idea list** — the discipline of Part 8's explicit "not in MVP" list is your main defense.
- **LLM diagnosis being unconstrained** — if it isn't forced into a fixed taxonomy with cited evidence, it becomes unauditable and violates the track's own bar; build the structured-output constraint early, not as a late add-on.
- **No injected ground truth** — without it you cannot honestly report precision/recall/accuracy, and the panel is explicitly warned against "one cherry-picked match."
- **Running out of time for the audit trail / dashboard** — these are what make the difference between "a script that works" and "a product," and they're exactly what the panel is trained to look for; don't leave them for the last day.

---

## Sources consulted (representative, not exhaustive)
- razorpay.com/buildathon (official track descriptions and bars, fetched directly)
- justt.ai (platform, FAQ, comparisons pages), thepaypers.com, businesswire coverage of the Justt–Recurly integration
- highradius.com (product pages), techcrunch.com / stripe.com newsroom (Recko acquisition coverage)
- reconpe.com, g2.com/products/transactig, terra-insight.com (India-specific reconciliation pain points and product capabilities)
- butterpayments.com, flycode.com, paymentsdive.com (revenue recovery / involuntary churn space)
- business-standard.com, medianama.com, stellagent.ai, outlookbusiness.com (NPCI Unified Agent Protocol coverage)
- razorpay.com/blog (Smart Collect, settlement transparency playbook)
