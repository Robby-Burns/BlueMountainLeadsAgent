import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Lead, save_leads_gracefully
from main import process_crew_output
import json

@pytest.fixture
def db_session():
    # Use in-memory SQLite for testing
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_save_leads_gracefully(db_session):
    leads_data = [
        {
            "business_name": "Bob's Plumbing",
            "city": "Kennewick",
            "state": "WA",
            "verified_tech_gap": "No virtual tour",
            "email_draft": "Hi Bob..."
        },
        {
            "business_name": "Alice's Bakery",
            "city": "Richland",
            "state": "WA",
            "verified_tech_gap": "HTTP site",
            "email_draft": "Hi Alice..."
        }
    ]
    
    # First save should succeed
    saved = save_leads_gracefully(db_session, leads_data)
    assert saved == 2
    assert db_session.query(Lead).count() == 2
    
    # Try to save same leads again
    saved_again = save_leads_gracefully(db_session, leads_data)
    assert saved_again == 0 # Duplicates skipped
    assert db_session.query(Lead).count() == 2 # Still 2
    
    # Save a new lead with identical city but different name
    new_lead = [{
         "business_name": "Charlie's Plumbing",
         "city": "Kennewick",
         "state": "WA",
         "verified_tech_gap": "HTTP site",
         "email_draft": "Hi Charlie..."
    }]
    saved_new = save_leads_gracefully(db_session, new_lead)
    assert saved_new == 1
    assert db_session.query(Lead).count() == 3

class MockPydanticLeads:
    def __init__(self, leads):
        self.leads = leads

class MockPydanticResult:
    def __init__(self, leads):
        self.pydantic = MockPydanticLeads(leads)
        self.raw = ""

class MockLead:
    def __init__(self, data):
        self.data = data
    def dict(self):
        return self.data

class MockRawResult:
    def __init__(self, raw_str):
        self.raw = raw_str
        self.pydantic = None

def test_process_crew_output_valid_pydantic(db_session):
    mock_leads = [
        MockLead({
            "business_name": "Test Pydantic Business",
            "city": "Seattle",
            "state": "WA",
            "verified_tech_gap": "No website",
            "email_draft": "Hello!"
        })
    ]
    result = MockPydanticResult(mock_leads)
    
    process_crew_output(result, db_session)
    
    # Check that it saved
    assert db_session.query(Lead).count() == 1
    lead = db_session.query(Lead).first()
    assert lead.business_name == "Test Pydantic Business"

def test_process_crew_output_fallback(db_session):
    raw_json = json.dumps([{
        "business_name": "Test Fallback Business",
        "city": "Spokane",
        "state": "WA",
        "tech_gap": "Old website",
        "email_draft": "Hi there!"
    }])
    result = MockRawResult(f"```json\n{raw_json}\n```")
    
    process_crew_output(result, db_session)
    
    assert db_session.query(Lead).count() == 1
    lead = db_session.query(Lead).first()
    assert lead.business_name == "Test Fallback Business"
    assert lead.tech_gap == "Old website"
