# LangChain SQL Chatbot - Project Documentation

## 📋 Project Overview

This project implements an intelligent chatbot that allows users to interact with SQLite databases using natural language queries. The system leverages LangChain's SQL agent framework combined with Google's Gemini language model to provide intelligent query processing and human-like responses.

## 🏗️ Architecture

The chatbot follows a modular architecture with the following key components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│   Main App      │───▶│  Google Gemini  │
│ (Natural Lang.) │    │   (main.py)     │    │      LLM        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │ LangChain SQL   │───▶│   SQLite DB     │
                       │     Agent       │    │  (sample_db)    │
                       └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
langchain-sql-chatbot/
├── .kiro/specs/langchain-sql-chatbot/    # Project specifications
│   ├── requirements.md                   # Feature requirements
│   ├── design.md                        # System design document
│   └── tasks.md                         # Implementation tasks
├── src/                                 # Source code modules
│   ├── models/                          # Data models
│   │   └── data_models.py              # Core data structures
│   ├── config.py                       # Configuration management
│   └── __init__.py
├── tests/                              # Unit tests
│   └── test_data_models.py             # Data model tests
├── main.py                             # Main application entry point
├── create_sample_db.py                 # Database creation script
├── explore_db.py                       # Database exploration utility
├── requirements.txt                    # Python dependencies
├── .env                               # Environment variables
├── .env.example                       # Environment template
├── sample_database.db                 # Sample SQLite database
└── README.md                          # Basic project info
```

## 🔧 Components Implemented

### 1. Main Application (`main.py`)
**Purpose**: Primary entry point for the chatbot application

**Key Features**:
- Environment variable validation
- Google Gemini LLM initialization
- LangChain SQL agent setup
- Interactive chat loop
- Error handling and user guidance

**Dependencies**: 
- `langchain-google-genai` for Gemini integration
- `langchain-community` for SQL agent functionality
- `python-dotenv` for environment management

### 2. Data Models (`src/models/data_models.py`)
**Purpose**: Core data structures for the application

**Classes Implemented**:
- `ConversationEntry`: Represents chat interactions
- `ColumnInfo`: Database column metadata
- `TableInfo`: Database table information
- `DatabaseSchema`: Complete database schema
- `QueryResult`: SQL query execution results
- `ChatSession`: User session management
- `Relationship`: Foreign key relationships

**Features**:
- JSON serialization/deserialization
- Utility methods for data access
- Type safety with dataclasses

### 3. Configuration Management (`src/config.py`)
**Purpose**: Centralized configuration and environment variable handling

**Features**:
- Environment variable validation
- Configuration parameter access
- Database path validation
- Error handling for missing configurations

### 4. Sample Database (`create_sample_db.py`)
**Purpose**: Creates realistic test data for chatbot testing

**Database Schema**:
- **customers** (100 records): Customer information with contact details
- **products** (50 records): Product catalog with categories and pricing
- **orders** (200 records): Order history with status tracking
- **order_items** (618+ records): Individual order line items
- **employees** (20 records): Company employee data with hierarchy

**Relationships**:
- Orders → Customers (foreign key)
- Order Items → Orders & Products (foreign keys)
- Employees → Managers (self-referencing)

### 5. Database Explorer (`explore_db.py`)
**Purpose**: Utility to examine database structure and sample data

**Features**:
- Schema inspection
- Sample data display
- Example query suggestions
- Table relationship visualization

### 6. Unit Tests (`tests/test_data_models.py`)
**Purpose**: Comprehensive testing of data model functionality

**Test Coverage**:
- Serialization/deserialization
- Utility method functionality
- Edge case handling
- Data validation

## 🚀 Setup and Installation

### Prerequisites
- Python 3.8+
- Google API key for Gemini
- SQLite (included with Python)

### Installation Steps

1. **Clone/Download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create sample database**:
   ```bash
   python create_sample_db.py
   ```

4. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=your_actual_api_key_here
     ```

5. **Run the chatbot**:
   ```bash
   python main.py
   ```

## 💬 Usage Examples

### Basic Queries
```
🧑 You: How many customers do we have?
🤖 Assistant: We have 100 customers in our database.

🧑 You: What are the top 5 most expensive products?
🤖 Assistant: Here are the top 5 most expensive products:
1. Laptop Pro 15" - $1,299.99
2. Smartphone X - $799.99
3. Standing Desk - $399.99
...
```

### Complex Queries
```
🧑 You: Show me customers who have spent more than $3000
🤖 Assistant: Here are customers who have spent over $3000:
- Stephanie Moore: $3,249.60
- Richard Gonzalez: $3,778.64
- Richard Williams: $3,914.90
...

🧑 You: Which department has the highest average salary?
🤖 Assistant: The Management department has the highest average salary at $141,666.67
```

## 🔧 Configuration Options

The application supports various configuration parameters via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_API_KEY` | Required | Google API key for Gemini |
| `DATABASE_PATH` | `sample_database.db` | Path to SQLite database |
| `MAX_QUERY_TIMEOUT` | `30` | Query timeout in seconds |
| `MAX_RESULT_ROWS` | `1000` | Maximum rows to return |
| `ALLOW_DESTRUCTIVE_QUERIES` | `false` | Allow UPDATE/DELETE operations |
| `MAX_CONVERSATION_HISTORY` | `50` | Max conversation entries |
| `SESSION_TIMEOUT_MINUTES` | `60` | Session timeout |
| `ENABLE_QUERY_LOGGING` | `true` | Enable SQL query logging |
| `LOG_LEVEL` | `INFO` | Logging level |

## 🛡️ Security Features

### Query Safety
- **Read-only by default**: Only SELECT queries allowed unless configured otherwise
- **SQL injection prevention**: LangChain handles query sanitization
- **Query timeouts**: Prevents long-running queries
- **Result limits**: Caps the number of returned rows

### Configuration Security
- **Environment variables**: Sensitive data stored in .env files
- **API key masking**: Configuration display masks sensitive values
- **Path validation**: Database file existence and accessibility checks

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests.test_data_models -v
```

### Test Coverage
- ✅ Data model serialization/deserialization
- ✅ Configuration validation
- ✅ Utility method functionality
- ✅ Error handling scenarios
- ✅ Edge case handling

## 🔍 Database Schema Details

### Tables Overview
```sql
-- Customers table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    registration_date DATE,
    total_spent DECIMAL(10,2)
);

-- Products table  
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INTEGER,
    description TEXT,
    supplier TEXT,
    created_date DATE
);

-- Orders table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status TEXT DEFAULT 'pending',
    shipping_address TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

-- Order items table
CREATE TABLE order_items (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);

-- Employees table
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT,
    position TEXT,
    salary DECIMAL(10,2),
    hire_date DATE,
    manager_id INTEGER,
    FOREIGN KEY (manager_id) REFERENCES employees (employee_id)
);
```

## 🚨 Troubleshooting

### Common Issues

1. **Missing API Key**
   ```
   Error: GOOGLE_API_KEY not found in environment variables
   ```
   **Solution**: Add your Google API key to the `.env` file

2. **Database Not Found**
   ```
   Error: Database file 'sample_database.db' not found
   ```
   **Solution**: Run `python create_sample_db.py` to create the sample database

3. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'langchain'
   ```
   **Solution**: Install dependencies with `pip install -r requirements.txt`

4. **API Rate Limits**
   ```
   Error: API quota exceeded
   ```
   **Solution**: Wait for quota reset or upgrade your Google API plan

### Debug Mode
To enable verbose logging, set the environment variable:
```bash
LOG_LEVEL=DEBUG
```

## 🔮 Future Enhancements

The current implementation provides a solid foundation. Potential future improvements include:

1. **Web Interface**: Streamlit or Flask web UI
2. **Multiple Database Support**: PostgreSQL, MySQL support
3. **Query History**: Persistent conversation storage
4. **Advanced Analytics**: Query performance metrics
5. **User Authentication**: Multi-user support
6. **Query Caching**: Performance optimization
7. **Export Features**: CSV/Excel result export
8. **Visualization**: Chart generation from query results

## 📝 Development Notes

### Design Decisions
- **LangChain Integration**: Chosen for robust SQL agent capabilities
- **Google Gemini**: Selected for superior natural language understanding
- **SQLite**: Lightweight, file-based database for easy setup
- **Modular Architecture**: Enables easy testing and future extensions

### Performance Considerations
- Query timeouts prevent system overload
- Result row limits manage memory usage
- Connection pooling for database efficiency
- Lazy loading of large datasets

## 📄 License & Credits

This project demonstrates the integration of:
- **LangChain**: Framework for LLM applications
- **Google Gemini**: Advanced language model
- **SQLite**: Embedded database engine

Built as a proof-of-concept for natural language database interaction using modern AI technologies.