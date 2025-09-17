#!/usr/bin/env python3
"""
Quick test script to verify streaming responses with status updates
"""
import asyncio
import json
from app.services import ChatService
from app.api.schemas import ChatRequest

async def test_streaming():
    """Test the streaming response functionality"""
    print("🚀 Testing streaming response with status updates...")
    
    service = ChatService()
    request = ChatRequest(query="Show me groundwater data for Karnataka")
    
    print("\n📡 Streaming response:")
    print("-" * 50)
    
    async for chunk in service.generate_streaming_response(request):
        # Check if it's a status message
        if chunk.startswith("data: {"):
            try:
                # Parse the JSON status message
                json_str = chunk.replace("data: ", "").replace("\n\n", "")
                status_data = json.loads(json_str)
                if status_data.get("type") == "status":
                    print(f"📍 STATUS: {status_data['message']}")
                else:
                    print(f"📊 DATA: {json_str}")
            except json.JSONDecodeError:
                print(f"📄 RAW: {chunk.strip()}")
        else:
            # This is the final response
            print(f"✅ FINAL RESPONSE:\n{chunk}")
    
    print("-" * 50)
    print("✨ Streaming test completed!")

if __name__ == "__main__":
    asyncio.run(test_streaming())