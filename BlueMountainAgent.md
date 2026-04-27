# Project: Blue Mountain Digital Marketing Lead Engine
# Stack: Python, CrewAI, SQLite, Serper.dev API, Resend API

Act as a Senior Python Developer and AI Architect. We are building a lead generation engine for a digital marketing agency called "Blue Mountain Digital Marketing" located in Kennewick, WA. 

## The Objective
Build a modular CrewAI system that identifies "Digital Ghost" leads (legacy Google Sites, Facebook-only presences, and businesses missing Virtual Tours) in Southeast Washington and Northeast Oregon.

## Technical Requirements
1. **Database (Memory):** Setup a local SQLite database (`leads.db`) with a table `leads`. 
   - Columns: `id`, `business_name`, `city`, `state`, `industry`, `source_url`, `lead_type` (Ghost/FB/Tour), `tech_gap`, `email_status` (Pending/Sent/Bounced), `last_contacted`, and `bite_count`.
   - Ensure a `UNIQUE` constraint on `business_name` and `city` to prevent duplicates.

2. **Agents:** Define three CrewAI Agents:
   - **The Regional Scout:** Uses `SerperDevTool` to find leads based on "Google Dorks" (e.g., site:sites.google.com "Walla Walla").
   - **The Technical Auditor:** Uses `ScrapeWebsiteTool` to verify if a site is insecure (HTTP), legacy, or if the "Website" link on a Maps profile leads only to Facebook.
   - **The Local Strategist:** Drafts a "Value-First" email tailored to the lead’s city and gap, emphasizing Blue Mountain's #1 local ranking.

3. **Functionality:**
   - Create a "PNW Toggle" variable. If True, expand search cities to include Seattle, Portland, Spokane, Boise.
   - Implement a "Human-in-the-Loop" gate: The system should process 100 leads, save drafts to the DB, and then PAUSE for a manual trigger before sending.
   - Integration for **Resend API** for email dispatch and a placeholder for link-click webhooks to track the "Bite."

## Initial Task
Write the boilerplate code for:
1. The SQLite database initialization script.
2. The CrewAI agent definitions using the `crewai` and `crewai_tools` libraries.
3. A `config.py` structure to hold the Serper and Resend API keys.

Make the code modular, handle errors gracefully (don't crash on a 404 website), and ensure the "Local Strategist" agent uses a professional, elevated-classic tone suitable for the Columbia Basin business community.