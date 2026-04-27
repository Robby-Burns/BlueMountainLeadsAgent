import pytest
from crewai import Agent
from agents import create_regional_scout, create_technical_auditor, create_local_strategist, SafeScrapeWebsiteTool

def test_agents_initialization():
    scout = create_regional_scout()
    assert isinstance(scout, Agent)
    assert scout.role == "Regional Scout"
    
    auditor = create_technical_auditor()
    assert isinstance(auditor, Agent)
    assert auditor.role == "Technical Auditor"
    
    strategist = create_local_strategist()
    assert isinstance(strategist, Agent)
    assert strategist.role == "Local Strategist"

def test_safe_scrape_tool_handles_exceptions(mocker):
    tool = SafeScrapeWebsiteTool()
    
    # Mock the underlying run to throw an exception
    mocker.patch('crewai_tools.ScrapeWebsiteTool._run', side_effect=Exception("Simulated HTTP 404"))
    
    result = tool._run(website_url="http://broken.test")
    assert "Assume technical gap exists" in result
    assert "Simulated HTTP 404" in result
