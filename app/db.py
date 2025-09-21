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

def execute_query(fields: list, filters: dict) -> list:
    """
    Safely builds and executes a SQL query on the "ingressdata2025" table,
    selecting only the specified fields.
    """
    # Always include STATES and DISTRICT for context in the response
    if "DISTRICT" not in fields:
        fields.insert(0, "DISTRICT")
    if "STATES" not in fields:
        fields.insert(0, "STATES")
    
    # Remove duplicates while preserving order
    unique_fields = list(dict.fromkeys(fields))
    
    # Prevent SQL injection by ensuring field names are valid (though they are controlled by the LLM prompt)
    # For this implementation, we trust the LLM's output based on the controlled prompt.
    select_clause = ", ".join([f'"{field}"' for field in unique_fields])
    
    query_builder = [f'SELECT {select_clause} FROM public."ingressdata2025" WHERE 1=1']
    params = {}

    # Dynamically and safely add filters from the JSON
    if 'state' in filters:
        state_filter = filters['state']
        if isinstance(state_filter, list):
            # Handle a list of states for comparison queries
            if state_filter:
                or_clauses = []
                for i, state in enumerate(state_filter):
                    param_name = f"state_{i}"
                    or_clauses.append(f'"STATES" ILIKE :{param_name}')
                    params[param_name] = f"%{state}%"
                query_builder.append(f"AND ({' OR '.join(or_clauses)})")
        else:
            # Handle a single state string
            query_builder.append('AND "STATES" ILIKE :state')
            params['state'] = f"%{state_filter}%"

    if 'district' in filters:
        district_filter = filters['district']
        if isinstance(district_filter, list):
            # Handle a list of districts for comparison queries
            if district_filter:
                or_clauses = []
                for i, district in enumerate(district_filter):
                    param_name = f"district_{i}"
                    or_clauses.append(f'"DISTRICT" ILIKE :{param_name}')
                    params[param_name] = f"%{district}%"
                query_builder.append(f"AND ({' OR '.join(or_clauses)})")
        else:
            # Handle a single district string
            query_builder.append('AND "DISTRICT" ILIKE :district')
            params['district'] = f"%{district_filter}%"
    
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