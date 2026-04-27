from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE_URL

# Set up declarative base for models
Base = declarative_base()

class Lead(Base):
    """
    Represents a Lead found by the agents.
    """
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    
    # Lead categorization
    # e.g., 'Ghost', 'Facebook Only', 'Missing Virtual Tour'
    lead_type = Column(String, nullable=True)
    
    # Specific technical gap identified by Auditor
    tech_gap = Column(String, nullable=True)
    
    # Email Status: Pending, Drafted, Sent, Bounced
    email_status = Column(String, default="Pending")
    
    # Drafted email body
    email_draft = Column(String, nullable=True)
    
    # Tracking
    last_contacted = Column(DateTime, nullable=True)
    bite_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Ensure no duplicates per business in a city
    __table_args__ = (
        UniqueConstraint('business_name', 'city', name='uq_business_city'),
    )

    def __repr__(self):
        return f"<Lead(business_name='{self.business_name}', city='{self.city}', status='{self.email_status}')>"


# Create engine and session factory
# Adding pool_pre_ping=True to handle connection drops gracefully, useful for Neon DBs.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize the database, creating all tables if they do not exist.
    """
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized. Connected to: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}")

def get_session():
    """
    Returns a new SQLAlchemy database session.
    """
    return SessionLocal()

def save_leads_gracefully(session, leads_data):
    """
    Saves leads to the database gracefully, catching IntegrityErrors for duplicates.
    """
    saved_count = 0
    for lead_data in leads_data:
        try:
            # Check if this lead already exists to avoid duplicates
            existing = session.query(Lead).filter_by(
                business_name=lead_data.get('business_name'),
                city=lead_data.get('city')
            ).first()
            
            if not existing:
                new_lead = Lead(
                    business_name=lead_data.get('business_name'),
                    city=lead_data.get('city'),
                    state=lead_data.get('state', 'WA'),
                    tech_gap=lead_data.get('verified_tech_gap', lead_data.get('tech_gap')),
                    email_draft=lead_data.get('email_draft'),
                    email_status="Drafted"
                )
                session.add(new_lead)
                session.commit()
                saved_count += 1
        except IntegrityError:
            session.rollback()
            print(f"Skipped duplicate lead due to constraint: {lead_data.get('business_name')} in {lead_data.get('city')}")
        except Exception as e:
            session.rollback()
            print(f"Database error while saving lead {lead_data.get('business_name')}: {e}")
            
    return saved_count
