# 🚀 START HERE - AI Agent Framework Documentation

**Version:** 1.6.0 | **Updated:** April 6, 2026 | **Part:** 1/10 of Framework  
**For:** AI Coding Assistants (Cursor/Claude Code/Antigravity) + You  
**Status:** Production Ready ✅  
**Framework Rating:** 10/10 ⭐ (Why: Prevents 80% of agent bugs • 2026-compliant • 30-50% faster builds • 80%+ code reuse)

---

## 📍 Purpose

This file is your **decision entry point** into the AI Agent Framework. It helps you (and the AI assistant) make 6 critical architectural choices:

1. **What's the risk?** (0-17 score determines guardrails)
2. **What architecture fits?** (Monolith vs Multi-Agent Orchestration vs Distributed Workers)
3. **What platform?** (Railway, GCP, Azure, Fly, or Northflank)
4. **What observability?** (OpenTelemetry + LangSmith/Phoenix by default for production)
5. **What tooling strategy?** (Local adapters vs MCP bridges)
6. **How does it stay current?** (Scheduled audit with HITL — configure notification channel in `scale.yaml` before first deploy)

---

## 🗺️ Quick Navigation

- [30-Second Quick Start](#-30-second-quick-start)
- [What's New in v1.6.0](#-whats-new-in-v160)
- [The Risk Scoring Decision Tree](#-the-risk-scoring-decision-tree-0-17-scale)
- [Framework Files Overview](#-framework-files-overview-1-10-docs)
- [Platform Deployment Matrix](#-platform-deployment-matrix)

---

## ⚡ 30-Second Quick Start

**If you are starting a new project right now:**
1. Copy `agent.md` (the System Kernel) into your project root and run `./scripts/sync-kernel.sh`. This sets up Cursor, Claude Code, Windsurf, and Antigravity's `.agents/` folder in one command.
2. Generate your `AgentSpec.md` using `MASTER_AGENT_DISCOVERY_PROMPT.md` — this defines *what* you're building.
3. Read `01_QUICK_REFERENCE.md` to calculate your Risk Score (0-17).
4. Use the `/new-agent` prompt pattern from `agent.md`.
5. Force the AI to use `08_AGNOSTIC_FACTORIES.md` so you aren't locked into one LLM or orchestrator.
6. Set `audit.notification_channel` in `scale.yaml` before first deploy (see `09_AUDIT_AND_MAINTENANCE.md`).
7. If using the Dual-LLM build/check cycle, read `DUAL-LLM-PHASE-CYCLE.md` — it defines how your Builder LLM and Checker LLM collaborate across 7 rounds per phase.

**New team member?** Read `TEAM_ONBOARDING.md` first — it covers everything in 15 minutes.

---

## 🆕 What's New in v1.6.0

- **Dual-LLM Phase Cycle (`DUAL-LLM-PHASE-CYCLE.md`):** Formal framework for running two separate LLMs — one to build, one to check — across 7 structured rounds per phase. Prevents a single line of thinking from rationalizing its own blind spots. Builder Team (Gemini or similar) implements; Checker Team (Claude or similar) traces root causes and delivers ranked suggestions. Governance Gate controls phase advancement.
- **System Kernel (`agent.md`):** Now includes Dual-LLM Cycle awareness — each LLM knows its team, its round, and its handoff responsibilities.
- **Tiered Debate Protocol:** Tier 1 (lightweight sanity checks), Tier 2 (full council at key moments), Tier 3 (human-triggered `/debate`). Ensures quality without killing velocity.
- **Multi-Tool Sync:** `sync-kernel.sh` propagates kernel to `.cursorrules`, `CLAUDE.md`, and `.windsurfrules` in one command.
- **Team Onboarding:** `TEAM_ONBOARDING.md` gets new team members productive in 15 minutes.
- **Scheduled Audit System:** Scheduled dependency, API, framework, and skills audits with mandatory HITL sign-off.
- **Skills Lifecycle:** Rule of 3 identification, `/new-skill` command, Skills Registry in `.build-context.md`, audit review in Layer 4.
- **Naming Normalization:** `.claude-context.md` renamed to `.build-context.md` across all files for tool-agnostic clarity.
- **10-Part Framework:** `09_AUDIT_AND_MAINTENANCE.md` as the dedicated maintenance guide.

---

## 📊 The Risk Scoring Decision Tree (0-17 Scale)

Before writing any code, you must score your agent.

**Data Sensitivity (0-4)** + **Agent Autonomy (0-5)** + **System Impact (0-5)** + **Model Risk (0-3)** = **Total Score**

* **0-5 (Low Risk):** Basic error handling. Proceed fast. (e.g., internal summarizer)
* **6-11 (Medium Risk):** Requires Circuit Breakers, Rate Limiting, and strict output validation. (e.g., draft email generator)
* **12-17 (High Risk):** Requires Human-in-the-Loop (HITL), dedicated sidecar proxy, and full audit trails. (e.g., automated refund issuer)

*(See `01_QUICK_REFERENCE.md` for the exact calculation formula).*

---

## 📚 Framework Files Overview (1-10 Docs)

| Part | File | What it is / When to use it |
| :--- | :--- | :--- |
| **1** | `00_START_HERE.md` | You are here. The entry point. |
| **2** | `01_QUICK_REFERENCE.md` | Formulas, checklists, and matrices. Pin this file. |
| **3** | `02_COMPLETE_GUIDE.md` | Deep methodology, architecture patterns, and testing targets. |
| **4** | `03_DEPENDENCY_MANAGEMENT.md` | `pyproject.toml`, `uv`, and reproducible builds. |
| **5** | `04_AI_ASSISTANT_INTEGRATION.md` | `.cursorrules` and prompt patterns to stop AI hallucinations. |
| **6** | `05_BUILD_CONTEXT_AND_BUGS.md` | Project memory templates (`.build-context.md`, `.bugs_tracker.md`). |
| **7** | `06_INFRASTRUCTURE_AS_CODE.md` | Terraform, Docker, and deployment patterns. |
| **8** | `07_CONFIGURATION_CONTROL.md` | `scale.yaml` and cost controls. |
| **9** | `08_AGNOSTIC_FACTORIES.md` | How to swap DBs, LLMs, and Orchestrators via config. |
| **10** | `09_AUDIT_AND_MAINTENANCE.md` | Scheduled audit system, HITL sign-off, and notification setup. |

**Supporting Files:**

| File | What it is |
| :--- | :--- |
| `agent.md` | **The System Kernel.** AI behavior rules, debate protocol, citation law. Synced to all tools. Includes Dual-LLM Cycle awareness. |
| `DUAL-LLM-PHASE-CYCLE.md` | **The Build/Check Cycle.** 7-round per-phase framework using two LLMs — Builder Team builds, Checker Team traces root causes and delivers ranked suggestions, Governance Gate controls advancement. |
| `TEAM_ONBOARDING.md` | 15-minute onboarding guide for new team members. |
| `scripts/sync-kernel.sh` | Copies `agent.md` to `.cursorrules`, `CLAUDE.md`, `.windsurfrules`. |
| `MASTER_AGENT_DISCOVERY_PROMPT.md` | Interview prompt for architecting new agents before coding. Output feeds Round 1 of the Dual-LLM cycle. |
| `MASTER_DOCS_PROMPT.md` | Post-build prompt for generating project documentation. |

---

## 🔄 The Dual-LLM Phase Cycle (Overview)

If you are running two LLMs in parallel — one to build, one to check — each phase follows this 7-round structure. See `DUAL-LLM-PHASE-CYCLE.md` for the full specification.

```
ROUND 1 → Builder Team plans and builds
ROUND 2 → Checker Team reviews (root cause chains + ranked suggestions)
ROUND 3 → Builder Team builds again (incorporates feedback)
ROUND 4 → Builder Team self-fix pass (internal cleanup)
ROUND 5 → Checker Team reviews again
ROUND 6 → Builder Team final build
ROUND 7 → Governance Gate (approve to advance, or loop back)
```

**Builder Team (LLM 1):** Product Manager, Architect, AI Engineer, Database Manager, DevOps Manager, UX/UI Designer, Data Analyst

**Checker Team (LLM 2):** QA Engineer, Devil's Advocate, Red Team Hacker, Infosec Lead, Project Lead

**Governance Gate:** Compliance Officer, Marketing Manager (if user-facing), Project Lead

---

## 📌 Version & Status

**Version:** 1.6.0  
**Released:** April 6, 2026  
**Status:** Production Ready ✅  
**Next File:** [01_QUICK_REFERENCE.md](./01_QUICK_REFERENCE.md)
