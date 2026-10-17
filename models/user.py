from models.person import Person


class User(Person):
    """Represent a user who can manage multiple projects."""

    def __init__(self, name, email, user_id):
        super().__init__(name, email)
        self.user_id = user_id
        self._projects = []

    @property
    def projects(self):
        """Return the projects associated with this user."""
        return self._projects.copy()

    def add_project(self, project):
        """Associate a project with this user."""
        if project.project_id not in [
            item.project_id for item in self._projects
        ]:
            self._projects.append(project)

    def __str__(self):
        """Return a readable user description."""
        return f"User {self.user_id}: {self.name} - {self.email}"