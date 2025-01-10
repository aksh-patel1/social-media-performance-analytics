from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import httpx
import json
from datetime import datetime
import logging
from fastapi.middleware.cors import CORSMiddleware
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Langflow Chat API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
LANGFLOW_BASE_URL = "http://127.0.0.1:7860"
DEFAULT_FLOW_ID = "2e80e619-11e1-4576-a3c0-6ceb1c62f9c6"

# Pydantic models for request/response validation
class ChatMessage(BaseModel):
    message: str
    flow_id: Optional[str] = None
    tweaks: Optional[Dict[str, Any]] = None
    api_key: Optional[str] = None

class Source(BaseModel):
    id: str
    display_name: str
    source: str

class MessageProperties(BaseModel):
    text_color: str = ""
    background_color: str = ""
    edited: bool = False
    source: Optional[Source] = None
    icon: str = ""
    allow_markdown: bool = False
    state: str = "complete"
    targets: List[str] = []

class ChatResponse(BaseModel):
    timestamp: datetime
    sender: str
    sender_name: str
    session_id: str
    text: str
    files: List[str] = []
    error: bool = False
    edit: bool = False
    properties: MessageProperties
    category: str = "message"
    content_blocks: List[Any] = []
    flow_id: str

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None

async def call_langflow_api(message: str, flow_id: str, tweaks: Optional[dict] = None, api_key: Optional[str] = None) -> dict:
    """Make API call to Langflow"""
    api_url = f"{LANGFLOW_BASE_URL}/api/v1/run/{flow_id}"
    
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat"
    }
    
    if tweaks:
        payload["tweaks"] = tweaks
        
    headers = {}
    if api_key:
        headers["x-api-key"] = api_key
    
    logger.info(f"Calling Langflow API at {api_url}")
    logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Status Error: {e.response.status_code} - {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Langflow API error: {e.response.text}"
            )
        except httpx.RequestError as e:
            logger.error(f"Request Error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error connecting to Langflow: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """
    Handle chat messages and interact with Langflow
    """
    try:
        logger.info(f"Received chat message: {chat_message.message}")
        
        flow_id = chat_message.flow_id or DEFAULT_FLOW_ID
        response = await call_langflow_api(
            message=chat_message.message,
            flow_id=flow_id,
            tweaks=chat_message.tweaks,
            api_key=chat_message.api_key
        )
        
        logger.debug(f"Langflow response: {json.dumps(response, indent=2)}")
        
        # Extract the relevant message data from Langflow response
        try:
            outputs = response.get("outputs", [])
            if not outputs:
                raise ValueError("No outputs in Langflow response")
                
            message_data = outputs[0]["outputs"][0]["results"]["message"]["data"]
            
            return ChatResponse(
                timestamp=datetime.fromisoformat(message_data["timestamp"].replace('Z', '+00:00')),
                sender=message_data["sender"],
                sender_name=message_data["sender_name"],
                session_id=message_data["session_id"],
                text=message_data["text"],
                files=message_data["files"],
                error=message_data["error"],
                edit=message_data["edit"],
                properties=MessageProperties(**message_data["properties"]),
                category=message_data["category"],
                content_blocks=message_data["content_blocks"],
                flow_id=message_data["flow_id"]
            )
        except (KeyError, IndexError, ValueError) as e:
            logger.error(f"Error parsing Langflow response: {str(e)}")
            logger.error(f"Response structure: {json.dumps(response, indent=2)}")
            raise HTTPException(
                status_code=500,
                detail=f"Invalid response structure from Langflow: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Try to connect to Langflow
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{LANGFLOW_BASE_URL}/health")
            langflow_status = "up" if response.status_code == 200 else "down"
    except Exception:
        langflow_status = "down"
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "langflow_status": langflow_status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)