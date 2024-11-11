from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class Task:
    def __init__(self, title, description, start_date, end_date):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def display(self):
        status = "✓" if self.completed else "✗"
        return (f"[{status}] {self.title}\n"
                f"    Description: {self.description}\n"
                f"    Start Date: {self.start_date}\n"
                f"    End Date: {self.end_date}")

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, start_date, end_date):
        task = Task(title, description, start_date, end_date)
        self.tasks.append(task)
        print(f"Task '{title}' added successfully.")

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            removed_task = self.tasks.pop(index)
            print(f"Task '{removed_task.title}' deleted successfully.")
        else:
            print("Invalid task number. No task deleted.")

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            print(f"Task '{self.tasks[index].title}' marked as completed.")
        else:
            print("Invalid task number. No task marked as completed.")

    def save_to_file(self, filename="tasks.txt"):
        with open(filename, "w") as file:
            for task in self.tasks:
                status = "1" if task.completed else "0"
                file.write(f"{status},{task.title},{task.description},{task.start_date},{task.end_date}\n")
        print("Tasks saved to file successfully.")

    def load_from_file(self, filename="tasks.txt"):
        try:
            with open(filename, "r") as file:
                self.tasks = []
                for line in file:
                    parts = line.strip().split(",", 4)
                    if len(parts) == 5:
                        status, title, description, start_date, end_date = parts
                        task = Task(title, description, start_date, end_date)
                        if status == "1":
                            task.mark_completed()
                        self.tasks.append(task)
                    else:
                        print("Skipping malformed line in tasks file.")
            print("Tasks loaded from file successfully.")
        except FileNotFoundError:
            print("No saved tasks found.")

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")

        # Initialize ToDoList instance
        self.todo_list = ToDoList()
        self.todo_list.load_from_file()  # Load tasks from file at startup

        # Create GUI layout
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        tk.Label(self.root, text="To-Do List", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=4)

        # Task Listbox
        self.task_listbox = tk.Listbox(self.root, width=50, height=15)
        self.task_listbox.grid(row=1, column=0, columnspan=4)
        self.update_task_listbox()

        # Input fields for new task
        tk.Label(self.root, text="Title:").grid(row=2, column=0, sticky="e")
        self.title_entry = tk.Entry(self.root, width=20)
        self.title_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Description:").grid(row=3, column=0, sticky="e")
        self.description_entry = tk.Entry(self.root, width=20)
        self.description_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Start Date (YYYY-MM-DD):").grid(row=4, column=0, sticky="e")
        self.start_date_entry = tk.Entry(self.root, width=20)
        self.start_date_entry.grid(row=4, column=1)

        tk.Label(self.root, text="End Date (YYYY-MM-DD):").grid(row=5, column=0, sticky="e")
        self.end_date_entry = tk.Entry(self.root, width=20)
        self.end_date_entry.grid(row=5, column=1)

        # Buttons
        tk.Button(self.root, text="Add Task", command=self.add_task).grid(row=6, column=0, pady=10)
        tk.Button(self.root, text="Delete Task", command=self.delete_task).grid(row=6, column=1, pady=10)
        tk.Button(self.root, text="Mark Completed", command=self.mark_task_completed).grid(row=6, column=2, pady=10)
        tk.Button(self.root, text="Save & Exit", command=self.save_and_exit).grid(row=6, column=3, pady=10)

    def update_task_listbox(self):
        # Clear the listbox and re-populate it
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.todo_list.tasks):
            status = "✓" if task.completed else "✗"
            self.task_listbox.insert(tk.END, f"{i + 1}. [{status}] {task.title} - {task.description}")

    def add_task(self):
        # Get input values
        title = self.title_entry.get()
        description = self.description_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        # Check if start_date is today or in the future
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            if start_date_obj < datetime.now():
                messagebox.showwarning("Date Error", "Start date cannot be in the past. Please enter a valid date.")
                return
        except ValueError:
            messagebox.showwarning("Date Format Error", "Invalid start date format. Please use YYYY-MM-DD.")
            return

        # Add task to the list if all fields are valid
        if title and description and start_date and end_date:
            self.todo_list.add_task(title, description, start_date, end_date)
            self.update_task_listbox()
            messagebox.showinfo("Success", "Task added successfully.")
            # Clear input fields
            self.title_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.start_date_entry.delete(0, tk.END)
            self.end_date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.todo_list.delete_task(index)
            self.update_task_listbox()
            messagebox.showinfo("Success", "Task deleted successfully.")
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def mark_task_completed(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.todo_list.complete_task(index)
            self.update_task_listbox()
            messagebox.showinfo("Success", "Task marked as completed.")
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    def save_and_exit(self):
        self.todo_list.save_to_file()
        messagebox.showinfo("Save", "Tasks saved successfully.")
        self.root.quit()

# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
