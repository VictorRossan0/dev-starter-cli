import os
import subprocess
import sys
from pathlib import Path

from utils import ask_required, ask_yes_no, create_directory, create_files, print_created_structure


PYTHON_PROJECTS = {
    "1": {
        "name": "Automação simples",
        "requirements": "python-dotenv\nrequests\npydantic\n",
        "files": {
            "run.py": "from app.main import main\n\n\nif __name__ == '__main__':\n    main()\n",
            "app/__init__.py": "",
            "app/main.py": "def main():\n    print('Automação iniciada com sucesso!')\n",
            "app/config.py": "from pathlib import Path\nfrom dotenv import load_dotenv\n\nBASE_DIR = Path(__file__).resolve().parent.parent\nload_dotenv(BASE_DIR / '.env')\n",
            "app/services/__init__.py": "",
            "tests/__init__.py": "",
        },
    },
    "2": {
        "name": "FastAPI",
        "requirements": "fastapi\nuvicorn[standard]\npython-dotenv\npydantic\nhttpx\nsqlalchemy\npsycopg2-binary\n",
        "files": {
            "run.py": "import uvicorn\n\n\nif __name__ == '__main__':\n    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)\n",
            "app/__init__.py": "",
            "app/main.py": "from fastapi import FastAPI\n\nfrom app.routes.health import router as health_router\n\napp = FastAPI(title='API Starter')\napp.include_router(health_router)\n",
            "app/config.py": "from pathlib import Path\nfrom dotenv import load_dotenv\n\nBASE_DIR = Path(__file__).resolve().parent.parent\nload_dotenv(BASE_DIR / '.env')\n",
            "app/database.py": "# Configure aqui sua conexão com banco de dados quando necessário.\n",
            "app/routes/__init__.py": "",
            "app/routes/health.py": "from fastapi import APIRouter\n\nrouter = APIRouter(prefix='/health', tags=['Health'])\n\n\n@router.get('')\ndef health_check():\n    return {'status': 'ok'}\n",
            "app/services/__init__.py": "",
            "app/schemas/__init__.py": "",
            "app/utils/__init__.py": "",
            "tests/__init__.py": "",
            "Dockerfile": "FROM python:3.12-slim\n\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n",
            "docker-compose.yml": "services:\n  api:\n    build: .\n    ports:\n      - \"8000:8000\"\n    env_file:\n      - .env\n",
        },
    },
    "3": {
        "name": "Scraping",
        "requirements": "python-dotenv\nrequests\nbeautifulsoup4\nplaywright\npandas\n",
        "files": {
            "run.py": "from app.main import main\n\n\nif __name__ == '__main__':\n    main()\n",
            "app/__init__.py": "",
            "app/main.py": "def main():\n    print('Scraping iniciado com sucesso!')\n",
            "app/config.py": "from pathlib import Path\nfrom dotenv import load_dotenv\n\nBASE_DIR = Path(__file__).resolve().parent.parent\nload_dotenv(BASE_DIR / '.env')\n",
            "app/scraper/__init__.py": "",
            "app/scraper/browser.py": "# Implemente aqui a inicialização do navegador ou parser.\n",
            "app/services/__init__.py": "",
            "app/storage/__init__.py": "",
            "data/.gitkeep": "",
            "logs/.gitkeep": "",
            "tests/__init__.py": "",
        },
    },
}


def get_venv_python_path(project_path: Path) -> Path:
    if os.name == "nt":
        return project_path / ".venv" / "Scripts" / "python.exe"

    return project_path / ".venv" / "bin" / "python"


def create_virtual_environment(project_path: Path) -> bool:
    print("\nCriando ambiente virtual .venv...")

    try:
        subprocess.run(
            [sys.executable, "-m", "venv", str(project_path / ".venv")],
            check=True,
        )
        print("Ambiente virtual criado com sucesso.")
        return True
    except subprocess.CalledProcessError as error:
        print("Erro ao criar ambiente virtual.")
        print(error)
        return False


def install_requirements(project_path: Path) -> None:
    venv_python = get_venv_python_path(project_path)
    requirements_path = project_path / "requirements.txt"

    if not venv_python.exists():
        print("Python da .venv não encontrado. Instalação cancelada.")
        return

    print("\nAtualizando pip...")
    try:
        subprocess.run(
            [str(venv_python), "-m", "pip", "install", "--upgrade", "pip"],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        print("Não foi possível atualizar o pip.")
        print(error)

    print("\nInstalando dependências do requirements.txt...")
    try:
        subprocess.run(
            [str(venv_python), "-m", "pip", "install", "-r", str(requirements_path)],
            check=True,
        )
        print("Dependências instaladas com sucesso.")
    except subprocess.CalledProcessError as error:
        print("Erro ao instalar dependências.")
        print(error)


def show_next_steps(project_path: Path) -> None:
    print("\nPróximos passos:")
    print(f"cd {project_path}")

    if os.name == "nt":
        print(r".venv\Scripts\activate")
    else:
        print("source .venv/bin/activate")

    print("python run.py")


def generate_python_project() -> None:
    print("\nTipos de projeto Python:")
    for key, project in PYTHON_PROJECTS.items():
        print(f"{key} - {project['name']}")

    option = ask_required("\nEscolha uma opção: ")
    if option not in PYTHON_PROJECTS:
        print("Opção inválida.")
        return

    project_name = ask_required("Nome do projeto: ")
    base_path = Path.cwd() / "output" / project_name

    if base_path.exists() and not ask_yes_no("O projeto já existe. Deseja sobrescrever arquivos?", default=False):
        print("Operação cancelada.")
        return

    project = PYTHON_PROJECTS[option]
    create_directory(base_path)

    common_files = {
        ".env": "APP_ENV=local\n",
        ".env.example": "APP_ENV=local\n",
        ".gitignore": ".env\n.venv/\n__pycache__/\n*.pyc\nlogs/\n",
        "requirements.txt": project["requirements"],
        "README.md": f"# {project_name}\n\nProjeto gerado com Dev Starter CLI.\n\nTipo: {project['name']}\n",
    }

    create_files(base_path, common_files)
    create_files(base_path, project["files"])

    print_created_structure(base_path, list(common_files.keys()) + list(project["files"].keys()))
    print("\nProjeto Python criado com sucesso!")

    if ask_yes_no("Deseja criar ambiente virtual .venv?", default=True):
        venv_created = create_virtual_environment(base_path)

        if venv_created and ask_yes_no("Deseja instalar as dependências agora?", default=True):
            install_requirements(base_path)

        show_next_steps(base_path)
