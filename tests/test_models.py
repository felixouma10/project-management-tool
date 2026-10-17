import pytest

from models.user import User
from models.project import Project
from models.task import Task


def test_user_can_have_multiple_projects():
    user = User("Alex", "alex@example.com", 1)
    project1 = Project("Website", 101, owner_id=1)
    project2 = Project("CLI Tool", 102, owner_id=1)

    user.add_project(project1)
    user.add_project(project2)

    assert len(user.projects) == 2


def test_project_can_have_multiple_tasks():
    project = Project("CLI Tool", 101)
    task1 = Task("Create models", 201)
    task2 = Task("Build CLI", 202)

    project.add_task(task1)
    project.add_task(task2)

    assert len(project.tasks) == 2


def test_task_can_be_completed():
    task = Task("Write tests", 201)

    task.mark_complete()

    assert task.status == "completed"


def test_task_rejects_invalid_status():
    task = Task("Write tests", 201)

    with pytest.raises(ValueError):
        task.status = "unknown"


def test_task_supports_multiple_contributors():
    task = Task("Build CLI", 201)
    task.assign_contributor(1)
    task.assign_contributor(2)
    task.assign_contributor(1)

    assert task.assigned_to == [1, 2]


def test_project_rejects_duplicate_task_ids():
    project = Project("CLI Tool", 101)
    project.add_task(Task("First task", 201))

    with pytest.raises(ValueError):
        project.add_task(Task("Duplicate task", 201))
