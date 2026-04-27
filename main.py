import json
import threading
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from crewai import Crew, Process
from config import get_target_cities, MAX_LEADS_BATCH
from database import init_db, get_session, Lead, save_leads_gracefully
from agents import (
    create_regional_scout, 
    create_technical_auditor, 
    create_local_strategist,
    create_discovery_task,
    create_audit_task,
    create_drafting_task
)

# --- Health Check Server ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()
            
    def log_message(self, format, *args):
        pass # Silence logging to keep CrewAI console clean

def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return port

def process_crew_output(result, session):
    """
    Parses the Pydantic output from the Crew and saves drafted leads to the database.
    """
    leads_data = []
    if not result or not hasattr(result, 'pydantic') or not result.pydantic:
        print("Crew did not return valid Pydantic output. Falling back to raw JSON parsing if possible...")
        try:
            raw = getattr(result, 'raw', str(result))
            clean_json = raw.strip()
            if clean_json.startswith("```json"):
                clean_json = clean_json[7:-3]
            elif clean_json.startswith("```"):
                clean_json = clean_json[3:-3]
            leads_data = json.loads(clean_json)
        except Exception as e:
            print(f"Failed to process output entirely. Error: {e}")
            return
    else:
        # Pydantic is safely accessible
        leads_data = [lead.dict() for lead in result.pydantic.leads]

    saved_count = save_leads_gracefully(session, leads_data)
    print(f"Successfully saved {saved_count} new drafted leads to the database.")

def main():
    print("Initializing Blue Mountain Digital Marketing Lead Engine...")
    port = start_health_server()
    print(f"Started background /health server on port {port}.")
    
    # 1. Initialize Database
    init_db()
    session = get_session()
    
    # 2. Check HitL / Batch limits before running
    # Count how many Pending/Drafted leads we currently have.
    pending_count = session.query(Lead).filter(Lead.email_status.in_(['Pending', 'Drafted'])).count()
    
    if pending_count >= MAX_LEADS_BATCH:
        print(f"\n--- HUMAN-IN-THE-LOOP GATE TRIGGERED ---")
        print(f"You have {pending_count} pending/drafted leads, which meets/exceeds the max batch of {MAX_LEADS_BATCH}.")
        print("Please review and dispatch these emails by running: python dispatcher.py")
        print("Pausing engine. Keeping container alive for health checks...")
        while True:
            time.sleep(3600)
        
    # 3. Setup Crew
    print("Setting up AI Crew...")
    scout = create_regional_scout()
    auditor = create_technical_auditor()
    strategist = create_local_strategist()
    
    target_cities = get_target_cities()
    
    discovery = create_discovery_task(scout, target_cities)
    audit = create_audit_task(auditor, discovery)
    drafting = create_drafting_task(strategist, audit)
    
    crew = Crew(
        agents=[scout, auditor, strategist],
        tasks=[discovery, audit, drafting],
        process=Process.sequential,
        verbose=True
    )
    
    # 4. Run the Crew
    print(f"Kicking off crew for cities: {', '.join(target_cities)}...")
    result = crew.kickoff()
    
    # 5. Save Results
    print("Crew finished. Processing results...")
    process_crew_output(result, session)
    
    # Check if we hit the limit after saving
    new_pending_count = session.query(Lead).filter(Lead.email_status.in_(['Pending', 'Drafted'])).count()
    if new_pending_count >= MAX_LEADS_BATCH:
        print(f"\n--- HUMAN-IN-THE-LOOP GATE TRIGGERED ---")
        print(f"You now have {new_pending_count} drafted leads ready for review.")

    print("\nEngine process complete. Keeping container alive for health checks...")
    while True:
        time.sleep(3600)

if __name__ == "__main__":
    main()
