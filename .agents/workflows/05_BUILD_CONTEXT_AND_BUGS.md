# 🧠 Build Context & Bug Tracking - AI Project Memory

**Version:** 1.6.0 | **Updated:** March 19, 2026 | **Part:** 6/10  
**Status:** Production Ready ✅  
**Purpose:** Give AI Coding Assistants project memory to prevent repeated bugs and architecture drift.

---

## 📍 Purpose

AI Coding Assistants (Cursor, Windsurf, Claude Code, Antigravity) have **zero memory between sessions**. 

To solve this, we use two files that the **AI is responsible for reading and updating**:
1. **`.build-context.md`** — Project state, recent changes, architecture, audit history.
2. **`.bugs_tracker.md`** — Active bugs, patterns, root causes.

**Core Rule:** The AI must manage its own memory through a strict "Read -> Act -> Update" loop (enforced via `agent.md` in File `04`).

**Memory Lifecycle:** These files are append-only during active development, but must be periodically archived to prevent context window overflow. See [The Archive Protocol](#-the-archive-protocol-cold-storage) for the rotation lifecycle.

---

## 🗺️ Quick Navigation

- [The AI-First Bookkeeping Workflow](#-the-ai-first-bookkeeping-workflow)
- [File 1: .build-context.md Template](#-file-1-build-contextmd)
- [File 2: .bugs_tracker.md Template](#-file-2-bugs_trackermd)
- [The Archive Protocol (Cold Storage)](#-the-archive-protocol-cold-storage)
- [Troubleshooting Memory Loss](#-troubleshooting)

---

## 🤖 The AI-First Bookkeeping Workflow

You do not need to manually update these files. You enforce that the AI does it.

### Step 1: Session Start (READ)
The AI reads `.build-context.md` automatically via the `agent.md` rules.
**You say:** "Let's continue building the Research Agent. Read project memory."

### Step 2: Coding (ACT)
The AI follows the "Tech Radar -> Factory" pipeline, writes the code, and runs tests.

### Step 3: Session End (UPDATE)
**You say:** "Great, that works. Update `.build-context.md` with what we built today and any new architectural decisions. If we hit any bugs, log them in `.bugs_tracker.md`."

---

## 📄 File 1: `.build-context.md`

### Template (Create this in your root folder)

```markdown
# AI Project Memory - [PROJECT NAME]

**Last Updated:** [DATE/TIME]  
**Project Phase:** [Discovery/Build/Test/Deploy/Maintain]  
**Risk Score:** [0-17]  

---

## 📍 Current State

### What I'm Working On Right Now
- **Feature:** [Current feature name]
- **Status:** [Started/In Progress/Testing/Blocked]
- **Blocker:** [What's blocking progress]

### Summary of Past Phases
*(AI: This section is maintained by the /archive-memory command. It contains compressed summaries of completed phases. Do not delete these entries — they are the only record of archived work.)*

- **Phase 1 (Discovery):** [2-3 sentence summary of key decisions and outcomes]
- **Phase 2 (Build - Core Agents):** [2-3 sentence summary]

### Recent Changes (AI-UPDATED)
- **[DATE]:** Built [feature/component]
  - Files modified: `app/agents/researcher.py`
  - Architectural Decision: Decided to use LangGraph for orchestration.

---

## 🏗️ Project Structure
[Provide a brief tree of your /app, /infra, and /tests folders here]

---

## ⚙️ Configuration & Factories
- **LLM Engine:** [e.g., Anthropic via scale.yaml]
- **Orchestration:** [e.g., LangGraph]
- **Database:** [e.g., PostgreSQL]
- **Environment:** Hybrid MCP + Local

---

## 🛠️ Important Architectural Decisions
*(AI: Never delete these entries. Add to them when making technical choices.)*
*(AI: Audit findings that result in approved changes are architectural decisions. Log them here with the audit date and the rationale the human gave for approving.)*

**Decision:** Use hybrid tooling  
**Why:** DB queries need speed (local); file access needs safety (MCP)

**Decision:** Agent Orchestration  
**Why:** Decided to use LangGraph to manage cyclic agent routing instead of linear scripts.

---

## 🔍 Audit History
*(AI: Add an entry each time an audit is completed or an item is applied)*

**Audit [DATE]:**
  Completed: [DATE]
  Items approved: [N]
  Items deferred: [N]
  Items rejected: [N]
  Applied changes: [list]
  Test result: PASS / FAIL + rollback note if applicable
  Sign-off: [human name or initials]

**Between-audit CVE alerts:**
  [DATE]: [package] [CVE-ID] — [action taken]

---

## 🗄️ Archive History
*(AI: Add an entry each time /archive-memory is run)*

| Archive Date | File | Phases Covered | Bugs Promoted to Skills |
|-------------|------|----------------|------------------------|
| [DATE] | `docs/archive/memory_archive_[DATE].md` | Phase 1-2 | [skill-name] or None |

---

## 🧩 Skills Registry
*(AI: Register every reusable skill here. Check this list before writing a new pattern — if a skill already exists, use it.)*

| Skill Name | Location | Trigger Condition | Created | Last Audited |
|------------|----------|-------------------|---------|--------------|
| [e.g., test-scaffold] | `/skills/test-scaffold/` | "Create a Pytest file with LLM-as-a-judge for any new agent" | [DATE] | [DATE] |
| [e.g., factory-generator] | `/skills/factory-generator/` | "Create interface + adapter + factory for a new external service" | [DATE] | [DATE] |
```

---

## 📄 File 2: `.bugs_tracker.md`

### Template (Create this in your root folder)

```markdown
# Bug Tracker & Pattern Memory

**Last Updated:** [DATE]  
**Active Bugs:** [COUNT]  

---

## 🚨 Active Bugs
### BUGS-001: MCP Connection Timeout
**Status:** Active | **Severity:** Major  
**Description:** Agent fails to connect to `mcp-filesystem` on initial startup.
**Fix Attempts:** Tried sleep(5). Didn't work reliably. Next step: Add Tenacity retry backoff.

---

## 🔍 Bug Patterns Identified (AI-UPDATED)
*(AI: Read this before writing new integration code to avoid repeating mistakes)*

### Pattern 1: Sidecar Race Conditions
**Occurrences:** 2 times (MCP filesystem + Database)  
**Root cause:** Containers starting before services are ready  
**Solution:** Always use exponential backoff decorators on connection logic.

### Pattern 2: API Rate Limiting
**Occurrences:** 1 time (External Search Tool)
**Root cause:** Parallel agent execution triggered 429 errors.
**Solution:** Implemented the Token Bucket algorithm in the `RateLimiter` middleware.

---

## ✅ Resolved Bugs (Pending Archive)
*(AI: Resolved bugs live here temporarily. During /archive-memory, move these to the archive file. If a resolved bug reveals a recurring pattern, promote it to a skill BEFORE archiving.)*

### BUGS-000: [Example Resolved Bug]
**Status:** Resolved [DATE] | **Severity:** Minor  
**Resolution:** [What fixed it]  
**Pattern?:** [Yes → promoted to skill / No]
```

---

## 🗄️ The Archive Protocol (Cold Storage)

### The Problem

`.build-context.md` and `.bugs_tracker.md` grow with every session. On a long-running project, they will eventually exceed the AI's useful context window — causing the assistant to lose focus, hallucinate older details, or silently drop important constraints.

### The Solution: Log Rotation for AI Memory

Separate **Active Memory** (what the AI needs right now) from **Cold Storage** (historical record for audits and reference).

### Archive Directory

```text
docs/
  archive/
    memory_archive_2026-03-01.md    # Phase 1 context + resolved bugs
    memory_archive_2026-06-15.md    # Phase 2 context + resolved bugs
```

### When to Archive

Archive is triggered by **either** of these conditions:

1. **Threshold:** `.build-context.md` exceeds the line count or token count configured in `scale.yaml` (see `07_CONFIGURATION_CONTROL.md` → `context_management.archive_threshold_lines`).
2. **Phase transition:** When the project moves to a new phase (Discovery → Build → Test → Deploy → Maintain), archive the completed phase's working notes.

The `/archive-memory` command in `04_AI_ASSISTANT_INTEGRATION.md` executes the routine. You can also trigger it manually at any time.

### The Archive Routine (What the AI Does)

When `/archive-memory` is triggered, the AI executes these steps in order:

**Step 1 — Skill Promotion Check (Before Deletion)**
Read the "Resolved Bugs (Pending Archive)" section in `.bugs_tracker.md`. For each resolved bug, check: does this reveal a recurring pattern (3+ occurrences)? If yes, the AI **must** propose a `/new-skill` before the bug entry is moved to the archive. Patterns that are archived without becoming skills are lost knowledge.

**Step 2 — Compress & Move**
The AI reads the oldest completed features, resolved bugs, and historical entries. It writes them into a timestamped archive file at `docs/archive/memory_archive_[DATE].md` with full detail preserved.

**Step 3 — Summarize**
The AI writes a 2-3 sentence summary per archived phase into the "Summary of Past Phases" section at the top of `.build-context.md`. This summary is the AI's compressed memory — enough to orient itself without reading the full archive.

**Step 4 — Truncate**
Active files are trimmed to only what is relevant to the current sprint or phase. The "Recent Changes" section keeps only the last 14 days. The "Resolved Bugs (Pending Archive)" section is cleared.

**Step 5 — Verify**
Start a fresh read of the trimmed `.build-context.md` and confirm the AI can orient itself without referencing the archive.

### What Gets Archived vs. What Stays

| Content | Action |
|---------|--------|
| Completed features older than 14 days | Archive |
| Resolved bugs (after skill promotion check) | Archive |
| Audit History entries | **Stay** (never archive — compliance record) |
| Architectural Decisions | **Stay** (never archive — always relevant) |
| Skills Registry | **Stay** (never archive — active reference) |
| Summary of Past Phases | **Stay** (compressed memory, always at top) |
| Active bugs | **Stay** |
| Current sprint work | **Stay** |

### Archive File Format

```markdown
# Archive — [PROJECT NAME] — [DATE]

**Archived by:** /archive-memory command  
**Covers:** Phase [N] ([Start Date] — [End Date])  
**Skills promoted from this archive:** [skill-name] or None

---

## Completed Features
[Full detail of completed features moved from .build-context.md]

## Resolved Bugs
[Full detail of resolved bugs moved from .bugs_tracker.md]

## Notes
[Any context the AI thought was worth preserving for future reference]
```

---

## 🔧 Troubleshooting

### AI Keeps Forgetting Context
**Cause:** Context window exceeded.  
**Fix:** Run `/archive-memory` to trim the active files. Check if `.build-context.md` exceeds the threshold in `scale.yaml`.

### AI References Archived Details Incorrectly
**Cause:** The AI is guessing from the compressed summary instead of reading the archive.  
**Fix:** Say: "Read `docs/archive/memory_archive_[DATE].md` for the full details on that."

### AI Doesn't Update Memory After Session
**Cause:** Session ended without the update prompt.  
**Fix:** Always close with: "Update `.build-context.md` with what we built today."

---

## 📌 File Meta

**Version:** 1.6.0  
**Released:** March 19, 2026  
**Status:** Production Ready ✅  
**Part of:** 10-Part AI Agent Framework  

**Next File:** [06_INFRASTRUCTURE_AS_CODE.md](./06_INFRASTRUCTURE_AS_CODE.md) (Deployment)
