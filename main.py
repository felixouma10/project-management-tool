import argparse
import re

from datetime import date
from rich.console import Console
from rich.table import Table

from utils.storage import (
    load_users,
    save_users,
    load_projects,
    save_projects,
    load_tasks,
    save_tasks,
)

console = Console()


def next_id(records, key):
    """Generate the next ID for a collection."""
    return max((item[key] for item in records), default=0) + 1


def find_record(records, key, value):
    """Find a record by a field value."""
    return next(
        (record for record in records if record.get(key) == value),
        None,
    )


def add_user(args):
    """Create and save a user."""
    users = load_users()

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", args.email):
        console.print("[red]Please provide a valid email address.[/red]")
        return
    
    if not re.fullmatch(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", args.email):
        console.print("[red]Invalid email address.[/red]")
        return
    
    if any(user["email"] == args.email for user in users):
        console.print("[red]A user with this email already exists.[/red]")
        return

    user = {
        "user_id": next_id(users, "user_id"),
        "name": args.name,
        "email": args.email,
    }

    users.append(user)
    save_users(users)
    console.print(f"[green]Created user:[/green] {user}")


def list_users(args):
    """Display all users."""
    users = load_users()
    table = Table(title="Users")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Email")

    for user in users:
        table.add_row(
            str(user["user_id"]), user["name"], user["email"]
        )

    console.print(table)


def add_project(args):
    """Create a project for an existing user."""
    users = load_users()
    projects = load_projects()

    user = find_record(users, "user_id", args.user_id)
    if user is None:
        console.print("[red]User not found.[/red]")
        return

    if args.due_date:
        try:
            date.fromisoformat(args.due_date)
        except ValueError:
            console.print(
                "[red]Invalid due date. Use YYYY-MM-DD.[/red]"
            )
            return

    if args.due_date:
        try:
            date.fromisoformat(args.due_date)
        except ValueError:
            console.print(
                "[red]Invalid due date. Use YYYY-MM-DD.[/red]"
            )
            return

    project = {
        "project_id": next_id(projects, "project_id"),
        "title": args.title,
        "description": args.description,
        "due_date": args.due_date,
        "owner_id": args.user_id,
    }

    projects.append(project)
    save_projects(projects)
    console.print(f"[green]Created project:[/green] {project}")


def list_projects(args):
    """List all projects or filter by user ID."""
    projects = load_projects()

    if args.user_id is not None:
        projects = [
            project for project in projects
            if project["owner_id"] == args.user_id
        ]

    table = Table(title="Projects")
    table.add_column("ID", style="cyan")
    table.add_column("Title")
    table.add_column("Owner ID")
    table.add_column("Due Date")

    for project in projects:
        table.add_row(
            str(project["project_id"]),
            project["title"],
            str(project["owner_id"]),
            project["due_date"] or "Not set",
        )

    console.print(table)


def add_task(args):
    """Add a task to an existing project."""
    projects = load_projects()
    tasks = load_tasks()

    project = find_record(projects, "project_id", args.project_id)
    if project is None:
        console.print("[red]Project not found.[/red]")
        return

    task = {
        "task_id": next_id(tasks, "task_id"),
        "project_id": args.project_id,
        "title": args.title,
        "status": "pending",
        "assigned_to": [],
    }

    tasks.append(task)
    save_tasks(tasks)
    console.print(f"[green]Created task:[/green] {task}")


def list_tasks(args):
    """Display tasks belonging to a project."""
    tasks = [
        task for task in load_tasks()
        if task["project_id"] == args.project_id
    ]

    table = Table(title=f"Tasks for Project {args.project_id}")
    table.add_column("ID", style="cyan")
    table.add_column("Title")
    table.add_column("Status")
    table.add_column("Contributors")

    for task in tasks:
        contributors = ", ".join(map(str, task["assigned_to"])) or "None"
        table.add_row(
            str(task["task_id"]),
            task["title"],
            task["status"],
            contributors,
        )

    console.print(table)


def complete_task(args):
    """Mark a task as completed."""
    tasks = load_tasks()
    task = find_record(tasks, "task_id", args.task_id)

    if task is None:
        console.print("[red]Task not found.[/red]")
        return

    task["status"] = "completed"
    save_tasks(tasks)
    console.print(f"[green]Completed task:[/green] {task['title']}")


def assign_task(args):
    """Assign a user to a task."""
    users = load_users()
    tasks = load_tasks()

    if find_record(users, "user_id", args.user_id) is None:
        console.print("[red]User not found.[/red]")
        return

    task = find_record(tasks, "task_id", args.task_id)
    if task is None:
        console.print("[red]Task not found.[/red]")
        return

    if args.user_id not in task["assigned_to"]:
        task["assigned_to"].append(args.user_id)
        save_tasks(tasks)

    console.print("[green]Contributor assigned successfully.[/green]")


def edit_project(args):
    """Update the supplied fields of an existing project."""
    projects = load_projects()
    project = find_record(projects, "project_id", args.project_id)

    if project is None:
        console.print("[red]Project not found.[/red]")
        return

    if args.title is not None:
        project["title"] = args.title

    if args.description is not None:
        project["description"] = args.description

    if args.due_date is not None:
        if args.due_date:
            try:
                date.fromisoformat(args.due_date)
            except ValueError:
                console.print(
                    "[red]Invalid due date. Use YYYY-MM-DD.[/red]"
                )
                return

        project["due_date"] = args.due_date or None

    save_projects(projects)
    console.print("[green]Project updated successfully.[/green]")


def edit_task(args):
    """Update the title or status of an existing task."""
    tasks = load_tasks()
    task = find_record(tasks, "task_id", args.task_id)

    if task is None:
        console.print("[red]Task not found.[/red]")
        return

    if args.title is not None:
        task["title"] = args.title

    if args.status is not None:
        task["status"] = args.status

    save_tasks(tasks)
    console.print("[green]Task updated successfully.[/green]")


def build_parser():
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Python Project Management CLI"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    user_parser = commands.add_parser("add-user", help="Create a user")
    user_parser.add_argument("--name", required=True)
    user_parser.add_argument("--email", required=True)
    user_parser.set_defaults(func=add_user)

    users_parser = commands.add_parser("list-users", help="List users")
    users_parser.set_defaults(func=list_users)

    project_parser = commands.add_parser(
        "add-project", help="Create a project"
    )
    project_parser.add_argument("--user-id", type=int, required=True)
    project_parser.add_argument("--title", required=True)
    project_parser.add_argument("--description", default="")
    project_parser.add_argument("--due-date", default=None)
    project_parser.set_defaults(func=add_project)

    projects_parser = commands.add_parser(
        "list-projects", help="List projects"
    )
    projects_parser.add_argument("--user-id", type=int)
    projects_parser.set_defaults(func=list_projects)

    task_parser = commands.add_parser("add-task", help="Create a task")
    task_parser.add_argument("--project-id", type=int, required=True)
    task_parser.add_argument("--title", required=True)
    task_parser.set_defaults(func=add_task)

    tasks_parser = commands.add_parser("list-tasks", help="List project tasks")
    tasks_parser.add_argument("--project-id", type=int, required=True)
    tasks_parser.set_defaults(func=list_tasks)

    complete_parser = commands.add_parser(
        "complete-task", help="Complete a task"
    )
    complete_parser.add_argument("--task-id", type=int, required=True)
    complete_parser.set_defaults(func=complete_task)

    assign_parser = commands.add_parser(
        "assign-task", help="Assign a contributor to a task"
    )
    assign_parser.add_argument("--task-id", type=int, required=True)
    assign_parser.add_argument("--user-id", type=int, required=True)
    assign_parser.set_defaults(func=assign_task)

    edit_project_parser = commands.add_parser(
        "edit-project", help="Edit an existing project"
    )
    edit_project_parser.add_argument(
        "--project-id", type=int, required=True
    )
    edit_project_parser.add_argument("--title")
    edit_project_parser.add_argument("--description")
    edit_project_parser.add_argument("--due-date")
    edit_project_parser.set_defaults(func=edit_project)

    edit_task_parser = commands.add_parser(
        "edit-task", help="Edit an existing task"
    )
    edit_task_parser.add_argument(
        "--task-id", type=int, required=True
    )
    edit_task_parser.add_argument("--title")
    edit_task_parser.add_argument(
        "--status", choices=("pending", "in progress", "completed")
    )
    edit_task_parser.set_defaults(func=edit_task)

    return parser


def main():
    """Run the selected CLI command and handle expected data errors."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        args.func(args)
    except (OSError, ValueError) as error:
        console.print(f"[red]Error: {error}[/red]")

if __name__ == "__main__":
    main()
