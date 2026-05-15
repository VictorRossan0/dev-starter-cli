from generators import python_generator


def test_get_docker_files_for_fastapi_contains_expected_files():
    project = python_generator.PYTHON_PROJECTS["2"]

    docker_files = python_generator.get_docker_files(project)

    assert "Dockerfile" in docker_files
    assert "docker-compose.yml" in docker_files
    assert ".dockerignore" in docker_files
    assert "8000:8000" in docker_files["docker-compose.yml"]
    assert "uvicorn" in docker_files["Dockerfile"]


def test_generate_integration_worker_project_without_side_effects(tmp_path, monkeypatch):
    answers = iter([
        "4",  # tipo Integração/API Worker
        "worker_test",  # nome do projeto
        "s",  # adicionar Docker
        "n",  # inicializar Git
        "n",  # criar .venv
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(python_generator, "get_output_dir", lambda: tmp_path)

    python_generator.generate_python_project()

    project_path = tmp_path / "worker_test"

    assert project_path.exists()
    assert (project_path / "run.py").exists()
    assert (project_path / "app" / "main.py").exists()
    assert (project_path / "app" / "clients" / "external_api_client.py").exists()
    assert (project_path / "app" / "services" / "integration_service.py").exists()
    assert (project_path / "app" / "logs" / "logger.py").exists()
    assert (project_path / "Dockerfile").exists()
    assert (project_path / "docker-compose.yml").exists()
    assert (project_path / ".dockerignore").exists()
    assert "loguru" in (project_path / "requirements.txt").read_text(encoding="utf-8")


def test_generate_fastapi_project_without_docker_or_venv(tmp_path, monkeypatch):
    answers = iter([
        "2",  # tipo FastAPI
        "api_test",  # nome do projeto
        "n",  # adicionar Docker
        "n",  # inicializar Git
        "n",  # criar .venv
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(python_generator, "get_output_dir", lambda: tmp_path)

    python_generator.generate_python_project()

    project_path = tmp_path / "api_test"

    assert project_path.exists()
    assert (project_path / "app" / "main.py").exists()
    assert (project_path / "app" / "routes" / "health.py").exists()
    assert not (project_path / "Dockerfile").exists()
    assert "fastapi" in (project_path / "requirements.txt").read_text(encoding="utf-8")
