import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def save_data(filename, data):
    """Save a list of dictionaries to a JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / filename

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return file_path


def load_data(filename):
    """Load a JSON list, returning an empty list if missing or invalid."""
    file_path = DATA_DIR / filename

    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Expected a JSON list.")

        return data

    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(
            f"Cannot load {filename}: invalid JSON data."
        ) from error


def save_users(users):
    """Save user records."""
    return save_data("users.json", users)


def load_users():
    """Load user records."""
    return load_data("users.json")


def save_projects(projects):
    """Save project records."""
    return save_data("projects.json", projects)


def load_projects():
    """Load project records."""
    return load_data("projects.json")


def save_tasks(tasks):
    """Save task records."""
    return save_data("tasks.json", tasks)


def load_tasks():
    """Load task records."""
    return load_data("tasks.json")
