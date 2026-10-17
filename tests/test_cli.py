import json

from main import main
from utils import storage


def run_cli(monkeypatch, tmp_path, capsys, args):
    """Run a CLI command using temporary JSON storage."""
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    monkeypatch.setattr("main.load_users", storage.load_users)
    monkeypatch.setattr("main.save_users", storage.save_users)
    monkeypatch.setattr("main.load_projects", storage.load_projects)
    monkeypatch.setattr("main.save_projects", storage.save_projects)
    monkeypatch.setattr("main.load_tasks", storage.load_tasks)
    monkeypatch.setattr("main.save_tasks", storage.save_tasks)

    monkeypatch.setattr("sys.argv", ["main.py"] + args)
    main()
    return capsys.readouterr().out


def test_add_and_list_user(monkeypatch, tmp_path, capsys):
    """Verify the CLI can create and list a user."""
    run_cli(
        monkeypatch, tmp_path, capsys,
        ["add-user", "--name", "Alex", "--email", "alex@example.com"],
    )

    output = run_cli(
        monkeypatch, tmp_path, capsys, ["list-users"]
    )

    assert "Alex" in output
    assert "alex@example.com" in output


def test_add_project_and_task(monkeypatch, tmp_path, capsys):
    """Verify projects and tasks can be created through the CLI."""
    run_cli(
        monkeypatch, tmp_path, capsys,
        ["add-user", "--name", "Alex", "--email", "alex@example.com"],
    )

    run_cli(
        monkeypatch, tmp_path, capsys,
        [
            "add-project", "--user-id", "1",
            "--title", "CLI Tool",
        ],
    )

    run_cli(
        monkeypatch, tmp_path, capsys,
        [
            "add-task", "--project-id", "1",
            "--title", "Write tests",
        ],
    )

    tasks = storage.load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Write tests"
    assert tasks[0]["status"] == "pending"


def test_complete_task(monkeypatch, tmp_path, capsys):
    """Verify a task can be marked complete."""
    run_cli(
        monkeypatch, tmp_path, capsys,
        ["add-user", "--name", "Alex", "--email", "alex@example.com"],
    )
    run_cli(
        monkeypatch, tmp_path, capsys,
        ["add-project", "--user-id", "1", "--title", "CLI Tool"],
    )
    run_cli(
        monkeypatch, tmp_path, capsys,
        ["add-task", "--project-id", "1", "--title", "Write tests"],
    )

    run_cli(
        monkeypatch, tmp_path, capsys,
        ["complete-task", "--task-id", "1"],
    )

    tasks = storage.load_tasks()
    assert tasks[0]["status"] == "completed"


def test_project_requires_existing_user(monkeypatch, tmp_path, capsys):
    """Verify a project cannot be created for an unknown user."""
    output = run_cli(
        monkeypatch, tmp_path, capsys,
        ["add-project", "--user-id", "999", "--title", "Unknown"],
    )

    assert "User not found" in output
    assert storage.load_projects() == []
