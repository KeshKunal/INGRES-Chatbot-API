# app/services.py
from .api.schemas import ChatRequest
from .config import settings
import logging
import json
from sarvamai import SarvamAI

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        # Initialize Sarvam AI client
        self.client = SarvamAI(api_subscription_key=settings.LLM_API_KEY)
        
        # Mock database schema - this will help LLM generate proper SQL
        self.database_schema = """
        Database Schema:
        Table: groundwater_data
        - id (integer, primary key)
        - district (text)
        - state (text) 
        - water_level (float, in meters)
        - status (text: 'Critical', 'Semi-Critical', 'Safe')
        - recorded_date (date)
        
        Table: rainfall_data  
        - id (integer, primary key)
        - district (text)
        - state (text)
        - rainfall_mm (float)
        - month (text)
        - year (integer)
        """

        
        # Mock database data
        self.mock_data = {
            "groundwater_data": [
                {"id": 1, "district": "Delhi", "state": "Delhi", "water_level": 15.2, "status": "Critical", "recorded_date": "2024-01-15"},
                {"id": 2, "district": "Gurgaon", "state": "Haryana", "water_level": 25.8, "status": "Safe", "recorded_date": "2024-01-15"},
                {"id": 3, "district": "Hyderabad", "state": "Telangana", "water_level": 18.5, "status": "Semi-Critical", "recorded_date": "2024-01-15"},
                {"id": 4, "district": "Mumbai", "state": "Maharashtra", "water_level": 12.3, "status": "Critical", "recorded_date": "2024-01-15"},
                {"id": 5, "district": "Chennai", "state": "Tamil Nadu", "water_level": 8.9, "status": "Critical", "recorded_date": "2024-01-15"},
            ],
            "rainfall_data": [
                {"id": 1, "district": "Delhi", "state": "Delhi", "rainfall_mm": 45.5, "month": "January", "year": 2024},
                {"id": 2, "district": "Hyderabad", "state": "Telangana", "rainfall_mm": 32.1, "month": "January", "year": 2024},
                {"id": 3, "district": "Mumbai", "state": "Maharashtra", "rainfall_mm": 78.2, "month": "January", "year": 2024},
            ]
        }

    def call_sarvam_ai(self, messages: list) -> str:
        """
        Makes API call to Sarvam AI using the official SDK
        """
        try:
            response = self.client.chat.completions(messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling Sarvam AI: {str(e)}")
            return "Sorry, I'm having trouble processing your request right now."

    def execute_mock_sql(self, sql_query: str) -> list:
        """
        Simulates SQL execution on mock data
        """
        try:
            # Simple mock - look for table names and return relevant data
            sql_lower = sql_query.lower()
            
            if "groundwater_data" in sql_lower:
                # Filter based on common WHERE conditions
                data = self.mock_data["groundwater_data"].copy()
                
                # Simple filtering logic
                if "delhi" in sql_lower:
                    data = [row for row in data if "Delhi" in row["district"]]
                elif "hyderabad" in sql_lower:
                    data = [row for row in data if "Hyderabad" in row["district"]]
                elif "mumbai" in sql_lower:
                    data = [row for row in data if "Mumbai" in row["district"]]
                elif "critical" in sql_lower:
                    data = [row for row in data if row["status"] == "Critical"]
                
                return data
                
            elif "rainfall_data" in sql_lower:
                data = self.mock_data["rainfall_data"].copy()
                
                # Simple filtering for rainfall data
                if "delhi" in sql_lower:
                    data = [row for row in data if "Delhi" in row["district"]]
                elif "hyderabad" in sql_lower:
                    data = [row for row in data if "Hyderabad" in row["district"]]
                    
                return data
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error executing mock SQL: {str(e)}")
            return []

    def generate_response(self, request: ChatRequest) -> dict:
        """
        This is the core logic for generating a chatbot response.
        Implements the full text-to-SQL-to-response flow using Sarvam AI.
        """
        logger.info(f"Generating response for session: {request.session_id}")
        
        try:
            # Step 1: Convert user query to SQL using Sarvam AI
            sql_messages = [
                {
                    "role": "system",
                    "content": "You are a SQL expert for Indian groundwater database. Convert natural language questions into valid PostgreSQL queries. Return ONLY the SQL query, nothing else."
                },
                {
                    "role": "user",
                    "content": f"""
                    Database Schema:
                    {self.database_schema}
                    
                    User Question: {request.query}
                    
                    Convert this to a valid PostgreSQL SQL query. Return only the SQL query.
                    """
                }
            ]
            
            logger.info("Step 1: Converting query to SQL using Sarvam AI...")
            sql_query = self.call_sarvam_ai(sql_messages)
            logger.info(f"Generated SQL: {sql_query}")
            
            # Step 2: Execute SQL on mock database
            logger.info("Step 2: Executing SQL on mock database...")
            raw_data = self.execute_mock_sql(sql_query)
            logger.info(f"Raw data results: {len(raw_data)} records")
            
            # Step 3: Convert results back to natural language using Sarvam AI
            if raw_data:
                nl_messages = [
                    {
                        "role": "system", 
                        "content": "You are a helpful groundwater expert for India. Explain technical data in simple terms that common people can understand. Focus on practical implications and actionable insights."
                    },
                    {
                        "role": "user",
                        "content": f"""
                        User asked: "{request.query}"
                        
                        Database query result:
                        {json.dumps(raw_data, indent=2)}
                        
                        Please explain this data in simple terms. What does it mean for the user? Include practical implications.
                        """
                    }
                ]
            else:
                nl_messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant for Indian groundwater database queries."
                    },
                    {
                        "role": "user",
                        "content": f"""
                        The user asked: "{request.query}"
                        No matching data was found in our database.
                        
                        Provide a helpful response explaining this and suggest what they might try instead.
                        """
                    }
                ]
            
            logger.info("Step 3: Converting results to natural language using Sarvam AI...")
            
            # Handle language preference
            if request.language and request.language != "en":
                nl_messages[0]["content"] += f" Respond in {request.language} language."
            
            response_text = self.call_sarvam_ai(nl_messages)
            
            # Step 4: Generate visualization data if appropriate
            visualization_data = None
            map_data = None
            
            if raw_data and ("chart" in request.query.lower() or "graph" in request.query.lower() or "show" in request.query.lower()):
                logger.info("Generating visualization data...")
                visualization_data = self.generate_chart_data(raw_data)
            
            if raw_data and ("map" in request.query.lower() or "location" in request.query.lower() or "area" in request.query.lower()):
                logger.info("Generating map data...")
                map_data = self.generate_map_data(raw_data)
            
            return {
                "response_text": response_text,
                "visualization_data": visualization_data,
                "map_data": map_data,
            }
            
        except Exception as e:
            logger.error(f"Error in generate_response: {str(e)}")
            return {
                "response_text": f"माफ़ करें, आपका अनुरोध प्रोसेस करते समय एक त्रुटि हुई। कृपया दोबारा कोशिश करें। (Sorry, I encountered an error processing your request. Please try again.)",
                "visualization_data": None,
                "map_data": None,
            }

    def generate_chart_data(self, data: list) -> dict:
        """
        Generate chart data from query results
        """
        if not data:
            return None
            
        # Simple chart generation based on data structure
        if "water_level" in data[0]:
            return {
                "type": "bar",
                "title": "Water Levels by District",
                "labels": [f"{row['district']}, {row['state']}" for row in data],
                "data": [row["water_level"] for row in data],
                "unit": "meters below ground",
                "colors": [
                    "#ff4444" if row["status"] == "Critical" 
                    else "#ffaa00" if row["status"] == "Semi-Critical"
                    else "#00aa44" for row in data
                ]
            }
        elif "rainfall_mm" in data[0]:
            return {
                "type": "bar", 
                "title": "Rainfall by District",
                "labels": [f"{row['district']}, {row['state']}" for row in data],
                "data": [row["rainfall_mm"] for row in data],
                "unit": "mm",
                "colors": ["#1f77b4" for _ in data]
            }
        return None

    def generate_map_data(self, data: list) -> dict:
        """
        Generate map data from query results
        """
        if not data:
            return None
            
        # Simple map data generation
        return {
            "type": "markers",
            "title": "Data Locations",
            "points": [
                {
                    "district": row["district"],
                    "state": row["state"], 
                    "value": row.get("water_level", row.get("rainfall_mm", 0)),
                    "status": row.get("status", "unknown"),
                    "label": f"{row['district']}: {row.get('water_level', row.get('rainfall_mm', 0))}"
                }
                for row in data
            ]
        }