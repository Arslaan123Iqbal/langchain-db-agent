"""Data models for the LangChain SQL Chatbot."""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Optional, Any
import json


@dataclass
class ConversationEntry:
    """Represents a single conversation entry between user and chatbot."""
    
    timestamp: datetime
    user_query: str
    sql_generated: str
    results: List[Dict[str, Any]]
    formatted_response: str
    execution_time: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'user_query': self.user_query,
            'sql_generated': self.sql_generated,
            'results': self.results,
            'formatted_response': self.formatted_response,
            'execution_time': self.execution_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationEntry':
        """Create instance from dictionary."""
        return cls(
            timestamp=datetime.fromisoformat(data['timestamp']),
            user_query=data['user_query'],
            sql_generated=data['sql_generated'],
            results=data['results'],
            formatted_response=data['formatted_response'],
            execution_time=data['execution_time']
        )


@dataclass
class ColumnInfo:
    """Information about a database column."""
    
    name: str
    type: str
    nullable: bool
    primary_key: bool
    default_value: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ColumnInfo':
        """Create instance from dictionary."""
        return cls(**data)


@dataclass
class TableInfo:
    """Information about a database table."""
    
    name: str
    columns: List[ColumnInfo]
    row_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'name': self.name,
            'columns': [col.to_dict() for col in self.columns],
            'row_count': self.row_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TableInfo':
        """Create instance from dictionary."""
        return cls(
            name=data['name'],
            columns=[ColumnInfo.from_dict(col) for col in data['columns']],
            row_count=data['row_count']
        )
    
    def get_column_names(self) -> List[str]:
        """Get list of column names."""
        return [col.name for col in self.columns]
    
    def get_primary_keys(self) -> List[str]:
        """Get list of primary key column names."""
        return [col.name for col in self.columns if col.primary_key]


@dataclass
class Relationship:
    """Represents a foreign key relationship between tables."""
    
    from_table: str
    from_column: str
    to_table: str
    to_column: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Relationship':
        """Create instance from dictionary."""
        return cls(**data)


@dataclass
class DatabaseSchema:
    """Complete database schema information."""
    
    tables: List[TableInfo]
    relationships: List[Relationship]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'tables': [table.to_dict() for table in self.tables],
            'relationships': [rel.to_dict() for rel in self.relationships]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DatabaseSchema':
        """Create instance from dictionary."""
        return cls(
            tables=[TableInfo.from_dict(table) for table in data['tables']],
            relationships=[Relationship.from_dict(rel) for rel in data['relationships']]
        )
    
    def get_table_names(self) -> List[str]:
        """Get list of all table names."""
        return [table.name for table in self.tables]
    
    def get_table_by_name(self, name: str) -> Optional[TableInfo]:
        """Get table information by name."""
        for table in self.tables:
            if table.name.lower() == name.lower():
                return table
        return None
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'DatabaseSchema':
        """Create instance from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)


@dataclass
class QueryResult:
    """Result of executing a SQL query."""
    
    success: bool
    data: List[Dict[str, Any]]
    error_message: Optional[str]
    execution_time: float
    rows_affected: int
    sql_query: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QueryResult':
        """Create instance from dictionary."""
        return cls(**data)
    
    def is_empty(self) -> bool:
        """Check if query returned no data."""
        return len(self.data) == 0
    
    def get_column_names(self) -> List[str]:
        """Get column names from the first row of data."""
        if self.data:
            return list(self.data[0].keys())
        return []


@dataclass
class ChatSession:
    """Represents a chat session with conversation history."""
    
    session_id: str
    created_at: datetime
    conversation_history: List[ConversationEntry]
    database_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'session_id': self.session_id,
            'created_at': self.created_at.isoformat(),
            'conversation_history': [entry.to_dict() for entry in self.conversation_history],
            'database_path': self.database_path
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatSession':
        """Create instance from dictionary."""
        return cls(
            session_id=data['session_id'],
            created_at=datetime.fromisoformat(data['created_at']),
            conversation_history=[ConversationEntry.from_dict(entry) for entry in data['conversation_history']],
            database_path=data.get('database_path')
        )
    
    def add_conversation_entry(self, entry: ConversationEntry) -> None:
        """Add a new conversation entry."""
        self.conversation_history.append(entry)
    
    def get_recent_context(self, limit: int = 5) -> List[ConversationEntry]:
        """Get recent conversation entries for context."""
        return self.conversation_history[-limit:] if self.conversation_history else []
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history.clear()
    
    def get_total_queries(self) -> int:
        """Get total number of queries in this session."""
        return len(self.conversation_history)
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ChatSession':
        """Create instance from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)