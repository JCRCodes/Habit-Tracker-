"""Main application file for the Habit Tracker app."""

import os
import time
from datetime import datetime
import threading
from dotenv import load_dotenv
import customtkinter as ctk
from data_access import HabitDatabase

# Load environment variables and connect to the database
load_dotenv()
connection_string = os.getenv("DB_CONNECTION_STRING")
if connection_string is None:
    raise ValueError("Database connection string must not be None. Check your .env file.")

db = HabitDatabase(connection_string)

# Define MainScreen class to manage the main application window
class MainScreen(ctk.CTkFrame):
    """Main screen for the Habit Tracker application."""

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(fg_color="#F1B5C9")  # Set background color
        
        # Create an overlay frame for additional content
        self.overlay_frame = ctk.CTkFrame(self, fg_color="#FFFFFF") # Set overlay color with transparency
        self.overlay_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create a label for the main screen
        self.label = ctk.CTkLabel(
            self.overlay_frame,
            text="Welcome to the Habit Tracker",
            font=("Roboto", 28, "bold"),
            text_color="#89495D",
        )
        self.label.pack(pady=20, padx=20)

    # Heading for the main screen
        self.heading = ctk.CTkLabel(
            self.overlay_frame,
            text="What would you like to do today?",
            font=("Roboto", 18, "bold"),
            text_color="#89495D",
            justify="center",
        )
        self.heading.pack(pady=20, padx=40)
        
        
        # Add Habit Input Button
        input_frame = ctk.CTkFrame(self.overlay_frame, fg_color="#FFFFFF")
        input_frame.pack(pady=10)
        
        input_frame.heading = ctk.CTkLabel(
            input_frame,
            text="Add a New Habit",
            font=("Roboto", 16, "bold"),
            text_color="#89495D",
        )
        input_frame.heading.pack(pady=(10, 5))

        self.habit_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter Habit Name",
            width=200,
            fg_color="#FCEBF0",
            text_color="#89495D",
            border_color="#FCEBF0",
            corner_radius=10,
        )
        self.habit_entry.pack(side="left", padx=10, pady=10)
        
        self.description_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter description",
            width=200,
            fg_color="#FCEBF0",
            text_color="#89495D",
            border_color="#FCEBF0",
            corner_radius=10,
        )
        
        self.description_entry.pack(side="left", padx=10, pady=10)
        
        
        self_category_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter a category",
            width=200,
            fg_color="#FCEBF0",
            text_color="#89495D",
            border_color="#FCEBF0",
            corner_radius=10,
        )
        
        self_category_entry.pack(side="left", padx=10, pady=10)
        
        self_frequency_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter frequency (e.g., Daily, Weekly)",
            width=200,
            fg_color="#FCEBF0",
            text_color="#89495D",
            border_color="#FCEBF0",
            corner_radius=10,
        )

# Define Main Application Class
class HabitTrackerApp(ctk.CTk):
    """Main application class for the Habit Tracker."""

    def __init__(self):
        super().__init__()
        self.title("Habit Tracker")
        self.geometry("800x600")
        self.resizable(True, True)
        self.configure(fg_color="#BC84AB")
        self.MainScreen = MainScreen(self)
        # Show the splash screen first

        # Splash Frame
        self.splash_frame = ctk.CTkFrame(self, fg_color="#BC84AB")
        self.splash_frame.pack(fill="both", expand=True)
        
        # Top spacer
        ctk.CTkFrame(self.splash_frame, fg_color="#BC84AB").pack(expand=True, fill="both")

        self.label = ctk.CTkLabel(
            self.splash_frame,
            text="Loading Habit Tracker...",
            font=("Roboto", 40, "bold"),
            text_color="white",
        )
        self.label.pack(pady=20, padx=40)

        self.progress_bar = ctk.CTkProgressBar(
            self.splash_frame, mode="indeterminate", width=300
        )
        self.progress_bar.pack(pady=40, padx=20)
        self.progress_bar.configure(fg_color="#F2C6D4", bg_color="#BC84AB", progress_color="#89495D")
        self.progress_bar.start()
        
        # Bottom spacer
        ctk.CTkFrame(self.splash_frame, fg_color="#BC84AB").pack(expand=True, fill="both")

        # After 5 seconds, show the main app
        self.after(5000, self.splash_disappear)

    def splash_disappear(self):
        """Hide the splash screen and show the main app."""
        self.splash_frame.pack_forget()
        self.label.pack_forget()
        self.MainScreen.pack(expand=True, fill="both")
        self.MainScreen.label.pack(pady=20)
        self.MainScreen.overlay_frame.pack(expand=True, fill="both", padx=40, pady=40)

if __name__ == "__main__":
    app = HabitTrackerApp()
    app.mainloop()
