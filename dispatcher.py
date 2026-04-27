import os
from datetime import datetime
from database import get_session, Lead
from config import RESEND_API_KEY

def dispatch_emails():
    print("Initializing Blue Mountain Dispatcher...")
    if not RESEND_API_KEY:
        print("ERROR: RESEND_API_KEY is missing. Cannot dispatch emails.")
        return

    session = get_session()
    
    # Get all drafted leads
    drafted_leads = session.query(Lead).filter(Lead.email_status == 'Drafted').all()
    
    if not drafted_leads:
        print("No drafted leads found in the database. Run main.py first.")
        return
        
    print(f"Found {len(drafted_leads)} drafted leads ready for dispatch.")
    
    for lead in drafted_leads:
        print(f"\n--- Lead: {lead.business_name} ({lead.city}, {lead.state}) ---")
        print(f"Technical Gap: {lead.tech_gap}")
        print(f"Draft:\n{lead.email_draft}\n")
        
        choice = input("Send this email? (y/n/q to quit): ").strip().lower()
        
        if choice == 'q':
            print("Exiting dispatcher.")
            break
        elif choice == 'y':
            try:
                # Placeholder for Resend API call
                # import resend
                # resend.api_key = RESEND_API_KEY
                # resend.Emails.send(...)
                
                print(f"Sending email to {lead.business_name} via Resend (Simulated)...")
                lead.email_status = 'Sent'
                lead.last_contacted = datetime.utcnow()
                session.commit()
                print("Status updated to 'Sent' in database.")
            except Exception as e:
                print(f"Failed to send email: {e}")
                session.rollback()
        else:
            print("Skipping...")

if __name__ == "__main__":
    dispatch_emails()
