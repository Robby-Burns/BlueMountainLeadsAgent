import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API Keys ---
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")

if not SERPER_API_KEY:
    raise RuntimeError("SERPER_API_KEY is not set. The Regional Scout agent requires it.")
    
if not RESEND_API_KEY:
    raise RuntimeError("RESEND_API_KEY is not set. Email dispatch requires it.")

# --- LLM Provider ---
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

# --- Database ---
# Set DATABASE_URL in your .env to connect to an external DB like Neon.
# Format for Neon: postgresql://[user]:[password]@[host]/[dbname]?sslmode=require
# If not set, it defaults to a local SQLite database 'leads.db'.
DEFAULT_SQLITE_URL = "sqlite:///leads.db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

# --- Feature Toggles & Settings ---
# If True, expand search cities to include Seattle, Portland, Spokane, Boise.
# Default to False (Southeast WA and Northeast OR only).
PNW_TOGGLE = os.getenv("PNW_TOGGLE", "False").lower() in ("true", "1", "yes")

# The maximum number of leads to process before triggering the Human-In-The-Loop gate.
MAX_LEADS_BATCH = int(os.getenv("MAX_LEADS_BATCH", "100"))

# Target cities for the Regional Scout
BASE_TARGET_CITIES = [
    "Kennewick", "Pasco", "Richland", "Walla Walla", "Pendleton", "Hermiston"
]

PNW_TARGET_CITIES = [
    "Seattle", "Portland", "Spokane", "Boise"
]

def get_target_cities():
    if PNW_TOGGLE:
        return BASE_TARGET_CITIES + PNW_TARGET_CITIES
    return BASE_TARGET_CITIES
