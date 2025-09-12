# setup_db.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db import engine
from sqlalchemy import text

# Create sample groundwater table
create_table_sql = """
CREATE TABLE IF NOT EXISTS groundwater_data (
    id SERIAL PRIMARY KEY,
    assessment_unit VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    groundwater_level NUMERIC(10, 2),
    category VARCHAR(50),
    extraction_stage VARCHAR(20),
    latitude NUMERIC(10, 6),
    longitude NUMERIC(10, 6)
);
"""

# Sample data
sample_data = """
INSERT INTO groundwater_data (assessment_unit, year, groundwater_level, category, extraction_stage, latitude, longitude)
VALUES
('Chennai', 2022, 8.2, 'Over-exploited', '95%', 13.0827, 80.2707),
('Chennai', 2021, 7.5, 'Over-exploited', '90%', 13.0827, 80.2707),
('Bengaluru', 2022, 12.5, 'Critical', '85%', 12.9716, 77.5946),
('Mathikere, Bengaluru', 2023, 13.2, 'Critical', '95%', 13.0307, 77.5646),
('Delhi', 2022, 15.8, 'Over-exploited', '98%', 28.7041, 77.1025),
('Mumbai', 2022, 5.2, 'Safe', '60%', 19.0760, 72.8777),
('Kolkata', 2022, 4.5, 'Safe', '55%', 22.5726, 88.3639),
('Hyderabad', 2022, 9.8, 'Semi-critical', '75%', 17.3850, 78.4867),
('Pune', 2022, 7.4, 'Semi-critical', '72%', 18.5204, 73.8567),
('Jaipur', 2022, 18.6, 'Over-exploited', '95%', 26.9124, 75.7873)
"""

try:
    with engine.connect() as conn:
        conn.execute(text(create_table_sql))
        conn.execute(text("DELETE FROM groundwater_data"))  # Clear existing data
        conn.execute(text(sample_data))
        conn.commit()
        print("Sample data created successfully!")
except Exception as e:
    print(f"Error setting up sample data: {str(e)}")