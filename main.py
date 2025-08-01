"""Simple LangChain SQL Chatbot - Main Application"""

import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents.agent_types import AgentType

def main():
    """Main application entry point."""
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please create a .env file with your Google API key:")
        print("GOOGLE_API_KEY=your_api_key_here")
        return
    
    # Database path
    db_path = os.getenv('DATABASE_PATH', 'sample_database.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Error: Database file '{db_path}' not found.")
        print("Please run 'python create_sample_db.py' to create sample data.")
        return
    
    print("🤖 LangChain SQL Chatbot")
    print("=" * 50)
    print(f"📊 Connected to database: {db_path}")
    
    try:
        # Initialize Gemini LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=api_key,
            temperature=0
        )
        
        # Create database connection
        db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        
        # Create SQL agent
        agent_executor = create_sql_agent(
            llm=llm,
            db=db,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )
        
        print("✅ Chatbot initialized successfully!")
        print("\n💡 Example questions you can ask:")
        print("- How many customers do we have?")
        print("- What are the top 5 products by price?")
        print("- Show me orders from this month")
        print("- Which department has the most employees?")
        print("\nType 'quit' or 'exit' to stop.\n")
        
        # Chat loop
        while True:
            try:
                user_input = input("🧑 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                print("🤖 Assistant: ", end="")
                
                # Get response from agent
                start_time = datetime.now()
                response = agent_executor.run(user_input)
                end_time = datetime.now()
                
                execution_time = (end_time - start_time).total_seconds()
                
                print(f"{response}")
                print(f"⏱️  Executed in {execution_time:.2f} seconds\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                print("Please try rephrasing your question.\n")
    
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {str(e)}")
        print("Please check your API key and database connection.")

if __name__ == "__main__":
    main()