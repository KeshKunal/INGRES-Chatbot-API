from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base 
from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def execute_query(query_json: dict) -> list:
    """
    Safely builds and executes a SQL query from the complete JSON object (fields and filters).
    """
    # ---- DYNAMICALLY SELECT COLUMNS ----
    fields_to_select = query_json.get("fields", ["STATES", "DISTRICT"]) # Default to selecting state and district if not specified
    # Safety Check: Ensure no malicious field names are passed. We only allow valid column names.
    # This is a simplified check. A more robust version would compare against a predefined list of all valid columns.
    safe_fields = [f'"{field}"' for field in fields_to_select if field.replace('_', '').isalnum()]
    
    if not safe_fields:
        safe_fields = ['"STATES"', '"DISTRICT"'] # Fallback to default
        
    select_clause = ", ".join(safe_fields)
    
    # ---- DYNAMICALLY BUILD FILTERS ----
    filters = query_json.get("filters", {})
    query_builder = [f'SELECT {select_clause} FROM public."ingressdata2025" WHERE 1=1']
    params = {}

    if 'state' in filters:
        query_builder.append('AND "STATES" ILIKE :state')
        params['state'] = f"%{filters['state']}%"

    if 'district' in filters:
        query_builder.append('AND "DISTRICT" ILIKE :district')
        params['district'] = f"%{filters['district']}%"
    
    # Add a safety limit to prevent returning too many records
    query_builder.append("LIMIT 20")
    
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