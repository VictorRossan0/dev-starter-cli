import shutil
import subprocess

from utils import ask_required, ask_yes_no, get_output_dir, initialize_git_repository


def generate_laravel_project() -> None:
    """Generate a Laravel project using Composer."""
    project_name = ask_required("Nome do projeto Laravel: ")
    output_dir = get_output_dir()
    project_path = output_dir / project_name

    if shutil.which("composer") is None:
        print("Composer não encontrado no PATH.")
        print("Instale o Composer antes de criar projetos Laravel.")
        return

    command = [
        "composer",
        "create-project",
        "laravel/laravel",
        str(project_path),
    ]

    print("\nExecutando:")
    print(" ".join(command))

    try:
        subprocess.run(command, check=True)
        print("\nProjeto Laravel criado com sucesso!")
        print(project_path)
    except subprocess.CalledProcessError as error:
        print("Erro ao criar projeto Laravel.")
        print(error)
        return

    if ask_yes_no("Deseja inicializar um repositório Git neste projeto?", default=True):
        initialize_git_repository(project_path)
