import os
import json
import uvicorn
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from crewai import Crew, Process
from config import get_target_cities, MAX_LEADS_BATCH, RESEND_API_KEY
from database import init_db, get_session, Lead, save_leads_gracefully
from agents import (
    create_regional_scout, 
    create_technical_auditor, 
    create_local_strategist,
    create_discovery_task,
    create_audit_task,
    create_drafting_task
)

app = FastAPI(title="BlueMountain Lead Engine")

# Ensure static dir exists
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/health")
def health_check():
    return "OK"

@app.get("/api/leads")
def get_leads():
    session = get_session()
    leads = session.query(Lead).order_by(Lead.created_at.desc()).all()
    
    return [
        {
            "id": lead.id,
            "business_name": lead.business_name,
            "city": lead.city,
            "state": lead.state,
            "tech_gap": lead.tech_gap,
            "email_status": lead.email_status,
            "email_draft": lead.email_draft,
            "created_at": lead.created_at
        } for lead in leads
    ]

# Keep track if crew is running
is_crew_running = False

def run_crew_job():
    global is_crew_running
    try:
        session = get_session()
        pending_count = session.query(Lead).filter(Lead.email_status.in_(['Pending', 'Drafted'])).count()
        if pending_count >= MAX_LEADS_BATCH:
            print("HitL limit reached. Aborting crew run.")
            return

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
        
        result = crew.kickoff()
        
        leads_data = []
        if not result or not hasattr(result, 'pydantic') or not result.pydantic:
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
        else:
            leads_data = [lead.dict() for lead in result.pydantic.leads]

        save_leads_gracefully(session, leads_data)
        
    finally:
        is_crew_running = False

@app.post("/api/run-crew")
def trigger_crew(background_tasks: BackgroundTasks):
    global is_crew_running
    if is_crew_running:
        raise HTTPException(status_code=400, detail="Crew is already running.")
    
    is_crew_running = True
    background_tasks.add_task(run_crew_job)
    return {"message": "Crew AI Engine started in the background."}

class DispatchRequest(BaseModel):
    contact_email: str

@app.post("/api/dispatch/{lead_id}")
def dispatch_email(lead_id: int, req: DispatchRequest):
    session = get_session()
    lead = session.query(Lead).filter_by(id=lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
        
    if not RESEND_API_KEY:
        raise HTTPException(status_code=500, detail="RESEND_API_KEY not set. Check .env")
        
    try:
        import resend
        resend.api_key = RESEND_API_KEY
        
        resend.Emails.send({
            "from": "Acquisition <hello@bluemountaindigital.com>", 
            "to": req.contact_email,
            "subject": f"Quick question about {lead.business_name}'s website",
            "text": lead.email_draft
        })
        
        lead.email_status = 'Sent'
        session.commit()
        return {"message": "Email sent successfully."}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
