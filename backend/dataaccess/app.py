"""Main application file for the Habit Tracker app."""

import os
import time
from datetime import datetime
import threading
from dotenv import load_dotenv
import customtkinter as ctk
from tkinter import ttk
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
        
        #### Top Padding ####
        
        top_padding = ctk.CTkFrame(
            self, 
            fg_color="#BC84AB"
        )
        top_padding.pack(padx=20, pady=20)
        
        ctk.CTkLabel(
            self,
            text="Habit Tracker is loading...",
            font=("Roboto", 40, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=20)
        progress = ctk.CTkProgressBar(
            self,
            mode="indeterminate",
            width=300,
            fg_color="#FFFFFF",
            progress_color="#631F5D"
        )
        progress.pack(pady=20)
        progress.start()
        self.after(2000, show_main_callback)

class MainScreen(ctk.CTkFrame):
    """Main screen for viewing and managing habits."""
    def __init__(self, master, show_add_habit_callback, show_view_habits_callback):
        super().__init__(master)
        self.configure(fg_color="#BC84AB")
        overlay = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        overlay.pack(expand=True, fill="both", padx=40, pady=40)
        ctk.CTkLabel(
            overlay,
            text="Habit Tracker",
            text_color="#664863",
            font=("Roboto", 32, "bold"),
            ).pack(pady=(20, 20))
        
        #### Button Frame 1 ####
        
        button_frame = ctk.CTkFrame(overlay, fg_color="white")
        button_frame.pack(side="top", anchor="n", pady=80, padx=40)
        
        ctk.CTkButton(
            button_frame,
            text="Add Habit",
            text_color="#FFFFFF",
            font=("Roboto", 16, "bold"),
            fg_color="#BC84AB",
            hover_color="#A86B8C",
            command=show_add_habit_callback,
            width=150,
            height=40
        ).pack(padx=20, side="left")
        ctk.CTkButton(
            button_frame,
            text="View Habits",
            text_color="#FFFFFF",
            font=("Roboto", 16, "bold"),
            fg_color="#BC84AB",
            hover_color="#A86B8C",
            command=show_view_habits_callback,
            width=150,
            height=40
        ).pack(padx=20, side="left")

        #### Button Spacer ####
        
        button_spacer = ctk.CTkFrame(overlay, fg_color="white")
        button_spacer.pack(expand=True, fill="both", pady=20)
        
        ctk.CTkLabel(
            overlay,
            fg_color= "white",
            text_color="#664863",
            text="Your Habits",
            font=("Roboto", 20, "bold")
        ).pack(pady=(20, 5))
        self.habits_box = ctk.CTkTextbox(overlay, width=500, height=200)
        self.habits_box.pack(pady=10)
        action_frame = ctk.CTkFrame(overlay, fg_color="white")
        action_frame.pack(pady=10)
        ctk.CTkButton(
            action_frame,
            text="Delete",
            command=self.delete_habit
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            action_frame,
            text="Amend",
            command=self.amend_habit
        ).pack(side="left", padx=10)

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
        ctk.CTkLabel(
            overlay,
            text="Add a New Habit:",
            text_color="#664863",
            font=("Inter", 28, "bold")
        ).pack(pady=30)
        
        #### Add Habit Padding ####
        
        add_habit_padding = ctk.CTkFrame(
            overlay,
            fg_color="white",
            height=20,
            width=200
            )
        add_habit_padding.pack(pady=10)

        self.habit_entry = ctk.CTkEntry(overlay,
                fg_color="white",
                border_color="#BC84AB",
                border_width=2,
                placeholder_text="   Habit name",
                font=("Inter", 20, "italic"), 
                width=400,
                height=60
        )
        self.habit_entry.pack(pady=10)
        self.desc_entry = ctk.CTkEntry(overlay,
                fg_color="white",
                border_color="#BC84AB",
                border_width=2,
                placeholder_text="   Description",
                width=400,
                height=60
        )
        self.habit_entry.pack(pady=10)
        
        
        self.desc_entry = ctk.CTkEntry(overlay,
                fg_color="white",
                border_color="#BC84AB",
                border_width=2,
                placeholder_text="   Description",
                font=("Inter", 20, "italic"),
                width=400,
                height=60
        )
        self.desc_entry.pack(pady=10, padx=20)
        self.frequency_var = ctk.StringVar(value="Frequency")
        self.frequency_menu = ctk.CTkOptionMenu(
            overlay,
            fg_color="#BC84AB",
            button_hover_color="#A86B8C",
            width=200,
            height=40,
            values=["Daily", "Weekly", "Monthly"],
            variable=self.frequency_var,
            button_color="#BC84AB",
            text_color="#FFFFFF",
            font=("Inter", 16),
            dropdown_font=("Inter", 16),
            dropdown_fg_color="white",
            dropdown_hover_color="#A86B8C",
            dropdown_text_color="#676667",
        )
        
        
        self.frequency_menu.pack(pady=10)
        button_row = ctk.CTkFrame(overlay, fg_color="white")
        button_row.pack(pady=10, padx=40)
        ctk.CTkButton(
            button_row,
            text="Enter Habit",
            text_color="#FFFFFF",
            font=("Inter", 12, "bold"),
            fg_color="#BC84AB",
            hover_color="#A86B8C",
            width=100,
            command=self.save_habit
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            button_row,
            text="Back",
            text_color="#FFFFFF",
            font=("Inter", 12, "bold"),
            fg_color="#BC84AB",
            hover_color="#A86B8C",
            width=100,
            command=show_main_callback
        ).pack(side="left", padx=10)

    def save_habit(self):
        # Logic for saving a new habit
        pass

class ViewHabitsFrame(ctk.CTkFrame):
    """Frame for viewing all habits."""
    def __init__(self, master, show_amend_habit_callback, show_main_callback):
        super().__init__(master)
        self.configure(fg_color="#BC84AB")
        overlay = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        overlay.pack(expand=True, fill="both", padx=40, pady=40)
        ctk.CTkLabel(
            overlay,
            text="Your Habits",
            font=("Roboto", 20, "bold")
        ).pack(pady=(20, 5))
        columns = ("Name", "Description", "Frequency")
        self.tree = ttk.Treeview(
            overlay,
            columns=columns,
            show="headings",
            height=8
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor="center")
        self.tree.pack(pady=20, padx=40, fill="x", anchor="n")
        self.tree.insert("", "end", values=("Drink Water", "Stay hydrated", "Daily"))
        self.tree.insert("", "end", values=("Read Book", "Read 10 pages", "Weekly"))
        def on_habit_select(event):
            selected = self.tree.selection()
            if selected:
                habit_data = self.tree.item(selected[0], "values")
                show_amend_habit_callback(habit_data)
        self.tree.bind("<<TreeviewSelect>>", on_habit_select)
        ctk.CTkButton(
            overlay,
            text="Back to Main Screen",
            command=show_main_callback
        ).pack(pady=10)

class AmendHabitFrame(ctk.CTkFrame):
    """Frame for amending a selected habit."""
    def __init__(self, master, habit_data, show_view_habits_callback):
        super().__init__(master)
        self.configure(fg_color="#BC84AB")
        overlay = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        overlay.pack(expand=True, fill="both", padx=40, pady=40)
        ctk.CTkLabel(
            overlay,
            text="Amend Habit",
            font=("Roboto", 24, "bold")
        ).pack(pady=20)
        self.name_entry = ctk.CTkEntry(overlay, placeholder_text="Name")
        self.name_entry.insert(0, habit_data[0])
        self.name_entry.pack(pady=10)
        self.desc_entry = ctk.CTkEntry(overlay, placeholder_text="Description")
        self.desc_entry.insert(0, habit_data[1])
        self.desc_entry.pack(pady=10)
        self.freq_entry = ctk.CTkEntry(overlay, placeholder_text="Frequency")
        self.freq_entry.insert(0, habit_data[2])
        self.freq_entry.pack(pady=10)
        ctk.CTkButton(
            overlay,
            text="Save Changes",
            command=self.save_changes
        ).pack(pady=10)
        ctk.CTkButton(
            overlay,
            text="Delete Habit",
            command=self.delete_habit
        ).pack(pady=10)
        ctk.CTkButton(
            overlay,
            text="Back",
            command=show_view_habits_callback
        ).pack(pady=10)

    def save_changes(self):
        # Update the habit in the database here
        pass

    def delete_habit(self):
        # Delete the habit from the database here
        pass

class App(ctk.CTk):
    """Main application window."""
    def __init__(self):
        super().__init__()
        self.title("Habit Tracker")
        self.geometry("800x600")
        self.splash = SplashScreenFrame(self, self.show_main_screen)
        self.main = MainScreen(self, self.show_add_habit_screen, self.show_view_habits_screen)
        self.add_habit = AddHabitFrame(self, self.show_main_screen)
        self.view_habits = ViewHabitsFrame(
            self,
            self.show_amend_habit_screen,
            self.show_main_screen
        )
        self.amend_habit_frame = None
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

    def show_view_habits_screen(self):
        self.hide_all_frames()
        self.view_habits.pack(expand=True, fill="both")

    def show_amend_habit_screen(self, habit_data):
        self.hide_all_frames()
        self.amend_habit_frame = AmendHabitFrame(
            self,
            habit_data,
            self.show_view_habits_screen
        )
        self.amend_habit_frame.pack(expand=True, fill="both")

    def hide_all_frames(self):
        for frame in [
            self.splash,
            self.main,
            self.add_habit,
            self.view_habits,
            self.amend_habit_frame
        ]:
            if frame is not None:
                frame.pack_forget()

if __name__ == "__main__":
    app = App()
    app.mainloop()