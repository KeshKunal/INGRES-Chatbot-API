import sys
import os
# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.llm_utils import get_json_from_query, get_english_from_data

# Test the NLU function
test_query = "What was the groundwater level in Chennai in 2022?"
print("\nTesting NLU function...")
result = get_json_from_query(test_query)
print(f"Query: {test_query}")
print(f"Structured JSON: {result}")

# Test the NLG function
test_data = {"location": "Chennai", "year": 2022, "groundwater_level": 8.2, "unit": "meters below ground"}
print("\nTesting NLG function...")
response = get_english_from_data(test_query, test_data)
print(f"Generated response: {response}")