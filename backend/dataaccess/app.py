"""Main application file for the Habit Tracker app."""

import os
import threading
from dotenv import load_dotenv
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from data_access import HabitDatabase

# Load environment variables and connect to the database
load_dotenv()
connection_string = os.getenv("DB_CONNECTION_STRING")
if connection_string is None:
    raise ValueError("Database connection string must not be None. Check your .env file.")

db = HabitDatabase(connection_string)

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
            font=("Inter", 40, "bold"),
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


# --- Main Application Window ---
class App(ctk.CTk):
    def __init__(self, connection_string):
        super().__init__()
        self.db = HabitDatabase(connection_string)
        self.title("Habit Tracker")
        self.geometry("800x600")

        # Instantiate frames
        self.frames = {}
        self.frames["main"] = MainScreen(self, self.show_add_habit, self.show_view_habits)
        self.frames["add"] = AddHabitFrame(self, self.show_main, self.db)
        self.frames["view"] = ViewHabitsFrame(self, self.show_amend_habit, self.show_main, self.db)
        self.frames["amend"] = None  # Created as needed

        self.show_main()
        
    # Functions

    def show_main(self):
        self.hide_all_frames()
        self.frames["main"].pack(expand=True, fill="both")

    def show_add_habit(self):
        self.hide_all_frames()
        self.frames["add"].pack(expand=True, fill="both")

    def show_view_habits(self):
        self.hide_all_frames()
        self.frames["view"].load_habits()
        self.frames["view"].pack(expand=True, fill="both")

    def show_amend_habit(self, habit_data):
        self.hide_all_frames()
        self.frames["amend"] = AmendHabitFrame(self, habit_data, self.show_view_habits, self.db)
        self.frames["amend"].pack(expand=True, fill="both")

    def hide_all_frames(self):
        for frame in self.frames.values():
            if frame is not None:
                frame.pack_forget()

# --- Main Screen ---
class MainScreen(ctk.CTkFrame):
    def __init__(self, master, show_add_habit_callback, show_view_habits_callback):
        super().__init__(master)
        self.configure(fg_color="#FFFFFF")
        
        
        # ---- Config and Overlay  ----
        overlay = ctk.CTkFrame(
            self, 
            fg_color="#87A988", 
            corner_radius=20
        )
        overlay.pack(expand=True, fill="both", padx=20, pady=20)
        
        # ---- Widgets ----
        
        
        # Welcome Label
        welcome_label = ctk.CTkLabel(
            overlay,
            text="Welcome to your Habit Tracker",
            font=("Inter", 32, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=40, padx = 40)
        
        
        
        # ---- Padding ----
        
        top_padding = ctk.CTkFrame(
            overlay,
            fg_color="#87A988",
            height=50,
            width=200
        ).pack(pady=20, padx=20)
        
        # View Habits Button
        view_my_habits_btn = ctk.CTkButton(
            overlay,
            command = show_view_habits_callback,
            text="View My Habits",
            font=("Inter", 24),
            height=50,
            width=200,
            fg_color="#C289B0",
            hover_color="#631F5D",
        ).pack(pady=10, padx=20)
        
        # Add Habits Button
        add_habit_btn = ctk.CTkButton(
            overlay,
            command = show_add_habit_callback,
            text="Add Habit",
            font=("Inter", 24),
            height=50,
            width=200,
            fg_color="#C289B0",
            hover_color="#631F5D",
        ).pack(pady=10, padx=20)

    
# ---- View Habits Frame ---
class ViewHabitsFrame(ctk.CTkFrame):
    def __init__(self, master, show_amend_callback, show_main_callback, db):
        super().__init__(master)
        self.db = db
        self.show_amend_callback = show_amend_callback
        self.show_main_callback = show_main_callback
        self.configure(fg_color="#FFFFFF")
        
        # ---- Config and Overlay  ----
        
        overlay = ctk.CTkFrame(
            self, 
            fg_color="#87A988", 
            corner_radius=20
        )
        overlay.pack(expand=True, fill="both", padx=20, pady=20)
        
        
        
        # ----Heading & Padding ----
        
        welcome_label = ctk.CTkLabel(
            overlay,
            text="Your Habits",
            font=("Inter", 32, "bold"),
            text_color="#FFFFFF"
        ).pack(padx=40, pady=40)
        
        # ---- Padding ----
        
        top_padding = ctk.CTkFrame(
            overlay,
            fg_color="#87A988",
            height=10,
            width=50
        ).pack(pady=10)
        
        # ---- Treeview Setup ----
        self.tree = ttk.Treeview(overlay, columns=("Name", "Description", "Category", "Frequency"),
        show="headings")
        
        style= ttk.Style()
        style.configure("Treeview", background="#FFFFFF", foreground="#FFFFFF", font=("Inter", 20))

        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # ---- Treeview Columns ----
        self.tree.heading("Name", text="Habit Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Frequency", text="Frequency")
        self.tree.column("Name", anchor="center")
        self.tree.column("Description", anchor="center")
        self.tree.column("Category", anchor="center")
        self.tree.column("Frequency", anchor="center")
        self.tree.pack(expand=True, fill="both", padx=20, pady=20)
        
        # ---- Widgets ----

        
        back_to_main_btn = ctk.CTkButton(
            overlay,
            command = show_main_callback,
            text="Back to Main",
            text_color="#FFFFFF",
            font=("Inter", 18),
            height=30,
            width=200,
            fg_color="#C289B0",
            hover_color="#631F5D",
        ).pack(pady=20, padx=20)
        
        
    # CRUD Operations
    
    # LOAD HABITS
    def load_habits(self):
        # Clear and reload habits from db
        self.tree.delete(*self.tree.get_children())
        for habit in self.db.get_user_habits(user_id=1):  # Replace with actual user logic
            self.tree.insert("", "end", values=habit[1:5])  # Adjust indices as needed

    # DOUBLE CLICK TO AMEND HABIT
    def on_double_click(self, event):
        selected = self.tree.selection()
        if selected:
            habit_data = self.tree.item(selected[0], "values")
            # You may need to fetch the habit ID separately
            self.show_amend_callback(habit_data)      

# --- Add Habit Frame ---
class AddHabitFrame(ctk.CTkFrame):
    def __init__(self, master, show_main_callback, db):
        super().__init__(master)
        self.db = db
        self.show_main_callback = show_main_callback
        
        self.configure(fg_color="#FFFFFF")
        
        # ---- Config and Overlay  ----
        
        overlay = ctk.CTkFrame(
            self, 
            fg_color="#87A988", 
            corner_radius=20
        )
        
        overlay.pack(expand=True, fill="both", padx=20, pady=20)
        
        # ---- Widgets ----
        
        add_habit_label = ctk.CTkLabel(
            overlay,
            text="Add New Habit",
            font=("Inter", 32, "bold"),
            text_color="#FFFFFF"
        ).pack(padx=40, pady=40)
        
        # ---- Padding ----
        
        top_padding = ctk.CTkFrame(
            overlay,
            fg_color="#87A988",
            height=10,
            width=200
        ).pack(pady=10)
        
        # ---- Input Fields ----
        self.name_entry = ctk.CTkEntry(overlay, placeholder_text="Habit Name", font=("Inter", 20, "italic"))
        self.name_entry.configure(width=300,
            fg_color="#FFFFFF",
            border_color="#FFFFFF",
            text_color="#000000",
            placeholder_text_color="#757575"
        )
        self.name_entry.pack(pady=10, padx=20)  
        
        self.description_entry = ctk.CTkEntry(overlay, placeholder_text="Description", font=("Inter", 20, "italic"))
        self.description_entry.configure(width=300,
            fg_color="#FFFFFF",
            border_color="#FFFFFF",
            text_color="#000000",
            placeholder_text_color="#757575"
        )
        self.description_entry.pack(pady=10, padx=20)
        
        self.category_entry = ctk.CTkEntry(overlay, placeholder_text="Category", font=("Inter", 20, "italic"))
        self.category_entry.configure(width=300,
            fg_color="#FFFFFF",
            border_color="#FFFFFF",
            text_color="#000000",
            placeholder_text_color="#757575"
        )
        self.category_entry.pack(pady=10, padx=20)
        
        dropdown = ctk.CTkOptionMenu(
            overlay,
            values=["Daily", "Weekly", "Monthly", "Yearly"],
            fg_color="#FFFFFF",
            text_color="#757575",
            font=("Inter", 20, "italic")
        )
        dropdown.set("Frequency")
        dropdown.configure(width=300)
        dropdown.pack(pady=10, padx=20)
        
        submit_btn = ctk.CTkButton(
            overlay,
            command=self.save_habit,
            text="Subit Habit",
            text_color="#FFFFFF",
            font=("Inter", 24),
            height=50,
            width=200,
            fg_color="#C289B0",
            hover_color="#631F5D",
        ).pack(pady=20, padx=20)
        
        back_to_main_btn = ctk.CTkButton(
            overlay,
            command = show_main_callback,
            text="Back to Main",
            text_color="#FFFFFF",
            font=("Inter", 18),
            height=30,
            width=200,
            fg_color="#C289B0",
            hover_color="#631F5D",
        ).pack(side="bottom", pady=20, padx=20)
        
        
    # CRUD Operations

    # SAVE HABIT
    def save_habit(self):
        
        name = self.name_entry.get()
        # ... get other fields ...
        # self.db.add_habit(...)
        # Show messagebox and return to main if successful
        pass

# --- Amend Habit Frame ---
class AmendHabitFrame(ctk.CTkFrame):
    def __init__(self, master, habit_data, show_view_habits_callback, db):
        super().__init__(master)
        self.db = db
        self.category_entry = ctk.CTkEntry(self)
        
        self.habit_id = habit_data[0]  # Adjust index as needed
        self.show_view_habits_callback = show_view_habits_callback
        
        # ---- Config and Overlay  ----
        
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.insert(0, habit_data[1])
        self.name_entry.pack(pady=5)
        
        self.description_entry = ctk.CTkEntry(self)
        self.description_entry.insert(0, habit_data[2])
        self.description_entry.pack(pady=5)
        
        self.category_entry.insert(0, habit_data[3])
        self.category_entry.pack(pady=5)
        self.frequency_dropdown = ctk.CTkOptionMenu(
            self,
            values=["Daily", "Weekly", "Monthly", "Yearly"],
            fg_color="#FFFFFF",
            text_color="#757575",
            font=("Inter", 20, "italic")
        )
        
        self.frequency_dropdown.set(habit_data[4])  # Set current frequency
        self.frequency_dropdown.pack(pady=5)
        
        ctk.CTkButton(self, text="Save Changes", command=self.update_habit).pack(pady=10)
        ctk.CTkButton(self, text="Delete", command=self.delete_habit).pack(pady=10)
        ctk.CTkButton(self, text="Back", command=show_view_habits_callback).pack(pady=10)

    def update_habit(self):
        user_id = 1  # Replace with actual user logic
        name = self.name_entry.get()
        desc = self.description_entry.get()
        category = self.category_entry.get()
        frequency = self.frequency_dropdown.get()
        success = self.db.update_habit(
            habit_id=self.habit_id,
            user_id=user_id,
            habit_name=name,
            description=desc,
            category=category,
            frequency=frequency
        )
        if success:
            messagebox.showinfo("Success", "Habit updated successfully.")
            self.show_view_habits_callback()
        else:
            messagebox.showerror("Error", "Failed to update habit. Please try again.")

    def delete_habit(self):
        answer = messagebox.askyesno("Delete Habit", "Are you sure you want to delete this habit?")
        if answer:
            if self.db.delete_habit(self.habit_id):
                messagebox.showinfo("Success", "Habit deleted successfully.")
                self.show_view_habits_callback()
            else:
                messagebox.showerror("Error", "Failed to delete habit. Please try again.")
                
                
                
                
                
#--- Main Application Entry Point ---
if __name__ == "__main__":
    connection_string = "YOUR_CONNECTION_STRING_HERE"
    app = App(connection_string)
    app.mainloop()

if __name__ == "__main__":
    app = App()
    app.mainloop()