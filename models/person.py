class Person:
    """Base class representing a person."""

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        """Return a readable description of the person."""
        return f"{self.name} ({self.email})"