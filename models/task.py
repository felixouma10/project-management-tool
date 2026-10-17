class Task:
    """Represent a task belonging to a project."""

    STATUSES = ("pending", "in progress", "completed")

    def __init__(self, title, task_id, assigned_to=None):
        """Initialize a task with a title, ID, and contributors."""
        self.title = title
        self.task_id = task_id
        self._status = "pending"
        self._assigned_to = []

        if assigned_to:
            for contributor in assigned_to:
                self.assign_contributor(contributor)

    @property
    def status(self):
        """Return the current task status."""
        return self._status

    @status.setter
    def status(self, value):
        """Validate status changes."""
        if value not in self.STATUSES:
            raise ValueError(
                f"Invalid status. Choose from: {', '.join(self.STATUSES)}"
            )
        self._status = value

    @property
    def assigned_to(self):
        """Return a copy of the contributor list."""
        return self._assigned_to.copy()

    def assign_contributor(self, user_id):
        """Assign a user to this task without creating duplicates."""
        if user_id not in self._assigned_to:
            self._assigned_to.append(user_id)

    def mark_complete(self):
        """Mark the task as completed."""
        self.status = "completed"

    def __str__(self):
        """Return a readable task description."""
        return (
            f"Task {self.task_id}: {self.title} "
            f"[{self.status}]"
        )