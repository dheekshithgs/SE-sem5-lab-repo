"""Manage tasks, persist them safely, and export task data."""

import json
import secrets
import subprocess
from datetime import datetime
from pathlib import Path

tasks = {}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def add_task(title, priority="medium", labels=None):
    """Add a task and return its unique identifier."""
    if priority not in PRIORITY_ORDER:
        raise ValueError(f"Unsupported priority: {priority}")
    task_id = len(tasks) + 1
    task_labels = list(labels) if labels is not None else []
    task_labels.append(priority)
    tasks[task_id] = {
        "title": title,
        "priority": priority,
        "labels": task_labels,
        "done": False,
        "created": datetime.now().isoformat(),
    }
    return task_id


def complete_task(task_id):
    """Mark a task complete, returning whether the task exists."""
    task = tasks.get(task_id)
    if task is None:
        print("No task with id", task_id)
        return False
    task["done"] = True
    return True


def pending_tasks():
    """Return pending task titles ordered by priority."""
    pending = [task for task in tasks.values() if not task["done"]]
    pending.sort(key=lambda task: PRIORITY_ORDER[task["priority"]])
    return [task["title"] for task in pending]


def find_task(keyword):
    """Return the first matching task identifier, or None if not found."""
    for task_id, task in tasks.items():
        if keyword.casefold() in task["title"].casefold():
            return task_id
    return None


def save_tasks(file_name="tasks.json"):
    """Save tasks as JSON to avoid unsafe object deserialization."""
    with Path(file_name).open("w", encoding="utf-8") as file_handle:
        json.dump(tasks, file_handle, indent=2)


def load_tasks(file_name="tasks.json"):
    """Load tasks from a JSON file and validate its top-level structure."""
    with Path(file_name).open("r", encoding="utf-8") as file_handle:
        loaded_tasks = json.load(file_handle)
    if not isinstance(loaded_tasks, dict):
        raise ValueError("Task data must be a JSON object.")
    return {int(task_id): task for task_id, task in loaded_tasks.items()}


def export_json(file_name="tasks.json"):
    """Export tasks to a human-readable JSON file."""
    save_tasks(file_name)


def remind_by_email(address, file_name="tasks.json"):
    """Send the JSON task export to an address without invoking a shell."""
    with Path(file_name).open("r", encoding="utf-8") as file_handle:
        task_data = file_handle.read()
    subprocess.run(
        ["mail", "-s", "Pending tasks", address],
        input=task_data,
        text=True,
        check=False,
    )


def main():
    """Run a small demonstration of task management."""
    tasks.clear()
    add_task("Submit lab report", "high")
    add_task("Buy groceries")
    add_task("Call plumber", "low")
    add_task("Book train tickets", "high")
    complete_task(2)
    complete_task(99)
    print("Pending tasks:", pending_tasks())
    print("Task id for 'plumber':", find_task("plumber"))
    print("Task id for 'gym':", find_task("gym"))
    pending = pending_tasks()
    if pending:
        print("Try this next:", secrets.choice(pending))
    else:
        print("No pending tasks to suggest.")
    save_tasks()
    restored = load_tasks()
    print("Tasks restored from file:", len(restored))
    export_json()
    print("Exported tasks to tasks.json")


if __name__ == "__main__":
    main()
