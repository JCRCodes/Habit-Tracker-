# connecting sql server management studio to python 

from dotenv import load_dotenv
# Load environment variables from .env file

load_dotenv()

def get_db_connection_string():
    """
    Retrieves the database connection string from environment variables.
    
    Returns:
        str: The connection string for the database.
    """
    import os
    return os.getenv("DATABASE_CONNECTION_STRING", "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=HabitTrackerDB;Trusted_Connection=yes;")