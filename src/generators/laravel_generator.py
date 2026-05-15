import shutil
import subprocess

from utils import ask_required, get_output_dir


def generate_laravel_project() -> None:
    """Generate a Laravel project using Composer."""
    project_name = ask_required("Nome do projeto Laravel: ")
    output_dir = get_output_dir()

    if shutil.which("composer") is None:
        print("Composer não encontrado no PATH.")
        print("Instale o Composer antes de criar projetos Laravel.")
        return

    command = [
        "composer",
        "create-project",
        "laravel/laravel",
        str(output_dir / project_name),
    ]

    print("\nExecutando:")
    print(" ".join(command))

    try:
        subprocess.run(command, check=True)
        print("\nProjeto Laravel criado com sucesso!")
        print(output_dir / project_name)
    except subprocess.CalledProcessError as error:
        print("Erro ao criar projeto Laravel.")
        print(error)
