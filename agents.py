from crewai import Agent, Task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel
from typing import List, Optional
import os
from factories.llm_factory import get_llm_provider

# Initialize Tools
# Ensure SERPER_API_KEY is set in environment, as SerperDevTool requires it.
search_tool = SerperDevTool()

class SafeScrapeWebsiteTool(ScrapeWebsiteTool):
    def _run(self, *args, **kwargs):
        try:
            return super()._run(*args, **kwargs)
        except Exception as e:
            return f"Error: Could not scrape site. Assume technical gap exists (e.g., legacy or broken site). Details: {e}"

scrape_tool = SafeScrapeWebsiteTool()

# --- Pydantic Models ---
class LeadOutput(BaseModel):
    business_name: str
    city: str
    state: Optional[str] = "WA"
    verified_tech_gap: str
    email_draft: str

class LeadListOutput(BaseModel):
    leads: List[LeadOutput]

# --- Agents ---

def create_regional_scout() -> Agent:
    """
    The Regional Scout uses Google Dorks via Serper to find target leads
    (legacy sites, facebook-only pages).
    """
    return Agent(
        role="Regional Scout",
        goal="Discover potential 'Digital Ghost' leads in the target cities by identifying legacy websites or Facebook-only presences.",
        backstory="""You are an expert digital prospector. You know how to use advanced search operators (Google Dorks)
        to find local businesses in specific cities that either use outdated website platforms (like legacy Google Sites)
        or have no website at all, relying entirely on a Facebook page.""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=get_llm_provider()
    )

def create_technical_auditor() -> Agent:
    """
    The Technical Auditor validates the leads by scraping the sites to check for
    HTTP protocols, outdated metadata, or redirect chains to Facebook.
    """
    return Agent(
        role="Technical Auditor",
        goal="Verify the technical gaps of prospective leads by analyzing their website content and metadata.",
        backstory="""You are a sharp technical analyst. You can look at a business's online footprint
        and immediately spot critical flaws: insecure HTTP connections, archaic HTML structures,
        or when a business uses a social media page as their primary website. You never make assumptions;
        you verify everything by inspecting the site data. If a site returns a 404, you gracefully note it as 'Dead Site'
        rather than failing.""",
        verbose=True,
        allow_delegation=False,
        tools=[scrape_tool],
        llm=get_llm_provider()
    )

def create_local_strategist() -> Agent:
    """
    The Local Strategist drafts the highly-tailored "Value-First" emails.
    """
    return Agent(
        role="Local Strategist",
        goal="Draft highly tailored, value-first emails to leads based on their specific technical gaps and location.",
        backstory="""You are a Senior Digital Marketing Strategist for Blue Mountain Digital Marketing,
        the premier marketing agency in the Columbia Basin. You write with an elevated-classic, professional tone.
        You emphasize the value of local expertise. When you see a technical gap (like a missing virtual tour
        or an insecure website), you frame it as a missed opportunity for growth rather than a criticism.
        You ensure every email feels personalized to the local community.""",
        verbose=True,
        allow_delegation=False,
        llm=get_llm_provider()
        # No specific external tools needed for drafting text
    )

# --- Tasks ---

def create_discovery_task(scout_agent: Agent, target_cities: list) -> Task:
    cities_str = ", ".join(target_cities)
    return Task(
        description=f"""
        Use advanced search queries to find 5 local businesses across the following cities: {cities_str}.
        Focus on finding businesses that match one of these criteria:
        1. They use a legacy website builder (e.g., sites.google.com, wixsite.com).
        2. They list a Facebook page as their primary website.
        3. They are local service businesses likely missing modern digital assets like virtual tours.
        
        Return a structured list of leads containing: Business Name, City, State, Website/URL, and Industry.
        """,
        expected_output="A list of 5 business leads formatted as JSON, each with business_name, city, state, url, industry, and a suspected lead_type.",
        agent=scout_agent
    )

def create_audit_task(auditor_agent: Agent, discovery_task: Task) -> Task:
    return Task(
        description="""
        Review the list of leads provided by the Regional Scout.
        For each lead with a URL, attempt to scrape the website to verify the technical gap.
        Identify whether the site is HTTP (insecure), heavily outdated, broken (404), or just a Facebook page.
        Do not crash on 404s; handle them gracefully by marking the tech gap as 'Dead Link/404'.
        """,
        expected_output="A verified list of leads as JSON, appending 'verified_tech_gap' to each lead record.",
        agent=auditor_agent,
        context=[discovery_task]
    )

def create_drafting_task(strategist_agent: Agent, audit_task: Task) -> Task:
    return Task(
        description="""
        Using the verified list of leads from the Technical Auditor, draft a customized 'Value-First' email for each.
        The email must:
        1. Mention their specific city and business name.
        2. Highlight the specific technical gap identified (e.g., why an insecure site hurts local SEO).
        3. Position Blue Mountain Digital Marketing as the #1 local expert in the Columbia Basin ready to help.
        4. Include a clear, low-pressure call to action.
        """,
        expected_output="A JSON array of objects, where each object contains the business_name, city, verified_tech_gap, and the final email_draft.",
        agent=strategist_agent,
        context=[audit_task],
        output_pydantic=LeadListOutput
    )
