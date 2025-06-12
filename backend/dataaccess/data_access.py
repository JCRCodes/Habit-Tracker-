"""Data Access Layer for Habit Tracker Database"""


import pyodbc
from datetime import datetime
from typing import List, Tuple, Optional
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env

# Load the connection string from environment variables
connection_string = os.getenv("DB_CONNECTION_STRING")
print("Loaded connection string:", connection_string)  # For debugging

class HabitDatabase:
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
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Insert new habit
            cursor.execute("""
                INSERT INTO Habits (User_ID, Habit_Name_, Description_, Category, Frequency, CreatedAt)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, habit_name, description, category, frequency, datetime.now()))

            conn.commit()
            print(f"✅ Successfully added habit: {habit_name}")
            return True

        except pyodbc.Error as e:
            print(f"❌ Error adding habit: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
                
    def get_user_habits(self, user_id: int) -> List[Tuple[int, str, str, str, str, datetime]]:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT Habit_ID, Habit_Name_, Description_, Category, Frequency, CreatedAt FROM Habits WHERE User_ID = ?",
                (user_id,)
            )
            habits = cursor.fetchall()
            return [tuple(row) for row in habits]
        except Exception as e:
            print(f"❌ Error fetching habits: {e}")
            return []  # Always return a list
        finally:
            if 'conn' in locals():
                conn.close()

    def get_habit_by_id(self, habit_id: int) -> Optional[Tuple[int, str, str, str, str, datetime]]:
        """
        Get a specific habit by its ID

        Args:
            habit_id: ID of the habit to retrieve

        Returns:
            Optional[Tuple]: Habit details or None if not found
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT Habit_ID, Habit_Name_, Description_, Category, Frequency, CreatedAt 
                FROM Habits WHERE Habit_ID = ?
            """, (habit_id,))
            
            habit = cursor.fetchone()
            if habit:
                return tuple(habit) # Convert to tuple for consistency 
            else:
                print(f"❌ Habit with ID {habit_id} not found")
            
            return None
        
        except pyodbc.Error as e:
            print(f"❌ Error fetching habit: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()
                
    def update_habit(self, habit_id: int, user_id: int, habit_name: str, description: str, category: str, frequency: str) -> bool:
        """
        Update an existing habit

        Args:
            habit_id: ID of the habit to update
            user_id: ID of the user updating the habit
            habit_name: New name of the habit
            description: New description of the habit
            category: New category of the habit
            frequency: New frequency of the habit

        Returns:
            bool: True if successful, False if error
        """
        
        try:
            #first check if the habit exists
            existing_habit = self.get_habit_by_id(habit_id)
            if not existing_habit:
                print(f"❌ Habit with ID {habit_id} does not exist")
                return False#
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Build dynamic update query
            update_fields = []
            values = []
            
            if habit_name is not None:
                update_fields.append("Habit_Name_ = ?")
                values.append(habit_name)
            if description is not None:
                update_fields.append("Description_ = ?")
                values.append(description)
            if category is not None:
                update_fields.append("Category = ?")
                values.append(category)
            if frequency is not None:
                update_fields.append("Frequency = ?")
                values.append(frequency)
            
            if not update_fields:
                print("❌ No fields to update")
                return False
            
            # add habit ID to values for WHERE clause 
            values.append(habit_id)
            
            query = f"""
                UPDATE Habits 
                SET {', '.join(update_fields)} 
                WHERE Habit_ID = ?
            """
            cursor.execute(query, values)
            
            if cursor.rowcount > 0:
                conn.commit()
                print(f"✅ Successfully updated habit with ID {habit_id}")
                return True
            else:
                return False

        except pyodbc.Error as e:
            print(f"❌ Error updating habit: {e}")  
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

            
    def delete_habit(self, habit_id: int) -> bool:
        """
        
        Delete a habit by its ID


        Args:
            habit_id (int):the unique identifier of the habit to delete

        Returns:
            bool: returns true if the habit was successful and false if there was an error or if the habit does not exist 
        """
        try:
            
            # first check if the habit exists
            
            existing_habit = self.get_habit_by_id(habit_id)
            if not existing_habit:
                print(f"❌ Habit with ID {habit_id} does not exist")
                return False
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Delete the habit
            cursor.execute("DELETE FROM Habits WHERE Habit_ID = ?", (habit_id,))
            
            if cursor.rowcount > 0:
                conn.commit()
                print(f"✅ Successfully deleted habit with ID {habit_id}")
                return True 
            else:
                print(f"❌ Habit with ID {habit_id} not found")
                return False
            
        except pyodbc.Error as e:   
            print(f"❌ Error deleting habit: {e}")
            return False
        except Exception as e:  
            print(f"❌ Unexpected error: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
                
    def get_habits_by_category(self, user_id: int, category: str) -> List[Tuple[int, str, str, str, str, datetime]]:
        """
        Get all habits for a user filtered by category

        Args:
            user_id: ID of the user
            category: Category to filter habits by

        Returns:
            List of habits in the specified category
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT Habit_ID, Habit_Name_, Description_, Category, Frequency, CreatedAt 
                FROM Habits 
                WHERE User_ID = ? AND Category = ?
            """, (user_id, category))
            
            habits = cursor.fetchall()
            return [tuple(row) for row in habits]
        
        except pyodbc.Error as e:
            print(f"❌ Error fetching habits by category: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()  

# Instantiate the database object after the class definition
db = HabitDatabase(connection_string)



if __name__ == "__main__":
    # Try to fetch all habits for user_id=1
    habits = db.get_user_habits(user_id=1)
    print("Habits for user 1:", habits)