# Python Project Management CLI Tool

This is a command-line application for managing users, projects, and tasks using Python, object-oriented programming, JSON persistence, and the `argparse` and `rich` libraries.

## Features

- Create and list users.
- Create projects and associate them with users.
- List all projects or filter projects by user ID.
- Create and list tasks belonging to projects.
- Assign multiple contributors to tasks.
- Mark tasks as completed.
- Persist data locally in JSON files.
- Display readable tables using Rich.
- Handle missing files and malformed JSON.
- Test models, storage, and CLI commands using pytest.

## Technologies Used

- Python 3.8.13
- argparse
- JSON and pathlib
- Rich
- pytest
- Pipenv

## Project Structure

```text
project-management-tool/
├── main.py
├── models/
│   ├── __init__.py
│   ├── person.py
│   ├── project.py
│   ├── task.py
│   └── user.py
├── utils/
│   ├── __init__.py
│   └── storage.py
├── data/
│   ├── projects.json
│   ├── tasks.json
│   └── users.json
├── tests/
│   ├── test_cli.py
│   ├── test_models.py
│   └── test_storage.py
├── Pipfile
├── Pipfile.lock
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/felixouma10/project-management-tool
cd project-management-tool
```

### 2. Set up Python

If you use pyenv and have Python 3.8.13 installed:

```bash
pyenv local 3.8.13
pipenv --python 3.8.13
```

### 3. Install dependencies

```bash
pipenv install
pipenv install --dev pytest
```

If installing from `requirements.txt` instead:

```bash
pip install -r requirements.txt
```

## Usage

Run commands from the project root using `pipenv run python main.py`.

### Add a user

```bash
pipenv run python main.py add-user \
  --name "Felix" \
  --email "felixouma3@studentmoringaschool.com"
```

### List users

```bash
pipenv run python main.py list-users
```

### Add a project

Use the ID of an existing user.

```bash
pipenv run python main.py add-project \
  --user-id 1 \
  --title "CLI Tool" \
  --description "Build a project management application" \
  --due-date 2026-12-15
```

The due date is optional and must use `YYYY-MM-DD` format.

### List projects

```bash
pipenv run python main.py list-projects
```

Filter projects by user:

```bash
pipenv run python main.py list-projects --user-id 1
```

### Add a task

Use an existing project ID.

```bash
pipenv run python main.py add-task \
  --project-id 1 \
  --title "Implement CLI"
```

### List tasks

```bash
pipenv run python main.py list-tasks --project-id 1
```

### Assign a contributor

```bash
pipenv run python main.py assign-task \
  --task-id 1 \
  --user-id 1
```

### Complete a task

```bash
pipenv run python main.py complete-task --task-id 1
```

### Display help

```bash
pipenv run python main.py --help
pipenv run python main.py add-project --help
```

## Data Persistence

The application stores records in JSON files inside the `data/` directory:

- `users.json`
- `projects.json`
- `tasks.json`

Records are loaded when commands execute and saved when data changes. The storage utility handles missing files and reports malformed JSON.

## Running Tests

Run the complete test suite:

```bash
pipenv run pytest -v
```

The current test suite covers model relationships, task status validation, JSON persistence, and core CLI operations.

## Known Limitations

- This is a local CLI application, not a networked multi-user service.
- User authentication and role-based access control are not implemented.
- Records are identified by numeric IDs; there are no delete commands.
- Data is stored locally in JSON files rather than a database.
- Editing commands support updating project details and task titles or
  statuses; deletion is not currently supported.
- Data files should not be edited while commands are running.

## Future Improvements

- Add commands to delete users, projects, and tasks.
- Add search by project title and task status.
- Improve email validation and input validation.
- Add integration tests for all CLI commands.
- Introduce a database for concurrent access and larger datasets.

## Testing Status

The current development test suite has passed all 18 tests.

## License

This project was created by Felix Ouma for educational purposes as part of a Python project management CLI assignment.
