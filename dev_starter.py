import sys
from pathlib import Path


def configure_import_paths() -> None:
    """Configure import paths for normal execution and PyInstaller execution."""
    if getattr(sys, "frozen", False):
        base_dir = Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    else:
        base_dir = Path(__file__).resolve().parent

    src_dir = base_dir / "src"

    for path in (base_dir, src_dir):
        path_str = str(path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)


configure_import_paths()

from menu import show_main_menu


if __name__ == "__main__":
    show_main_menu()
