"""FastAPI LangChain SQL Chatbot Application"""

import os
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents.agent_types import AgentType

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="LangChain SQL Chatbot API",
    description="Natural language interface to SQLite database using Google Gemini",
    version="1.0.0"
)

# Global variables for agent
agent_executor = None
db_connection = None

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    prompt: str

class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    execution_time: float
    sql_query: str = None
    success: bool = True
    error: str = None

def initialize_agent():
    """Initialize the SQL agent with Gemini LLM."""
    global agent_executor, db_connection
    
    # Check for API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    # Database path
    db_path = os.getenv('DATABASE_PATH', 'sample_database.db')
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file '{db_path}' not found")
    
    try:
        # Initialize Gemini LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=api_key,
            temperature=0
        )
        
        # Create database connection
        db_connection = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        
        # Create SQL agent
        agent_executor = create_sql_agent(
            llm=llm,
            db=db_connection,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )
        
        return True
    except Exception as e:
        raise RuntimeError(f"Failed to initialize agent: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Initialize the agent when the app starts."""
    try:
        initialize_agent()
        print("✅ SQL Agent initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {str(e)}")
        print("The API will not work properly without proper initialization.")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "LangChain SQL Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "/chat": "POST - Send natural language queries to the database",
            "/health": "GET - Check API health status",
            "/schema": "GET - Get database schema information"
        },
        "example_queries": [
            "How many customers do we have?",
            "What are the top 5 products by price?",
            "Show me orders from this month",
            "Which department has the most employees?"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if agent_executor is None:
        return {"status": "unhealthy", "message": "Agent not initialized"}
    
    return {
        "status": "healthy",
        "message": "SQL Agent is ready",
        "database_connected": db_connection is not None
    }

@app.get("/schema")
async def get_schema():
    """Get database schema information."""
    if db_connection is None:
        raise HTTPException(status_code=500, detail="Database not connected")
    
    try:
        # Get table information
        tables_info = db_connection.get_table_info()
        table_names = db_connection.get_usable_table_names()
        
        return {
            "tables": table_names,
            "schema_info": tables_info,
            "total_tables": len(table_names)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get schema: {str(e)}")


@app.post("/chat")
async def chat_simple(request: ChatRequest):
    """Simplified chat endpoint that returns just the response text."""
    
    if agent_executor is None:
        raise HTTPException(
            status_code=500, 
            detail="Agent not initialized. Check API key and database connection."
        )
    
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    try:
        response = agent_executor.run(request.prompt)
        return {"response": response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)