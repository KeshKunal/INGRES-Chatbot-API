# In app/db.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

# Database setup
SQLALCHEMY_DATABASE_URL = settings.get_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def execute_query(filters: dict) -> list:
    """
    Safely builds and executes a SQL query on the "ingressdata2025" table.
    """
    # Use the confirmed table name
    query_builder = ['SELECT "STATES", "DISTRICT", "RainfallTotal", "AnnualGroundwaterRechargeTotal" FROM public."ingressdata2025" WHERE 1=1']
    params = {}

    # Dynamically and safely add filters from the JSON
    if 'state' in filters:
        query_builder.append('AND "STATES" ILIKE :state')
        params['state'] = f"%{filters['state']}%"

    if 'district' in filters:
        query_builder.append('AND "DISTRICT" ILIKE :district')
        params['district'] = f"%{filters['district']}%"
    
    # You can add more filters here for other columns as needed...

    final_query = " ".join(query_builder)

    with SessionLocal() as session:
        try:
            result = session.execute(text(final_query), params)
            columns = result.keys()
            results_as_dict = [dict(zip(columns, row)) for row in result.fetchall()]
            return results_as_dict
        except Exception as e:
            logger.error(f"Database query failed: {e}")
            return []