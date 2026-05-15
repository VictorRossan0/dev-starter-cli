import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

DEFAULT_CONFIG = {
    "output_dir": "output",
}


def get_project_root() -> Path:
    """Return project root for normal execution and PyInstaller execution."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent.parent


def get_config_path() -> Path:
    return get_project_root() / "dev_starter_config.json"


def load_config() -> dict:
    """Load CLI configuration. If missing or invalid, return defaults."""
    config_path = get_config_path()

    if not config_path.exists():
        return DEFAULT_CONFIG.copy()

    try:
        with config_path.open("r", encoding="utf-8") as file:
            config = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Não foi possível ler dev_starter_config.json. Usando configuração padrão.")
        return DEFAULT_CONFIG.copy()

    return {**DEFAULT_CONFIG, **config}


def get_output_dir() -> Path:
    config = load_config()
    output_dir = Path(config.get("output_dir", DEFAULT_CONFIG["output_dir"])).expanduser()

    if not output_dir.is_absolute():
        output_dir = get_project_root() / output_dir

    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def ask_required(prompt: str) -> str:
    """Ask for a required text input."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Valor obrigatório. Tente novamente.")


def ask_yes_no(prompt: str, default: bool = False) -> bool:
    """Ask a yes/no question."""
    suffix = "[S/n]" if default else "[s/N]"
    value = input(f"{prompt} {suffix}: ").strip().lower()

    if not value:
        return default

    return value in {"s", "sim", "y", "yes"}


def create_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def create_file(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def create_files(base_path: Path, files: dict[str, str]) -> None:
    for relative_path, content in files.items():
        create_file(base_path / relative_path, content)


def print_created_structure(base_path: Path, paths: Iterable[str]) -> None:
    print("\nEstrutura criada:")
    print(base_path)
    for path in paths:
        print(f"  - {path}")


def initialize_git_repository(project_path: Path) -> None:
    """Initialize a Git repository and create the first commit."""
    if shutil.which("git") is None:
        print("Git não encontrado no PATH. Inicialização do repositório cancelada.")
        return

    if (project_path / ".git").exists():
        print("Repositório Git já existe neste projeto.")
        return

    print("\nInicializando repositório Git...")

    commands = [
        ["git", "init"],
        ["git", "add", "."],
        ["git", "commit", "-m", "Initial commit"],
    ]

    for command in commands:
        try:
            subprocess.run(command, cwd=project_path, check=True)
        except subprocess.CalledProcessError as error:
            print(f"Erro ao executar comando: {' '.join(command)}")
            print(error)

            if command[:2] == ["git", "commit"]:
                print("Verifique se seu Git possui user.name e user.email configurados.")
                print("Exemplo:")
                print('git config --global user.name "Seu Nome"')
                print('git config --global user.email "seu-email@example.com"')

            return

    print("Repositório Git inicializado com commit inicial.")
