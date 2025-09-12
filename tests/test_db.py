import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import engine
from sqlalchemy import text

# Test connection
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Database connection successful!")
        
        # List tables to see what's available
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
        print("\nAvailable tables:")
        for row in result:
            print(f"- {row[0]}")
except Exception as e:
    print(f"Database connection failed: {str(e)}")