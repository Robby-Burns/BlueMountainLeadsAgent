# 🎛️ Configuration Control - Cost-Aware Scaling & Multi-Environment

**Version:** 1.6.0 | **Updated:** March 19, 2026 | **Part:** 8/10  
**Status:** Production Ready ✅  
**Purpose:** Control system behavior via configuration (`scale.yaml`), not code changes.

---

## 📍 Purpose

This file teaches you to build **cost-aware, scalable systems** where you change `scale.yaml` to scale from $20/mo → $500+/mo. No code rewrites needed.

**Core Philosophy:** "Configuration as Code. Costs as Data."

---

## 🎛️ The Control File: `scale.yaml`

This project natively implements `config/scale.yaml` as its single source of truth. All environment toggles and audit controls map through this configuration structure:

```yaml
# 🎛️ SYSTEM CONTROL PANEL

deployment:
  tier: "small"                 # Options: learning, small, growing, enterprise
  environment: "dev"            # Options: dev, staging, prod

# 🧠 CONTEXT MANAGEMENT
context_management:
  max_history_messages: 20
  truncation_strategy: "summarize_oldest" # Options: summarize_oldest, drop_oldest, strict_cutoff
  rag_top_k_results: 5
  # Archive thresholds — triggers /archive-memory when either is exceeded
  archive_threshold_lines: 500          # Max lines in .build-context.md before archive recommended
  archive_threshold_age_days: 14        # Resolved bugs/completed features older than this are archive candidates

# 🎼 ORCHESTRATION ENGINE
orchestration:
  engine: "antigravity"         # Options: antigravity, simple_async, langgraph, crewai
  max_steps: 15                 # Prevent infinite loops

# 🤖 LLM INTELLIGENCE
llm:
  primary:
    provider: "anthropic"       # Switch via Agnostic Factory
    model: "claude-3-5-sonnet"
  routing:
    simple_tasks: "claude-3-haiku"
    critical_tasks: "claude-3-opus"

# 💾 DATA PERSISTENCE
database:
  type: "postgresql"            # Options: sqlite, postgresql, qdrant

# 📄 WORKERS & ASYNC SCALING
workers:
  enabled: false                # Redis/Celery background tasks

# 💰 BUDGET GUARDRAILS
cost_controls:
  hard_limit_usd: 50.00
  alert_threshold_usd: 40.00

# 🔍 SCHEDULED AUDIT
audit:
  schedule_interval_months: 6              # How often to run (recommended: 6)
  schedule_day: "first_monday"             # Which day of the scheduled month
  schedule_time: "06:00"              # 24-hour format
  schedule_timezone: "UTC"            # All server schedules in UTC
  notification_channel: "none"        # Options: slack | email | teams | webhook | none
  notification_link: "https://your-dashboard.com/audit"
  auto_apply: false                   # Never true. Human approves all changes.
  cve_check_weekly: true              # Weekly CVE scan between audits
```

---

## ⚙️ Implementation: Python + Pydantic

Ensure your configuration loads reliably and fails fast if incorrect:

```python
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from typing import List
import yaml, os

class ContextManagementConfig(BaseModel):
    max_history_messages: int
    truncation_strategy: str
    rag_top_k_results: int
    archive_threshold_lines: int = 500
    archive_threshold_age_days: int = 14

class OrchestrationConfig(BaseModel):
    engine: str
    max_steps: int

class AuditConfig(BaseModel):
    schedule_interval_months: int
    schedule_day: str
    schedule_time: str
    schedule_timezone: str
    notification_channel: str
    notification_link: str
    auto_apply: bool  # Must always be False
    cve_check_weekly: bool

class AppConfig(BaseSettings):
    context_management: ContextManagementConfig
    orchestration: OrchestrationConfig
    audit: AuditConfig
    
    @classmethod
    def load(cls, yaml_path: str = "config/scale.yaml"):
        with open(yaml_path) as f:
            config_data = yaml.safe_load(f)
        
        config = cls(**config_data)
        
        # Hard safety check: auto_apply must never be True
        if config.audit.auto_apply:
            raise ValueError(
                "FATAL: audit.auto_apply is True. "
                "This is forbidden. Human sign-off is mandatory."
            )
        
        return config

# Crash immediately if config is broken
config = AppConfig.load()
```

---

## 📌 Environment Constraints

Ensure the explicit `.env` file (which is git-ignored) contains the underlying bounds supporting the infrastructure logic. If utilizing standard fallback logic, you must supply:

- `LLM_PROVIDER`: gemini, openai, anthropic
- `EMBEDDER_PROVIDER`: gemini, openai
- `GOOGLE_API_KEY`: Required for active DB vectorizations
- `GOOGLE_MAPS_API_KEY`: Optional; utilized by GeoLogisticsFactory or deferred to mapping Sandboxes.
- `SHOPVOX_API_KEY`: Required 
- `NEON_DATABASE_URL`: Expected vector location

Note: `docker-compose.yml` now includes `db` and optional `redis` services; see the updated file for required env vars like `POSTGRES_USER` and `REDIS_URL`.

---

## 📌 File Meta

**Version:** 1.6.0  
**Released:** March 19, 2026  
**Status:** Production Ready ✅  
**Part of:** 10-Part AI Agent Framework  

**Next File:** [08_AGNOSTIC_FACTORIES.md](./08_AGNOSTIC_FACTORIES.md)
