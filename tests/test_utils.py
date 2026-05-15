from pathlib import Path

import utils


def test_create_file_creates_parent_directories(tmp_path):
    target = tmp_path / "nested" / "file.txt"

    utils.create_file(target, "hello")

    assert target.exists()
    assert target.read_text(encoding="utf-8") == "hello"


def test_create_files_creates_multiple_files(tmp_path):
    files = {
        "a.txt": "A",
        "folder/b.txt": "B",
    }

    utils.create_files(tmp_path, files)

    assert (tmp_path / "a.txt").read_text(encoding="utf-8") == "A"
    assert (tmp_path / "folder" / "b.txt").read_text(encoding="utf-8") == "B"


def test_get_output_dir_uses_configured_relative_path(tmp_path, monkeypatch):
    config_path = tmp_path / "dev_starter_config.json"
    config_path.write_text('{"output_dir": "generated"}', encoding="utf-8")

    monkeypatch.setattr(utils, "get_project_root", lambda: tmp_path)

    output_dir = utils.get_output_dir()

    assert output_dir == tmp_path / "generated"
    assert output_dir.exists()


def test_get_output_dir_uses_default_when_config_is_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(utils, "get_project_root", lambda: tmp_path)

    output_dir = utils.get_output_dir()

    assert output_dir == tmp_path / "output"
    assert output_dir.exists()
