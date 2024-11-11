# todo.py

from datetime import datetime


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
            print(f"Task '{removed_task.description}' deleted successfully.")
        else:
            print("Invalid task number. No task deleted.")

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            print(f"Task '{self.tasks[index].description}' marked as completed.")
        else:
            print("Invalid task number. No task marked as completed.")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks in the list.")
            return
        for i, task in enumerate(self.tasks):
            print(f"{i + 1}. {task.display()}")

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
                    status, title, description, start_date, end_date = line.strip().split(",", 4)
                    task = Task(title, description, start_date, end_date)
                    if status == "1":
                        task.mark_completed()
                    self.tasks.append(task)
            print("Tasks loaded from file successfully.")
        except FileNotFoundError:
            print("No saved tasks found.")


def main():
    todo_list = ToDoList()
    todo_list.load_from_file()

    while True:
        print("\nTo-Do List Application")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Complete Task")
        print("4. List Tasks")
        print("5. Save and Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            todo_list.add_task(title, description, start_date, end_date)
        elif choice == "2":
            todo_list.list_tasks()
            index = int(input("Enter task number to delete: ")) - 1
            todo_list.delete_task(index)
        elif choice == "3":
            todo_list.list_tasks()
            index = int(input("Enter task number to complete: ")) - 1
            todo_list.complete_task(index)
        elif choice == "4":
            todo_list.list_tasks()
        elif choice == "5":
            todo_list.save_to_file()
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()
