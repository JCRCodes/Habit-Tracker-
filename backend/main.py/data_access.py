# data_access.py - data access layer for Habit Tracker application

import pyodbc
from datetime import datetime
from typing import List, Tuple, Optional

class Habit_Database:
    def __init__(self, connection_string: str):
        """Initialize the database connection"""
        self.connection_string = connection_string
    
    def _get_connection(self):
        """Private method to get database connection"""
        return pyodbc.connect(self.connection_string)
    
# === HABIT MANAGEMENT FUNCTIONS ===

def add_habit(self, user_id: int, habit_name: str, description: str, category: str, frequency: str) -> bool:
    """
        Add a new habit to the database
        
        Args:
            user_id: ID of the user creating the habit
            habit_name: Name of the habit
            description: Description of what the habit involves
            category: Category (e.g., 'Health', 'Productivity', 'Personal')
            frequency: How often ('Daily', 'Weekly', 'Monthly')
        
        Returns:
            bool: True if successful, False if error
        """