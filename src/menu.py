from src.generators.laravel_generator import generate_laravel_project
from src.generators.python_generator import generate_python_project


def show_main_menu() -> None:
    while True:
        print("\n============================")
        print(" Dev Starter CLI")
        print("============================")
        print("1 - Criar projeto Python")
        print("2 - Criar projeto Laravel")
        print("0 - Sair")

        option = input("\nEscolha uma opção: ").strip()

        if option == "1":
            generate_python_project()
        elif option == "2":
            generate_laravel_project()
        elif option == "0":
            print("Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")
