from pathlib import Path
from typing import Iterable


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
