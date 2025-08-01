"""Script to explore the sample database structure and data."""

import sqlite3

def explore_database():
    """Display database structure and sample data."""
    
    conn = sqlite3.connect('sample_database.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("=== DATABASE STRUCTURE ===\n")
    
    for table in tables:
        table_name = table[0]
        print(f"📊 TABLE: {table_name.upper()}")
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print("   Columns:")
        for col in columns:
            col_name, col_type, not_null, default, pk = col[1], col[2], col[3], col[4], col[5]
            pk_indicator = " (PRIMARY KEY)" if pk else ""
            print(f"   - {col_name}: {col_type}{pk_indicator}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   Records: {count}")
        
        # Show sample data
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        sample_data = cursor.fetchall()
        
        if sample_data:
            print("   Sample data:")
            for i, row in enumerate(sample_data, 1):
                print(f"   {i}. {row}")
        
        print()
    
    print("=== EXAMPLE QUERIES YOU CAN ASK THE CHATBOT ===\n")
    
    example_queries = [
        "How many customers do we have?",
        "What are our top 5 best-selling products?",
        "Show me all orders from this month",
        "Which customers have spent the most money?",
        "What's the average order value?",
        "How many employees work in each department?",
        "Show me all products in the Electronics category",
        "Which orders are still pending?",
        "What's our total revenue this year?",
        "Show me customer information for orders over $500"
    ]
    
    for i, query in enumerate(example_queries, 1):
        print(f"{i:2d}. {query}")
    
    conn.close()

if __name__ == "__main__":
    explore_database()