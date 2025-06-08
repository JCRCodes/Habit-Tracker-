# test_connection.py - Run this to test your database connection

## testing driver available 

import pyodbc
print("Available ODBC drivers:")
for driver in pyodbc.drivers():
    if 'SQL Server' in driver:
        print(f"  - {driver}")
        
        
import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    try:
        # Get connection details from environment variables
        server = os.getenv('DB_SERVER', 'LAPTOP-1K4FMAFS\SQLEXPRESS')
        database = os.getenv('DB_NAME', 'HabitTrackerDB')
        username = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        
        print(f"Attempting to connect to:")
        print(f"Server: {server}")
        print(f"Database: {database}")
        print(f"Username: {username}")
        print("-" * 40)
        
        # Build connection string
        # Option 1: SQL Server Authentication
        if username and password:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        else:
            # Option 2: Windows Authentication
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
        
        print("Connecting to database...")
        
        # Establish connection
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Test query
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()
        print("✅ Connection successful!")
        print(f"SQL Server Version: {version[0][:50]}...")
        
# Test our tables
        cursor.execute("SELECT COUNT(*) FROM Habits")
        habit_count = cursor.fetchone()[0]
        print(f"✅ Found {habit_count} habits in database")
        
        # Check what columns exist in the Habits table
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'Habits'
            ORDER BY ORDINAL_POSITION
        """)
        columns = cursor.fetchall()
        print("\n📋 Columns in Habits table:")
        for column in columns:
            print(f"  - {column[0]} ({column[1]})")

        # Show sample data using the correct column names
        if columns:
            # Use the first few columns for the sample query
            col_names = [col[0] for col in columns[:3]]
            col_list = ', '.join(col_names)
            cursor.execute(f"SELECT TOP 3 {col_list} FROM Habits")
            habits = cursor.fetchall()
            print(f"\n📋 Sample data from first {len(col_names)} columns:")
            for habit in habits:
                print(f"  - {habit}")
        
        # Close connection
        cursor.close()
        connection.close()
        print("\n🎉 Database connection test completed successfully!")
        
    except pyodbc.Error as e:
        print("❌ Database connection failed!")
        print(f"Error: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your .env file has correct credentials")
        print("2. Ensure SQL Server is running")
        print("3. Verify ODBC Driver 17 for SQL Server is installed")
        print("4. Check if SQL Server allows remote connections")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_connection()