from datetime import date


class Project:
    """Represent a project that contains multiple tasks."""

    def __init__(
        self,
        title,
        project_id,
        description="",
        due_date=None,
        owner_id=None,
    ):
        """Initialize project details and an empty task collection."""
        self.title = title
        self.project_id = project_id
        self.description = description
        self.due_date = due_date
        self.owner_id = owner_id
        self._tasks = []

    @property
    def tasks(self):
        """Return a copy of the project's tasks."""
        return self._tasks.copy()

    def add_task(self, task):
        """Add a task unless its ID already exists in this project."""
        if any(item.task_id == task.task_id for item in self._tasks):
            raise ValueError("A task with this ID already exists.")
        self._tasks.append(task)

    def find_task(self, task_id):
        """Find a task by its ID."""
        for task in self._tasks:
            if task.task_id == task_id:
                return task
        return None

    def update_details(
        self, title=None, description=None, due_date=None
    ):
        """Update supplied project details."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if due_date is not None:
            date.fromisoformat(due_date)
            self.due_date = due_date

    def __str__(self):
        """Return a readable project description."""
        return (
            f"Project {self.project_id}: {self.title} "
            f"({len(self._tasks)} tasks)"
        )