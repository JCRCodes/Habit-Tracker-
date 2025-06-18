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

# db = HabitDatabase(connection_string)
class SplashScreenFrame(ctk.CTkFrame):
    """Splash screen frame."""
    def __init__(self, master, show_main_callback):
        super().__init__(master)
        self.configure(fg_color="#BC84AB")
        # Top spacer
        top_spacer = ctk.CTkFrame(self, height=200, fg_color="#BC84AB")
        top_spacer.pack(fill="x")
        
        # Centered splash content
        ctk.CTkLabel(self, text="Habit Tracker is loading...", font=("Roboto", 40, "bold"), text_color="#FFFFFF").pack(pady=40)
        progress = ctk.CTkProgressBar(self, mode="indeterminate", width=300, fg_color="#FFFFFF", progress_color="#631F5D")
        progress.pack(pady=20)
        progress.start()
        
        # Bottom spacer 
        bottom_spacer = ctk.CTkFrame(self, height=100, fg_color="#BC84AB")
        bottom_spacer.pack(fill="x", side="bottom")
        
        # After 2 seconds, show main screen
        self.after(2000, show_main_callback)

class MainScreen(ctk.CTkFrame):
    """Main screen for viewing and managing habits."""
    def __init__(self, master, show_add_habit_callback):
        super().__init__(master)
        self.configure(fg_color="#BC84AB")
        # White overlay
        overlay = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        overlay.pack(expand=True, fill="both", padx=40, pady=40)
        # Heading
        ctk.CTkLabel(overlay, text="Habit Tracker", font=("Helevetica", 32, "bold"), text_color="#BC84AB").pack(pady=(40, 20))

        # Top Padding
        top_padding = ctk.CTkFrame(overlay, height=50, fg_color="white")
        top_padding.pack(fill="x")
        
        # Add New Habit button
        ctk.CTkButton(
            overlay,
            text="Add New Habit",
            text_color="white",
            font=("Helevetica", 18, "bold"),
            fg_color="#BC84AB",
            hover_color="#A0699B",
            height=80,
            width=200,
            command=show_add_habit_callback
            ).pack(pady=10)

        # View My Habits Button
        ctk.CTkButton(
            overlay,
            text="View My Habits",
            text_color="white",
            font=("Helevetica", 18, "bold"),
            fg_color="#BC84AB",
            hover_color="#631F5D",
            height=80,
            width=200,
        ).pack(pady=10)

        # View Streak History Button
        ctk.CTkButton(
            overlay,
            text="View Streak History",
            text_color="white",
            font=("Helevetica", 18, "bold"),
            fg_color="#BC84AB",
            hover_color="#631F5D",
            height=80,
            width=200,
        ).pack(pady=10)

        # Bottom Padding
        bottom_padding = ctk.CTkFrame(
            overlay,
            height= 20,
            fg_color="white"
        )
        bottom_padding.pack(fill="x", side="bottom")

    def delete_habit(self):
        # Logic for deleting a habit
        pass

    def amend_habit(self):
        # Logic for amending a habit
        pass

class AddHabitFrame(ctk.CTkFrame):
    """Frame for adding a new habit."""
    def __init__(self, master, show_main_callback):
        super().__init__(master)
        self.configure(fg_color="#BC84AB")
        
        
        overlay = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        overlay.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Heading Padding
        heading_padding = ctk.CTkFrame(
        overlay,
        height=20,
        fg_color="white"    
        )
        heading_padding.pack(fill="x")
        
        # Heading Label
        ctk.CTkLabel(
        overlay,
        text="Add a New Habit",
        font=("Helevetica",
        28,
        "bold"),
        text_color="#BC84AB"
        ).pack(pady=30)
        
        # Top Padding
        top_padding = ctk.CTkFrame(overlay, height=50, fg_color="white")
        top_padding.pack(fill="x")
        
        
        # Input fields for habit name and description
        self.habit_entry = ctk.CTkEntry(overlay,
        fg_color="#FFFFFF",
        border_color="#BC84AB",
        border_width=2,
        text_color="#BC84AB",
        placeholder_text="Habit name",
        placeholder_text_color="#BC84AB",
        corner_radius=10,
        font=("Helevetica",
        16),
        width=300
        ).pack(pady=10)

        # Habit Name Entry Configuration
        self.configure(
        corner_radius=10,
        fg_color="#BC84AB",
        )
        
        # Habit Description Entry
        self.desc_entry = ctk.CTkEntry(overlay,
        fg_color="#FFFFFF",
        border_color="#BC84AB",
        border_width=2,
        text_color="#BC84AB",
        placeholder_text="Description",
        placeholder_text_color="#BC84AB",
        font=("Helevetica",
        16),
        width=300
        ).pack(pady=10)

        
        # Habit Frequency Dropdown

        self.frequency_var = ctk.StringVar(value="Select Frequency")
        ctk.CTkLabel(
        overlay,
        text="Select Frequency",
        font=("Helevetica", 16),
        text_color="#BC84AB")
        
        self.frequency_menu = ctk.CTkOptionMenu(
        overlay,
        variable=self.frequency_var,
        values=["Daily", "Weekly", "Monthly"],
        fg_color="#BC84AB",
        button_color="#BC84AB",
        button_hover_color="#A0699B",
        text_color="#FFFFFF",
        dropdown_fg_color="#FFFFFF",
        dropdown_text_color="#BC84AB",  
        dropdown_hover_color="#DBC4D9",
        dropdown_font=("Helevetica", 16),
        font=("Helevetica", 16),
        width=200
        )
        
        self.frequency_menu.set("Select Frequency")
        self.frequency_menu.pack(pady=20)
        
        
        # Habit Category Dropdown
        self.category_var = ctk.StringVar(value="Select Category")
        ctk.CTkLabel(
        overlay,
        text="Select Category",
        font=("Helevetica", 16),
        text_color="#BC84AB"
        )
        
        self.frequency_menu = ctk.CTkOptionMenu(
        overlay,
        variable=self.category_var,
        values=["Health", "Productivity", "Personal", "Other"],
        fg_color="#BC84AB",
        button_color="#BC84AB",
        button_hover_color="#A0699B",
        text_color="#FFFFFF",
        dropdown_fg_color="#FFFFFF",
        dropdown_text_color="#BC84AB",
        dropdown_hover_color="#DBC4D9",
        dropdown_font=("Helevetica", 16),
        font=("Helevetica", 16),
        width=200
        ).pack(pady=10)
        
        
        
        # Button Frame
        button_row = ctk.CTkFrame(
            overlay,
            fg_color="white",
            corner_radius=10
        )
        button_row.pack(pady=30)
        
        ## Enter Habit Button
        self.save_button = ctk.CTkButton(
            button_row,
            text="Save",
            text_color="white",
            font=("Helevetica", 16, "bold"),
            fg_color="#BC84AB",
            hover_color="#A0699B",
            #command=self.save_habit,
            width=100
        ).pack(side="left", padx=5)

        ## Back to Main Screen Button
        self.back_button = ctk.CTkButton(
            button_row,
            text="Back",
            text_color="white",
            font=("Helevetica", 16, "bold"),
            fg_color="#BC84AB",
            hover_color="#A0699B",
            #command=self.show_main_screen,
            width=100
        ).pack(side="right", padx=5)

class App(ctk.CTk):
    """Main application window."""
    def __init__(self):
        super().__init__()
        self.title("Habit Tracker")
        self.geometry("800x600")
        # Initialize frames
        self.splash = SplashScreenFrame(self, self.show_main_screen)
        self.main = MainScreen(self, self.show_add_habit_screen)
        self.add_habit = AddHabitFrame(self, self.show_main_screen)
        # Show splash screen first
        self.show_splash_screen()

    def show_splash_screen(self):
        self.hide_all_frames()
        self.splash.pack(expand=True, fill="both")

    def show_main_screen(self):
        self.hide_all_frames()
        self.main.pack(expand=True, fill="both")

    def show_add_habit_screen(self):
        self.hide_all_frames()
        self.add_habit.pack(expand=True, fill="both")

    def hide_all_frames(self):
        for frame in (self.splash, self.main, self.add_habit):
            frame.pack_forget()

if __name__ == "__main__":
    app = App()
    app.mainloop()
