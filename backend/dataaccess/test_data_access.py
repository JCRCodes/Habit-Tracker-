"""Test suite for HabitDatabase data access using a test database."""

# to run the test 'pytest test_data_access.py' in the terminal
# to run the test and see success messages, use 'pytest -s test_data_access.py'

import pytest
from dataaccess.data_access import HabitDatabase

# Test database connection string (update if your server/database name changes)
TEST_CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=LAPTOP-1K4FMAFS\\SQLEXPRESS;"
    "DATABASE=TestHabitTrackerDB;"
    "Trusted_Connection=yes;"
)

@pytest.fixture
def db():
    """Provides a HabitDatabase instance connected to the test database."""
    return HabitDatabase(TEST_CONNECTION_STRING)

def test_add_habit(db):
    """Test adding a habit to the database and verifying its existence."""
    result = db.add_habit(
        user_id=1,
        habit_name="Test Habit",
        description="Test Description",
        category="Test Category",
        frequency="Daily"
    )
    print("Add habit result:", result)
    assert result is True

    habits = db.get_user_habits(user_id=1)
    print("Habits:", habits)
    assert any(h[1] == "Test Habit" for h in habits) # assert means that we are checking if the habit exists in the list of habits
    print("✅ Habit added successfully and verified in test database.")
    
    
def test_get_user_habits(db):
    """Test retrieving user habits from the database."""
    habits = db.get_user_habits(user_id=1)
    print("Habits:", habits)
    assert isinstance(habits, list) # isinstance checks to ensure habits is a list 
    print("✅ User habits retrieved successfully from test database.")
    # the get_user_habits function is only looking for one parameter, user_id


def test_update_habit(db):
    """Test updating a habit in the database and verifying the update."""
    # First, add a habit to ensure it exists
    db.add_habit(
        user_id=1,
        habit_name="Original Habit",
        description="Original Description",
        category="Original Category",
        frequency="Daily"
    )
    # Get the most recently added habit's ID
    habits = db.get_user_habits(user_id=1)
    habit_id = habits[-1][0]

    # Update the habit
    result = db.update_habit(
        habit_id=habit_id,
        user_id=1,
        habit_name="Updated Habit",
        description="Updated Description",
        category="Updated Category",
        frequency="Weekly"
    )
    print("Update Habit Result:", result)
    assert result is True

    # Fetch habits after update and verify
    habits = db.get_user_habits(user_id=1)
    print("Updated Habits:", habits)
    assert any(h[0] == habit_id and h[1] == "Updated Habit" for h in habits)
    print("✅ Habit updated successfully and verified in test database.")

def test_delete_habit(db):
    """Test deleting a habit from the database and verifying its deletion."""
    # First, add a habit to ensure it exists
    db.add_habit(
        user_id=1,
        habit_name="Delete Me",
        description="To be deleted",
        category="Test",
        frequency="Daily"
    )
    # Get the most recently added habit's ID
    habits = db.get_user_habits(user_id=1)
    habit_id = habits[-1][0]

    # Delete the habit
    result = db.delete_habit(habit_id=habit_id)
    print("Delete Habit Result:", result)
    assert result is True

    # Verify the habit is deleted
    habits = db.get_user_habits(user_id=1)
    print("Habits after deletion:", habits)
    assert not any(h[0] == habit_id for h in habits)
    print("✅ Habit deleted successfully and verified in test database.")
    
def test_get_habit_by_category(db):
    """Test retrieving habits by category."""
    # First, add a habit to ensure it exists
    db.add_habit(
        user_id=1,
        habit_name="Category Test Habit",
        description="Testing category retrieval",
        category="Test Category",
        frequency="Daily"
    )
    
    # Retrieve habits by category
    habits = db.get_habits_by_category(user_id=1, category="Test Category")
    print("Habits by Category:", habits)
    
    assert isinstance(habits, list) # this asserts that habits is a list
    assert len(habits) > 0  # Ensure we got some habits back
    assert any(h[1] == "Category Test Habit" for h in habits) # assert that the habit exists in the list of habits
    print("✅ Habits retrieved by category successfully from test database.")
    
