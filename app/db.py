from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base # <-- ADD THIS MISSING IMPORT
from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

# Database setup
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() # This line will now work correctly

def execute_query(fields: list, filters: dict) -> list:
    """
    Safely builds and executes a SQL query using robust, case-insensitive
    filtering with IN clauses for lists.
    """
    # Ensure key fields are always present and uppercase for consistency
    required_fields = {"STATES", "DISTRICT"}
    field_set = {f.upper() for f in fields}
    field_set.update(required_fields)
    
    unique_fields = list(field_set)
    # Use aliases to standardize output keys to lowercase, preventing downstream errors
    select_clause = ", ".join([f'"{field}" AS {field.lower()}' for field in unique_fields])
    
    query_builder = [f'SELECT {select_clause} FROM public."ingressdata2025" WHERE 1=1']
    params = {}

    # Handle filters case-insensitively
    if 'state' in filters:
        state_filter = filters['state']
        if isinstance(state_filter, list):
            if state_filter:
                query_builder.append('AND UPPER("STATES") IN :states')
                params['states'] = tuple(s.upper() for s in state_filter)
        else:
            query_builder.append('AND UPPER("STATES") LIKE UPPER(:state)')
            params['state'] = f"%{state_filter}%"

    if 'district' in filters:
        district_filter = filters['district']
        if isinstance(district_filter, list):
            if district_filter:
                query_builder.append('AND UPPER("DISTRICT") IN :districts')
                params['districts'] = tuple(d.upper() for d in district_filter)
        else:
            query_builder.append('AND UPPER("DISTRICT") LIKE UPPER(:district)')
            params['district'] = f"%{district_filter}%"
    
    final_query = " ".join(query_builder)
    logger.info(f"Executing Query: {final_query}")
    logger.info(f"With Params: {params}")

    with SessionLocal() as session:
        try:
            result = session.execute(text(final_query), params)
            columns = result.keys()
            results_as_dict = [dict(zip(columns, row)) for row in result.fetchall()]
            logger.info(f"Query successful, returned {len(results_as_dict)} rows.")
            return results_as_dict
        except Exception as e:
            logger.error(f"DATABASE QUERY FAILED: {e}", exc_info=True)
            return []