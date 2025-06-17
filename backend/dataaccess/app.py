# This is the main application file for the Habit Tracker app.
import customtkinter as ctk
from customtkinter import CTkLabel, CTkButton, CTkToplevel, CTkProgressBar  # Import required widgets directly
import time
import threading 
from datetime import datetime
from data_access import HabitDatabase
import os
from dotenv import load_dotenv

# Load environment variables and connect to the database
load_dotenv()
connection_string = os.getenv("DB_CONNECTION_STRING")
if connection_string is None:
    raise ValueError("Database connection string must not be None. Check your .env file.")

# establishing the database to pull data from 
db = HabitDatabase(connection_string)

class HabitTrackerApp(ctk.CTk):
    """Main application class for the Habit Tracker."""
    
    def __init__(self):
        super().__init__()  # Initialize the parent class
        self.title("Habit Tracker")
        self.geometry("1000x700")
        self.resizable(True, True)
        self.label = ctk.CTkLabel(self, text="Welcome to Habit Tracker", font=("Roboto", 41, "bold"))
        self.label.pack(pady=60)


class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Loading...")
        self.geometry("800x600")
        self.resizable(False, False)
        self.configure(fg_color="#BC84AB")  # Set the background color of the splash screen
        
        def close_splash(self):
            self.destroy()
        self.close_splash = close_splash.__get__(self)
        
        # establishing frames for the loading assets to push them to the center of the screen
        
        center_frame = ctk.CTkFrame(self, width=800, height=500, corner_radius=10, fg_color="#BC84AB")
        center_frame.place(relx=0.5, rely=0.5, # relx and rely are used to center the frame
                            anchor="center") # anchor is used to center the frame

        # centered title
        label = ctk.CTkLabel(center_frame, text="Habit Tracker is loading...", font=("Roboto", 40, "bold"), text_color="#FFFFFF")
        label.pack(pady=20, padx=40)

        # centered progress bar
        self.progress = CTkProgressBar(center_frame, mode="indeterminate", width=300, fg_color="#FFFFFF", progress_color="#631F5D")
        self.progress.pack(pady=20, padx=40)
        self.progress.start()
        # After 5 seconds, close the splash screen and open the main app
        self.after(5000, self.start_main_app)

    def start_main_app(self):
        self.destroy()
        app = HabitTrackerApp()
        app.mainloop()
        
if __name__ == "__main__":
    splash = SplashScreen()
    splash.mainloop()

