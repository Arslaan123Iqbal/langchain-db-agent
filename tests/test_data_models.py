"""Unit tests for data models."""

import unittest
import json
from datetime import datetime
from src.models.data_models import (
    ConversationEntry, ColumnInfo, TableInfo, Relationship,
    DatabaseSchema, QueryResult, ChatSession
)


class TestDataModels(unittest.TestCase):
    """Test cases for data model classes."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_timestamp = datetime(2024, 1, 15, 10, 30, 0)
        
        self.sample_conversation_entry = ConversationEntry(
            timestamp=self.sample_timestamp,
            user_query="How many customers do we have?",
            sql_generated="SELECT COUNT(*) FROM customers",
            results=[{"count": 100}],
            formatted_response="We have 100 customers in total.",
            execution_time=0.25
        )
        
        self.sample_column_info = ColumnInfo(
            name="customer_id",
            type="INTEGER",
            nullable=False,
            primary_key=True,
            default_value=None
        )
        
        self.sample_table_info = TableInfo(
            name="customers",
            columns=[self.sample_column_info],
            row_count=100
        )
    
    def test_conversation_entry_serialization(self):
        """Test ConversationEntry serialization and deserialization."""
        # Test to_dict
        entry_dict = self.sample_conversation_entry.to_dict()
        self.assertEqual(entry_dict['user_query'], "How many customers do we have?")
        self.assertEqual(entry_dict['timestamp'], self.sample_timestamp.isoformat())
        
        # Test from_dict
        restored_entry = ConversationEntry.from_dict(entry_dict)
        self.assertEqual(restored_entry.user_query, self.sample_conversation_entry.user_query)
        self.assertEqual(restored_entry.timestamp, self.sample_conversation_entry.timestamp)
        self.assertEqual(restored_entry.execution_time, 0.25)
    
    def test_column_info_serialization(self):
        """Test ColumnInfo serialization and deserialization."""
        # Test to_dict
        column_dict = self.sample_column_info.to_dict()
        self.assertEqual(column_dict['name'], "customer_id")
        self.assertEqual(column_dict['type'], "INTEGER")
        self.assertTrue(column_dict['primary_key'])
        
        # Test from_dict
        restored_column = ColumnInfo.from_dict(column_dict)
        self.assertEqual(restored_column.name, "customer_id")
        self.assertEqual(restored_column.type, "INTEGER")
        self.assertTrue(restored_column.primary_key)
    
    def test_table_info_methods(self):
        """Test TableInfo utility methods."""
        # Add more columns for testing
        columns = [
            ColumnInfo("customer_id", "INTEGER", False, True),
            ColumnInfo("name", "TEXT", False, False),
            ColumnInfo("email", "TEXT", True, False)
        ]
        table = TableInfo("customers", columns, 100)
        
        # Test get_column_names
        column_names = table.get_column_names()
        self.assertEqual(column_names, ["customer_id", "name", "email"])
        
        # Test get_primary_keys
        primary_keys = table.get_primary_keys()
        self.assertEqual(primary_keys, ["customer_id"])
    
    def test_database_schema_methods(self):
        """Test DatabaseSchema utility methods."""
        # Create sample schema
        table1 = TableInfo("customers", [self.sample_column_info], 100)
        table2 = TableInfo("orders", [ColumnInfo("order_id", "INTEGER", False, True)], 50)
        relationship = Relationship("orders", "customer_id", "customers", "customer_id")
        
        schema = DatabaseSchema([table1, table2], [relationship])
        
        # Test get_table_names
        table_names = schema.get_table_names()
        self.assertEqual(set(table_names), {"customers", "orders"})
        
        # Test get_table_by_name
        found_table = schema.get_table_by_name("customers")
        self.assertIsNotNone(found_table)
        self.assertEqual(found_table.name, "customers")
        
        # Test case insensitive search
        found_table_upper = schema.get_table_by_name("CUSTOMERS")
        self.assertIsNotNone(found_table_upper)
        
        # Test non-existent table
        not_found = schema.get_table_by_name("nonexistent")
        self.assertIsNone(not_found)
    
    def test_database_schema_json_serialization(self):
        """Test DatabaseSchema JSON serialization."""
        table = TableInfo("test_table", [self.sample_column_info], 10)
        relationship = Relationship("table1", "col1", "table2", "col2")
        schema = DatabaseSchema([table], [relationship])
        
        # Test to_json
        json_str = schema.to_json()
        self.assertIsInstance(json_str, str)
        
        # Test from_json
        restored_schema = DatabaseSchema.from_json(json_str)
        self.assertEqual(len(restored_schema.tables), 1)
        self.assertEqual(len(restored_schema.relationships), 1)
        self.assertEqual(restored_schema.tables[0].name, "test_table")
    
    def test_query_result_methods(self):
        """Test QueryResult utility methods."""
        # Test successful query result
        success_result = QueryResult(
            success=True,
            data=[{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}],
            error_message=None,
            execution_time=0.1,
            rows_affected=2,
            sql_query="SELECT * FROM users"
        )
        
        self.assertFalse(success_result.is_empty())
        self.assertEqual(success_result.get_column_names(), ["id", "name"])
        
        # Test empty query result
        empty_result = QueryResult(
            success=True,
            data=[],
            error_message=None,
            execution_time=0.05,
            rows_affected=0,
            sql_query="SELECT * FROM empty_table"
        )
        
        self.assertTrue(empty_result.is_empty())
        self.assertEqual(empty_result.get_column_names(), [])
        
        # Test failed query result
        failed_result = QueryResult(
            success=False,
            data=[],
            error_message="Table not found",
            execution_time=0.01,
            rows_affected=0,
            sql_query="SELECT * FROM nonexistent"
        )
        
        self.assertFalse(failed_result.success)
        self.assertEqual(failed_result.error_message, "Table not found")
    
    def test_chat_session_methods(self):
        """Test ChatSession utility methods."""
        session = ChatSession(
            session_id="test_session_123",
            created_at=self.sample_timestamp,
            conversation_history=[],
            database_path="/path/to/db.sqlite"
        )
        
        # Test initial state
        self.assertEqual(session.get_total_queries(), 0)
        self.assertEqual(len(session.get_recent_context()), 0)
        
        # Test adding conversation entries
        session.add_conversation_entry(self.sample_conversation_entry)
        self.assertEqual(session.get_total_queries(), 1)
        
        # Add more entries
        for i in range(5):
            entry = ConversationEntry(
                timestamp=self.sample_timestamp,
                user_query=f"Query {i}",
                sql_generated=f"SELECT {i}",
                results=[],
                formatted_response=f"Response {i}",
                execution_time=0.1
            )
            session.add_conversation_entry(entry)
        
        # Test recent context limit
        recent_context = session.get_recent_context(3)
        self.assertEqual(len(recent_context), 3)
        self.assertEqual(recent_context[-1].user_query, "Query 4")
        
        # Test clear history
        session.clear_history()
        self.assertEqual(session.get_total_queries(), 0)
    
    def test_chat_session_json_serialization(self):
        """Test ChatSession JSON serialization."""
        session = ChatSession(
            session_id="test_session",
            created_at=self.sample_timestamp,
            conversation_history=[self.sample_conversation_entry],
            database_path="/test/path"
        )
        
        # Test to_json
        json_str = session.to_json()
        self.assertIsInstance(json_str, str)
        
        # Test from_json
        restored_session = ChatSession.from_json(json_str)
        self.assertEqual(restored_session.session_id, "test_session")
        self.assertEqual(len(restored_session.conversation_history), 1)
        self.assertEqual(restored_session.database_path, "/test/path")
        self.assertEqual(
            restored_session.conversation_history[0].user_query,
            "How many customers do we have?"
        )


if __name__ == '__main__':
    unittest.main()