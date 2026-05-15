import json
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
