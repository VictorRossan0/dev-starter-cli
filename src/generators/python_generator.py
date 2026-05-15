import os
import subprocess
import sys
from pathlib import Path

from utils import ask_required, ask_yes_no, create_directory, create_files, get_output_dir, print_created_structure


PYTHON_PROJECTS = {
    "1": {
        "name": "Automação simples",
        "run_command": "python run.py",
        "docker_service": "worker",
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
        "run_command": "uvicorn app.main:app --host 0.0.0.0 --port 8000",
        "docker_service": "api",
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
        },
    },
    "3": {
        "name": "Scraping",
        "run_command": "python run.py",
        "docker_service": "scraper",
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
    "4": {
        "name": "Integração/API Worker",
        "run_command": "python run.py",
        "docker_service": "worker",
        "requirements": "python-dotenv\nrequests\nhttpx\npydantic\nloguru\n",
        "files": {
            "run.py": "from app.main import main\n\n\nif __name__ == '__main__':\n    main()\n",
            "app/__init__.py": "",
            "app/main.py": "from app.services.integration_service import IntegrationService\nfrom app.logs.logger import logger\n\n\ndef main():\n    logger.info('Worker de integração iniciado.')\n    service = IntegrationService()\n    result = service.execute()\n    logger.info(f'Resultado da execução: {result}')\n",
            "app/config.py": "import os\nfrom pathlib import Path\nfrom dotenv import load_dotenv\n\nBASE_DIR = Path(__file__).resolve().parent.parent\nload_dotenv(BASE_DIR / '.env')\n\nAPP_ENV = os.getenv('APP_ENV', 'local')\nEXTERNAL_API_BASE_URL = os.getenv('EXTERNAL_API_BASE_URL', 'https://jsonplaceholder.typicode.com')\nEXTERNAL_API_TIMEOUT = float(os.getenv('EXTERNAL_API_TIMEOUT', '10'))\n",
            "app/clients/__init__.py": "",
            "app/clients/external_api_client.py": "import httpx\n\nfrom app.config import EXTERNAL_API_BASE_URL, EXTERNAL_API_TIMEOUT\nfrom app.logs.logger import logger\n\n\nclass ExternalApiClient:\n    def __init__(self):\n        self.base_url = EXTERNAL_API_BASE_URL.rstrip('/')\n        self.timeout = EXTERNAL_API_TIMEOUT\n\n    def get_health_sample(self) -> dict:\n        url = f'{self.base_url}/todos/1'\n        logger.info(f'Consultando API externa: {url}')\n\n        try:\n            response = httpx.get(url, timeout=self.timeout)\n            response.raise_for_status()\n            return response.json()\n        except httpx.HTTPError as error:\n            logger.error(f'Erro ao consultar API externa: {error}')\n            raise\n",
            "app/services/__init__.py": "",
            "app/services/integration_service.py": "from app.clients.external_api_client import ExternalApiClient\nfrom app.logs.logger import logger\n\n\nclass IntegrationService:\n    def __init__(self):\n        self.client = ExternalApiClient()\n\n    def execute(self) -> dict:\n        logger.info('Executando fluxo de integração.')\n        data = self.client.get_health_sample()\n\n        normalized_data = {\n            'external_id': data.get('id'),\n            'title': data.get('title'),\n            'completed': data.get('completed'),\n        }\n\n        logger.info(f'Dados normalizados: {normalized_data}')\n        return normalized_data\n",
            "app/logs/__init__.py": "",
            "app/logs/logger.py": "from pathlib import Path\nfrom loguru import logger\n\nLOGS_DIR = Path(__file__).resolve().parent.parent.parent / 'logs'\nLOGS_DIR.mkdir(parents=True, exist_ok=True)\n\nlogger.add(\n    LOGS_DIR / 'app.log',\n    rotation='1 MB',\n    retention='7 days',\n    level='INFO',\n    encoding='utf-8',\n)\n",
            "app/utils/__init__.py": "",
            "logs/.gitkeep": "",
            "tests/__init__.py": "",
            "tests/test_placeholder.py": "def test_placeholder():\n    assert True\n",
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


def get_docker_files(project: dict) -> dict[str, str]:
    run_command = project["run_command"]
    service_name = project["docker_service"]
    port_block = "    ports:\n      - \"8000:8000\"\n" if service_name == "api" else ""

    return {
        "Dockerfile": f"FROM python:3.12-slim\n\nWORKDIR /app\n\nENV PYTHONDONTWRITEBYTECODE=1\nENV PYTHONUNBUFFERED=1\n\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\nCOPY . .\n\nCMD {run_command.split()}\n",
        ".dockerignore": ".venv/\n__pycache__/\n*.pyc\n.env\n.git/\n.gitignore\nlogs/*.log\n",
        "docker-compose.yml": f"services:\n  {service_name}:\n    build: .\n    container_name: {service_name}_starter\n{port_block}    env_file:\n      - .env\n    volumes:\n      - .:/app\n",
    }


def show_next_steps(project_path: Path, docker_enabled: bool = False) -> None:
    print("\nPróximos passos:")
    print(f"cd {project_path}")

    if os.name == "nt":
        print(r".venv\Scripts\activate")
    else:
        print("source .venv/bin/activate")

    print("python run.py")

    if docker_enabled:
        print("\nCom Docker:")
        print("docker compose up --build")


def generate_python_project() -> None:
    print("\nTipos de projeto Python:")
    for key, project in PYTHON_PROJECTS.items():
        print(f"{key} - {project['name']}")

    option = ask_required("\nEscolha uma opção: ")
    if option not in PYTHON_PROJECTS:
        print("Opção inválida.")
        return

    project_name = ask_required("Nome do projeto: ")
    base_path = get_output_dir() / project_name

    if base_path.exists() and not ask_yes_no("O projeto já existe. Deseja sobrescrever arquivos?", default=False):
        print("Operação cancelada.")
        return

    project = PYTHON_PROJECTS[option]
    create_directory(base_path)

    common_files = {
        ".env": "APP_ENV=local\nEXTERNAL_API_BASE_URL=https://jsonplaceholder.typicode.com\nEXTERNAL_API_TIMEOUT=10\n",
        ".env.example": "APP_ENV=local\nEXTERNAL_API_BASE_URL=https://jsonplaceholder.typicode.com\nEXTERNAL_API_TIMEOUT=10\n",
        ".gitignore": ".env\n.venv/\n__pycache__/\n*.pyc\nlogs/*.log\n",
        "requirements.txt": project["requirements"],
        "README.md": f"# {project_name}\n\nProjeto gerado com Dev Starter CLI.\n\nTipo: {project['name']}\n",
    }

    create_files(base_path, common_files)
    create_files(base_path, project["files"])

    default_docker = option in {"2", "4"}
    docker_enabled = ask_yes_no("Deseja adicionar Docker ao projeto?", default=default_docker)
    if docker_enabled:
        docker_files = get_docker_files(project)
        create_files(base_path, docker_files)
        print("\nArquivos Docker adicionados ao projeto.")

    created_files = list(common_files.keys()) + list(project["files"].keys())
    if docker_enabled:
        created_files += list(get_docker_files(project).keys())

    print_created_structure(base_path, created_files)
    print("\nProjeto Python criado com sucesso!")

    if ask_yes_no("Deseja criar ambiente virtual .venv?", default=True):
        venv_created = create_virtual_environment(base_path)

        if venv_created and ask_yes_no("Deseja instalar as dependências agora?", default=True):
            install_requirements(base_path)

        show_next_steps(base_path, docker_enabled=docker_enabled)
