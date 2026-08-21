import json
from datetime import datetime

DATA_FILE = "tasks.json"


def read_tasks():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_tasks(tasks):
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def get_new_id(tasks):
    if not tasks:
        return 1

    return max(task["id"] for task in tasks) + 1


def choose_priority():
    while True:
        print("\nChoose priority:")
        print("1. High")
        print("2. Medium")
        print("3. Low")

        option = input("Enter your choice: ").strip()

        priorities = {
            "1": "High",
            "2": "Medium",
            "3": "Low"
        }

        if option in priorities:
            return priorities[option]

        print("Invalid choice. Please select 1, 2, or 3.")


def add_task(tasks):
    print("\n========== ADD TASK ==========")

    title = input("Enter task title: ").strip()

    if title == "":
        print("Task title cannot be empty.")
        return

    priority = choose_priority()

    print("\nChoose a category:")
    print("1. Work")
    print("2. Study")
    print("3. Personal")

    category_choices = {
        "1": "Work",
        "2": "Study",
        "3": "Personal"
    }

    while True:
        category_choice = input("Enter category (1-3): ").strip()

        if category_choice in category_choices:
            category = category_choices[category_choice]
            break

        print("Invalid choice. Please select 1, 2, or 3.")

    due_date = input(
        "Enter due date (YYYY-MM-DD) or press Enter to skip: "
    ).strip()

    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format.")
            return
    else:
        due_date = "Not set"

    new_task = {
        "id": get_new_id(tasks),
        "title": title,
        "priority": priority,
        "category": category,
        "due_date": due_date,
        "status": "Pending",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    tasks.append(new_task)
    write_tasks(tasks)

    print(f"\nTask added successfully! ID: {new_task['id']}")


def display_tasks(tasks):
    if not tasks:
        print("\nNo tasks available.")
        return

    print("\n" + "=" * 80)
    print(f"{'ID':<5}{'TASK':<30}{'PRIORITY':<12}"
          f"{'CATEGORY':<12}{'STATUS':<12}{'DUE DATE':<15}")
    print("=" * 80)

    priority_rank = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    ordered_tasks = sorted(
        tasks,
        key=lambda task: priority_rank.get(task["priority"], 4)
    )

    for task in ordered_tasks:
        print(
            f"{task['id']:<5}"
            f"{task['title'][:28]:<30}"
            f"{task['priority']:<12}"
            f"{task.get('category', 'Uncategorized'):<12}"
            f"{task['status']:<12}"
            f"{task['due_date']:<15}"
        )

    print("=" * 80)


def show_pending(tasks):
    pending = [
        task for task in tasks
        if task["status"] == "Pending"
    ]

    print("\n========== PENDING TASKS ==========")
    display_tasks(pending)


def show_high_priority(tasks):
    high_tasks = [
        task for task in tasks
        if task["priority"] == "High"
    ]

    print("\n========== HIGH PRIORITY ==========")
    display_tasks(high_tasks)


def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return None


def complete_task(tasks):
    print("\n========== COMPLETE TASK ==========")

    try:
        task_id = int(input("Enter task ID: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    task = find_task(tasks, task_id)

    if task is None:
        print("Task not found.")
        return

    if task["status"] == "Done":
        print("This task is already completed.")
        return

    task["status"] = "Done"
    write_tasks(tasks)

    print(f"'{task['title']}' has been completed.")

def edit_task(tasks):
    print("\n========== EDIT TASK ==========")

    try:
        task_id = int(input("Enter the ID of the task to edit: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    task = find_task(tasks, task_id)

    if task is None:
        print("Task not found.")
        return

    print(f"\nCurrent title: {task['title']}")
    print(f"Current priority: {task['priority']}")

    print("\nWhat would you like to edit?")
    print("1. Title")
    print("2. Priority")
    print("3. Both")
    print("4. Cancel")

    choice = input("Choose an option: ").strip()

    if choice in ("1", "3"):
        new_title = input("Enter the new title: ").strip()

        if new_title:
            task["title"] = new_title
        else:
            print("Title cannot be empty.")
            return

    if choice in ("2", "3"):
        task["priority"] = choose_priority()

    if choice == "4":
        print("Edit cancelled.")
        return

    if choice not in ("1", "2", "3", "4"):
        print("Invalid choice.")
        return

    write_tasks(tasks)
    print("Task updated successfully!")

def delete_task(tasks):
    print("\n========== DELETE TASK ==========")

    try:
        task_id = int(input("Enter task ID: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    task = find_task(tasks, task_id)

    if task is None:
        print("Task not found.")
        return

    print(f"\nTask: {task['title']}")

    confirmation = input("Delete this task? (y/n): ").strip().lower()

    if confirmation == "y":
        tasks.remove(task)
        write_tasks(tasks)
        print("Task deleted successfully.")
    else:
        print("Task was not deleted.")


def search_tasks(tasks):
    print("\n========== SEARCH TASKS ==========")

    keyword = input("Enter a keyword: ").strip().lower()

    matches = [
        task for task in tasks
        if keyword in task["title"].lower()
    ]

    display_tasks(matches)

def show_overdue_tasks(tasks):
    print("\n========== OVERDUE TASKS ==========")

    today = datetime.now().date()
    overdue = []

    for task in tasks:
        if task["due_date"] == "Not set":
            continue

        try:
            due = datetime.strptime(
                task["due_date"], "%Y-%m-%d"
            ).date()
        except ValueError:
            continue

        if due < today and task["status"] == "Pending":
            overdue.append(task)

    if overdue:
        print("These tasks are overdue:")
        display_tasks(overdue)
    else:
        print("No overdue tasks found.")

def show_due_today(tasks):
    print("\n========== TASKS DUE TODAY ==========")

    today = datetime.now().strftime("%Y-%m-%d")

    due_today = [
        task for task in tasks
        if task["due_date"] == today
        and task["status"] == "Pending"
    ]

    if due_today:
        print("These tasks are due today:")
        display_tasks(due_today)
    else:
        print("No tasks are due today.")

def show_statistics(tasks):
    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task["status"] == "Done"
    )

    pending = total - completed

    high_pending = sum(
        1 for task in tasks
        if task["priority"] == "High"
        and task["status"] == "Pending"
    )

    print("\n========== STATISTICS ==========")
    print(f"Total tasks       : {total}")
    print(f"Completed tasks   : {completed}")
    print(f"Pending tasks     : {pending}")
    print(f"High priority     : {high_pending}")

    if total > 0:
        percentage = (completed / total) * 100
        print(f"Completion rate   : {percentage:.0f}%")
    else:
        print("Completion rate   : 0%")


def main():
    tasks = read_tasks()

    while True:
        print("\n")
        print("=" * 40)
        print("        TO-DO LIST MANAGER")
        print("=" * 40)
        print("1. Add a task")
        print("2. View all tasks")
        print("3. View pending tasks")
        print("4. View high-priority tasks")
        print("5. Mark task as completed")
        print("6. Delete a task")
        print("7. Search tasks")
        print("8. Show statistics")
        print("9. Edit a task")
        print("10. Show overdue tasks")
        print("11. Show tasks due today")
        print("12. Exit")
        print("=" * 40)

        choice = input("Select an option (1-9): ").strip()

        if choice == "1":
            add_task(tasks)

        elif choice == "2":
            display_tasks(tasks)

        elif choice == "3":
            show_pending(tasks)

        elif choice == "4":
            show_high_priority(tasks)

        elif choice == "5":
            complete_task(tasks)

        elif choice == "6":
            delete_task(tasks)

        elif choice == "7":
            search_tasks(tasks)

        elif choice == "8":
            show_statistics(tasks)

        elif choice == "9":
            edit_task(tasks)

        elif choice == "10":
            show_overdue_tasks(tasks)

        elif choice == "11":
            show_due_today(tasks)

        elif choice == "12":
            print("\nThank you for using the To-Do List Manager!")
            break

        else:
            print("\nInvalid option. Please choose 1-12.")


if __name__ == "__main__":
    main()