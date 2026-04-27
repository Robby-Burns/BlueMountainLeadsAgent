---
file: GENERIC-ROLES-MASTER-GUIDE.md
version: 1.2.0
description: How all generic roles work together in an Antigravity agent system
framework: Antigravity (adaptable to other frameworks)
---

# 📚 GENERIC ROLES MASTER GUIDE

This document explains how your **12 core roles + 2 advisory roles** work together to build and operate an Antigravity agent system.

---

## 🎯 THE 12 CORE ROLES

| Role | Authority | Primary Job | Blocking Power |
|------|-----------|-------------|----------------|
| **Product Manager** | Strategic | Define mission, own success metrics, go/no-go | ✅ Can block launches |
| **Architect** | Technical | Design patterns, factory enforcement, tech decisions | ✅ Can block code |
| **Database Manager** | Technical | Schema, encryption, performance, backups | ✅ Can block deployments (data risk) |
| **Infosec Lead** | Security | Audits, kill switch, breach prevention | ✅ Can block (activate kill switch) |
| **DevOps Manager** | Operations | Deployment, costs, uptime, monitoring | ✅ Can block deployments |
| **AI Engineer** | Technical | Implement agents, write code, optimize | ⚠️ Code review blocker (if violates patterns) |
| **QA Engineer** | Technical | Tests, coverage, quality gates | ✅ Can block deployments (tests fail) |
| **Data Analyst** | Insights | Track metrics, detect anomalies, dashboards | ⚠️ Informs decisions, doesn't block |
| **Compliance Officer** | Legal | GDPR/CCPA compliance, data retention, legal risk | ✅ Can block (legal liability) |
| **Marketing Manager** | Strategic | Brand rules, final approval, messaging | ✅ Can block publication |
| **UX/UI Designer** | Strategic | User interfaces, accessibility, usability testing | ✅ Can block launches (accessibility) |
| **Project Lead** | Operational | Coordinate team, remove blockers, manage phases | ✅ Can block (scope/timeline) |

### Advisory Roles (Inform and Challenge — Don't Block Directly)

| Role | Authority | Primary Job | Blocking Power |
|------|-----------|-------------|----------------|
| **Red Team Hacker** | Adversarial Testing | Attack surfaces, prompt injection, exploit discovery | ⚠️ Findings escalate to Infosec Lead who blocks |
| **Devil's Advocate** | Advisory Critical | Challenge assumptions, pre-mortems, failure analysis | ⚠️ Flags risks, doesn't block directly |

**Why separate?** The 12 core roles *own decisions and can block progress*. The advisory roles *inform* those decisions. The Red Team Hacker's findings become Infosec Lead's blocking decisions. The Devil's Advocate's challenges become the team's validated (or invalidated) assumptions. This prevents advisory roles from becoming bottlenecks while ensuring their insights reach the people who can act.

---

## 🔄 WORKFLOW: How Roles Work Together

### PHASE 1: PLANNING (Product Manager + Architect + Devil's Advocate)

```
Product Manager defines:
├─ Mission: "Our system should [do X]"
├─ Success metrics: "[Metric 1], [Metric 2], [Metric 3]"
├─ Phase gates: "Ready to launch when [criteria met]"
└─ Scope boundaries: "Include [this], exclude [that]"

Architect reviews:
├─ "Can we build this with our tech stack?"
├─ "What patterns should we use?"
├─ "Any vendor lock-in risks?"
└─ Recommendation: "Yes, with [approach]" or "No, redesign needed"

Devil's Advocate challenges:
├─ "What assumptions are we making about users?"
├─ "What's the simplest thing that could go wrong?"
├─ "Do we actually need AI for this, or would rules work?"
└─ Pre-mortem: "Imagine this failed — why?"

All agree on Phase 1 success criteria
Devil's Advocate flags documented and addressed or accepted

→ APPROVED TO BUILD
```

### PHASE 2: BUILD (AI Engineer + Architect)

```
AI Engineer writes:
├─ Agent code (following Architect's patterns)
├─ Use factories (LLM factory, DB adapter, etc)
├─ Write unit tests
└─ Submit PR for code review

Architect reviews:
├─ Are factories used? ✅
├─ Any hardcoded vendor choices? ✅
├─ Any anti-patterns? ✅
└─ Tests prove swappability? ✅

QA Engineer reviews:
├─ Coverage >80%? ✅
├─ Performance tests? ✅
├─ Integration tests? ✅
└─ Ready for next phase?

Both approve → CODE MERGED
```

### PHASE 3: SECURITY (Infosec Lead + Database Manager + Red Team Hacker)

```
Database Manager verifies:
├─ Sensitive data encrypted? ✅
├─ Access controls enforced? ✅
├─ Backups working? ✅
└─ Schema supports audit trail? ✅

Infosec Lead verifies:
├─ PII handling correct? ✅
├─ No secrets in logs/code? ✅
├─ Audit trail complete? ✅
└─ Kill switch tested? ✅

Red Team Hacker attacks:
├─ Prompt injection attempts (direct + indirect) ✅
├─ Data exfiltration attempts ✅
├─ Privilege escalation tests ✅
├─ Abuse scenario exploration ✅
└─ Findings report delivered to Infosec Lead

Infosec Lead reviews Red Team findings:
├─ Critical findings? → BLOCK until fixed
├─ High findings? → Fix before next phase gate
├─ Medium/Low? → Backlog with timeline

All approve → SECURITY CLEARED
```

### PHASE 4: QUALITY (QA Engineer + Data Analyst + Devil's Advocate)

```
QA Engineer verifies:
├─ All tests passing? ✅
├─ Latency acceptable? ✅
├─ Error rate <threshold? ✅
└─ Code coverage >80%? ✅

Data Analyst verifies:
├─ Can we measure success metrics? ✅
├─ Dashboard ready? ✅
├─ Baselines established? ✅
└─ Anomaly detection working? ✅

Devil's Advocate reviews:
├─ Edge cases from design review tested? ✅
├─ Failure modes documented? ✅
├─ Graceful degradation path exists? ✅
└─ Unvalidated assumptions flagged in risk register? ✅

All approve → QUALITY GATE PASSED
```

### PHASE 5: DEPLOYMENT (DevOps Manager + Infosec Lead)

```
DevOps Manager verifies:
├─ Infrastructure ready? ✅
├─ Cost within budget? ✅
├─ Monitoring configured? ✅
├─ Rollback plan ready? ✅

Infosec Lead verifies:
├─ Kill switch works? ✅
├─ Audit trail enabled? ✅
├─ Red Team findings resolved? ✅
└─ Emergency procedures documented? ✅

Both approve → GO FOR DEPLOYMENT
```

### PHASE 6: EXECUTION (All Roles Monitor)

```
AI Engineer deploys code

Data Analyst monitors:
├─ Success metrics hitting targets?
├─ Error rate normal?
├─ Anomalies detected?
└─ Reports to Product Manager

Marketing Manager monitors:
├─ Brand compliance maintained?
├─ Quality high?
└─ Approval gates working?

Infosec Lead monitors:
├─ Any security incidents?
├─ Audit trail complete?
├─ Kill switch ready?

DevOps Manager monitors:
├─ Uptime good?
├─ Cost within budget?
├─ Performance acceptable?

Red Team Hacker (at deployment phase gates):
├─ Retest after major updates
└─ Findings to Infosec Lead

All roles report to Product Manager at phase gates
```

---

## 🔗 DECISION AUTHORITY MATRIX

**Who makes the final call?**

```
Decision                          | Authority        | Approvers (can block)
----------------------------------|------------------|--------------------
Deploy to production?             | Product Manager  | QA, Infosec, DevOps
New tech stack component?         | Architect        | Product Manager
Schema change?                    | Database Manager | Architect, Infosec
Activate kill switch?             | Infosec Lead     | Product Manager (notified)
Brand approval for post?          | Marketing Mgr    | None (final call)
Success metric target?            | Product Manager  | Data Analyst (feasible?)
Cost optimization strategy?       | DevOps Manager   | Product Manager (budget)
PII redaction rules?              | Infosec Lead     | Compliance Officer
Compliance requirement?           | Compliance Ofc   | Product Manager (feasible?)
Agent performance acceptable?     | AI Engineer      | QA Engineer (tests pass?)
Security finding severity?        | Infosec Lead     | Red Team (provides evidence)
Assumption valid or invalid?      | Product Manager  | Devil's Advocate (challenges)
Launch despite open risk?         | Product Manager  | Infosec Lead, Devil's Advocate (flag)
Phase advancement?                | Project Lead     | All roles (phase checkpoints)
```

---

## 📊 THE ANTIGRAVITY WORKFLOW

### Agent Manager (Orchestration)

```
Agent Manager has a task:
"Build [Feature]. Success = [Metric]. Phase gate: [Criteria]"

Task workflow:
1. AI Engineer: Claim task → Work on code/agents
2. Architect: Code review on PR → Approve/block
3. QA Engineer: Test review → Approve/block
4. Data Analyst: Set up metrics → Approve
5. DevOps Manager: Deploy → Approve/block
6. Product Manager: Mark complete

If any role blocks:
→ Task stays open
→ Role who blocked explains why
→ Fix applied → Re-review → Continue

Advisory role integration:
→ Devil's Advocate reviews during Phase 1 (planning) and Phase 4 (quality)
→ Red Team Hacker tests during Phase 3 (security) and at deployment gates
→ Neither blocks tasks directly — findings route through blocking roles
```

### Context Files (Documentation)

```
Pinned context files in Agent Manager:
├─ .build-context.md (current status)
├─ MISSION_AND_SUCCESS_METRICS.md (Product Manager)
├─ ARCHITECTURE.md (Architect)
├─ SECURITY_REQUIREMENTS.md (Infosec Lead)
├─ DATABASE_SCHEMA.md (Database Manager)
├─ DEPLOYMENT_CHECKLIST.md (DevOps Manager)
├─ BRAND_RULES.md (Marketing Manager)
├─ COMPLIANCE_REQUIREMENTS.md (Compliance Officer)
├─ RED_TEAM_FINDINGS.md (Red Team Hacker)
└─ RISK_REGISTER.md (Devil's Advocate)

Each role is responsible for keeping their doc current
```

---

## 🛑 WHEN ROLES DISAGREE

### Conflict Between Core Roles

```
Scenario: Architect and QA Engineer disagree on code review

Process:
1. Present positions (2 min each)
2. Product Manager decides based on mission alignment
3. Decision logged in .build-context.md
4. Team moves forward

Key: Product Manager breaks ties (aligns with mission)
```

### When Advisory Roles Are Ignored

```
Scenario: Devil's Advocate flags a risk, Architect dismisses it

Process:
1. Devil's Advocate documents the concern with reasoning
2. Architect responds with counter-reasoning
3. If unresolved: Escalate to Project Lead → Product Manager
4. Core role must: Accept risk (documented) or address it

Key: Advisory concerns are never silently ignored.
     They are either addressed or formally accepted as risks.
```

---

## 📋 ONBOARDING A NEW TEAM MEMBER

**Session 1:**
- Read: MISSION_AND_SUCCESS_METRICS.md
- Read: Their role skill
- Read: ARCHITECTURE.md
- Understand: Who owns what
- Understand: How to communicate with other roles

**Session 2:**
- See: Live Agent Manager tasks
- Ask: Questions answered by their role mentor
- Run: Their first task
- Ready: To contribute

---

## 🎯 SUCCESS METRICS FOR THE WHOLE TEAM

**Tracked at phase gates:**

```
MISSION EXECUTION
├─ Primary metric hitting target? ✅
├─ Secondary metrics on track? ✅
├─ Phase gates passing? ✅
└─ Scope maintained (no creep)? ✅

TEAM HEALTH
├─ All roles productive? ✅
├─ Decisions being made quickly? ✅
├─ Blockers resolved same-session? ✅
├─ Conflicts resolved constructively? ✅
└─ Velocity stable/improving? ✅

TECHNICAL HEALTH
├─ Code quality high? ✅
├─ Tests comprehensive? ✅
├─ Security posture strong? ✅
├─ Infrastructure reliable? ✅
└─ Costs within budget? ✅

ADVERSARIAL HEALTH
├─ Red Team findings resolved on schedule? ✅
├─ Assumptions validated (not just accepted)? ✅
├─ Risk register current? ✅
└─ No "surprises" post-launch? ✅
```

---

## 🔄 SCALING: What to Add When

| Team Size | Approach | Why |
|-----------|----------|-----|
| 1-3 people | One person wears multiple role hats | Too small to specialize |
| 3-5 | Keep all roles, rotate ownership | Roles can overlap |
| 5-8 | 1-2 people per role | Specialization helps |
| 8-15 | Full team (1 per core role) + Project Lead | Coordination becomes critical |
| 15-25 | Dedicated Red Team + Devil's Advocate | Advisory roles need full-time attention |
| 25+ | Add domain experts | Scale challenges emerge |

---

## ✅ QUICK START: Your First Project

**Phase 1 (Planning):** PM + Architect + Devil's Advocate define scope (Devil's Advocate runs pre-mortem)
**Phase 2 (Build):** AI Engineer + Architect design and implement
**Phase 3 (Security):** Infosec Lead + DB Manager audit, Red Team runs attack scan
**Phase 4 (Quality):** QA Engineer verifies, Data Analyst sets up dashboards
**Phase 5 (Deploy):** DevOps Manager deploys, Infosec Lead confirms kill switch
**Phase 6 (Execute):** All roles monitor, iterate

**Result:** By the end of Phase 2, you have a working prototype with validated assumptions and enforced patterns.

---

## 🚀 THE POWER OF THIS STRUCTURE

```
✅ Clear ownership (every decision has an owner)
✅ Built-in oversight (every role reviews others' work)
✅ Risk management (multiple perspectives catch issues)
✅ Adversarial testing (Red Team breaks it before attackers do)
✅ Assumption validation (Devil's Advocate catches groupthink)
✅ Scalable (structure works from 3 people to 30)
✅ Phase-gated (no calendar dependencies, works at any pace)
✅ Antigravity-native (works with agent paradigm)
✅ Reusable (same structure for every project)
```

---

## 🔄 HOW TO ADAPT FOR YOUR PROJECT

1. **Copy this master guide**
2. **For each role:** Customize [YOUR PROJECT] placeholders
3. **Add missing roles:** Use MISSING-ROLES-ASSESSMENT.md
4. **Define success metrics:** Product Manager fills in
5. **Define phase structure:** Discovery → Build → Test → Deploy → Maintain (or your own)
6. **Document decisions:** Keep decision log (decision → owner → reasoning)

---

**This structure is your governance model. It scales from MVP to production.** 🚀
