"""Configuration management for the LangChain SQL Chatbot."""

import os
from typing import Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv


class ConfigurationError(Exception):
    """Custom exception for configuration-related errors."""
    pass


class ConfigurationManager:
    """Manages configuration settings and environment variables."""
    
    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration manager and load environment variables.
        
        Args:
            env_file: Optional path to .env file. If None, uses default .env
        """
        self._load_environment(env_file)
        self._validate_required_config()
    
    def _load_environment(self, env_file: Optional[str] = None) -> None:
        """Load environment variables from .env file."""
        if env_file:
            env_path = Path(env_file)
            if not env_path.exists():
                raise ConfigurationError(f"Environment file not found: {env_file}")
            load_dotenv(env_path)
        else:
            load_dotenv()  # Load from default .env file
    
    def _validate_required_config(self) -> None:
        """Validate that required configuration parameters are present."""
        required_vars = ['GOOGLE_API_KEY']
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ConfigurationError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                "Please create a .env file with these variables. "
                "See .env.example for reference."
            )
    
    def validate_database_path(self, path: str) -> bool:
        """Validate that a database path exists and is accessible.
        
        Args:
            path: Path to the database file
            
        Returns:
            True if valid, False otherwise
        """
        try:
            db_path = Path(path)
            if not db_path.exists():
                return False
            if not db_path.is_file():
                return False
            # Try to access the file
            with open(db_path, 'rb') as f:
                f.read(1)
            return True
        except (OSError, IOError, PermissionError):
            return False
    
    @property
    def google_api_key(self) -> str:
        """Get Google API key for Gemini."""
        return os.getenv('GOOGLE_API_KEY', '')
    
    @property
    def database_path(self) -> Optional[str]:
        """Get default database path."""
        return os.getenv('DATABASE_PATH')
    
    @property
    def max_query_timeout(self) -> int:
        """Get maximum query timeout in seconds."""
        try:
            return int(os.getenv('MAX_QUERY_TIMEOUT', '30'))
        except ValueError:
            return 30
    
    @property
    def max_conversation_history(self) -> int:
        """Get maximum conversation history entries to keep."""
        try:
            return int(os.getenv('MAX_CONVERSATION_HISTORY', '50'))
        except ValueError:
            return 50
    
    @property
    def enable_query_logging(self) -> bool:
        """Get whether to enable query logging."""
        return os.getenv('ENABLE_QUERY_LOGGING', 'false').lower() == 'true'
    
    @property
    def log_level(self) -> str:
        """Get logging level."""
        return os.getenv('LOG_LEVEL', 'INFO').upper()
    
    @property
    def session_timeout_minutes(self) -> int:
        """Get session timeout in minutes."""
        try:
            return int(os.getenv('SESSION_TIMEOUT_MINUTES', '60'))
        except ValueError:
            return 60
    
    @property
    def max_result_rows(self) -> int:
        """Get maximum number of rows to return from queries."""
        try:
            return int(os.getenv('MAX_RESULT_ROWS', '1000'))
        except ValueError:
            return 1000
    
    @property
    def allow_destructive_queries(self) -> bool:
        """Get whether to allow destructive queries (UPDATE, DELETE, etc.)."""
        return os.getenv('ALLOW_DESTRUCTIVE_QUERIES', 'false').lower() == 'true'
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration values as a dictionary."""
        return {
            'google_api_key': '***' if self.google_api_key else None,  # Mask sensitive data
            'database_path': self.database_path,
            'max_query_timeout': self.max_query_timeout,
            'max_conversation_history': self.max_conversation_history,
            'enable_query_logging': self.enable_query_logging,
            'log_level': self.log_level,
            'session_timeout_minutes': self.session_timeout_minutes,
            'max_result_rows': self.max_result_rows,
            'allow_destructive_queries': self.allow_destructive_queries
        }
    
    def validate_all_config(self) -> Dict[str, bool]:
        """Validate all configuration parameters.
        
        Returns:
            Dictionary with validation results for each parameter
        """
        validation_results = {}
        
        # Validate Google API key
        validation_results['google_api_key'] = bool(self.google_api_key)
        
        # Validate database path if provided
        if self.database_path:
            validation_results['database_path'] = self.validate_database_path(self.database_path)
        else:
            validation_results['database_path'] = True  # Optional parameter
        
        # Validate numeric parameters
        validation_results['max_query_timeout'] = self.max_query_timeout > 0
        validation_results['max_conversation_history'] = self.max_conversation_history > 0
        validation_results['session_timeout_minutes'] = self.session_timeout_minutes > 0
        validation_results['max_result_rows'] = self.max_result_rows > 0
        
        # Validate log level
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        validation_results['log_level'] = self.log_level in valid_log_levels
        
        return validation_results