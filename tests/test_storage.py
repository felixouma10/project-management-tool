import pytest

from utils import storage


def test_save_and_load_data(tmp_path, monkeypatch):
    """Verify data can be saved and restored."""
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)

    users = [
        {"user_id": 1, "name": "Felix", "email": "felix@moringa.com"}
    ]

    storage.save_users(users)

    assert storage.load_users() == users


def test_missing_file_returns_empty_list(tmp_path, monkeypatch):
    """Verify missing data files are handled."""
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)

    assert storage.load_users() == []


def test_malformed_json_raises_error(tmp_path, monkeypatch):
    """Verify malformed JSON produces a useful error."""
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    (tmp_path / "users.json").write_text("{invalid", encoding="utf-8")

    with pytest.raises(ValueError, match="invalid JSON"):
        storage.load_users()


def test_non_list_json_raises_error(tmp_path, monkeypatch):
    """Verify JSON objects are rejected when a list is expected."""
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    (tmp_path / "users.json").write_text(
        '{"name": "Felix"}', encoding="utf-8"
    )

    with pytest.raises(ValueError, match="invalid JSON"):
        storage.load_users()
