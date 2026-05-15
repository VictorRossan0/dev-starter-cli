# Dev Starter CLI

Uma CLI em Python para criar projetos de forma rápida, padronizada e com estrutura inicial profissional.

O **Dev Starter CLI** automatiza a criação de projetos Python e Laravel, reduzindo tarefas repetitivas como criação de pastas, arquivos base, ambiente virtual, dependências, Docker, configuração inicial e Git.

## Objetivo

O projeto nasceu para acelerar o início de novos projetos e manter um padrão mínimo de organização desde o primeiro commit.

Em vez de criar manualmente arquivos como `.env`, `.gitignore`, `requirements.txt`, `README.md`, estrutura de pastas, Dockerfile e ambiente virtual, a CLI guia o usuário por um menu interativo e gera tudo automaticamente.

## Funcionalidades

- Menu interativo no terminal
- Criação de projetos Python por template
- Criação de projetos Laravel via Composer
- Geração automática de estrutura de diretórios
- Criação de `.env` e `.env.example`
- Criação de `.gitignore`
- Criação de `requirements.txt`
- Criação automática de ambiente virtual `.venv`
- Instalação automática de dependências
- Docker opcional por template
- Arquivo de configuração para pasta de saída
- Inicialização opcional de repositório Git
- Build de executável com PyInstaller
- Testes automatizados com pytest

## Templates disponíveis

### Python

Atualmente a CLI permite gerar os seguintes tipos de projetos Python:

1. **Automação simples**
   - Estrutura base para scripts e automações operacionais.

2. **FastAPI**
   - Estrutura inicial para APIs com rota `/health`, documentação Swagger e suporte opcional a Docker.

3. **Scraping**
   - Estrutura para projetos de coleta de dados, scraping e manipulação de informações.

4. **Integração/API Worker**
   - Estrutura para automações de integração entre sistemas, consumo de APIs externas, normalização de dados e logs estruturados.

### Laravel

A CLI também permite criar projetos Laravel usando:

```bash
composer create-project laravel/laravel nome-do-projeto
```

## Estrutura do repositório

```text
dev-starter-cli/
├── src/
│   ├── main.py
│   ├── menu.py
│   ├── utils.py
│   └── generators/
│       ├── python_generator.py
│       └── laravel_generator.py
├── tests/
│   ├── conftest.py
│   ├── test_utils.py
│   └── test_python_generator.py
├── dev_starter.py
├── dev_starter_config.json
├── build_exe.bat
├── run_tests.bat
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## Configuração

A pasta de saída dos projetos é definida no arquivo:

```text
dev_starter_config.json
```

Configuração padrão:

```json
{
  "output_dir": "output"
}
```

Você pode alterar para outro diretório, inclusive absoluto:

```json
{
  "output_dir": "C:/Users/seu-usuario/Projetos"
}
```

## Como executar localmente

Clone o repositório:

```bash
git clone https://github.com/VictorRossan0/dev-starter-cli.git
cd dev-starter-cli
```

Execute a CLI:

```bash
python src/main.py
```

Ou execute pelo entrypoint da raiz:

```bash
python dev_starter.py
```

## Fluxo de uso

Ao executar a CLI, você verá um menu como este:

```text
============================
 Dev Starter CLI
============================
1 - Criar projeto Python
2 - Criar projeto Laravel
0 - Sair
```

Para projetos Python, a CLI pergunta:

- tipo de projeto;
- nome do projeto;
- se deseja adicionar Docker;
- se deseja inicializar Git;
- se deseja criar `.venv`;
- se deseja instalar as dependências.

## Executável Windows

O projeto possui um script para gerar executável com PyInstaller:

```powershell
.\build_exe.bat
```

O executável será criado em:

```text
dist/dev-starter.exe
```

Para executar:

```powershell
.\dist\dev-starter.exe
```

## Testes automatizados

Para rodar os testes no Windows:

```powershell
.\run_tests.bat
```

Ou manualmente:

```bash
pip install -r requirements-dev.txt
pytest
```

Os testes validam:

- criação de arquivos e diretórios;
- leitura da configuração de saída;
- geração do template FastAPI;
- geração do template Integração/API Worker;
- geração opcional de Docker;
- fluxo sem criar `.venv` real durante os testes;
- fluxo sem inicializar Git real durante os testes.

## Exemplo de projeto FastAPI gerado

```text
meu-projeto/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── routes/
│   │   └── health.py
│   ├── services/
│   ├── schemas/
│   └── utils/
├── tests/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── run.py
```

Executando localmente:

```bash
python run.py
```

Acesse:

```text
http://localhost:8000/health
http://localhost:8000/docs
```

## Exemplo de projeto Integração/API Worker gerado

```text
meu-worker/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── clients/
│   │   └── external_api_client.py
│   ├── services/
│   │   └── integration_service.py
│   ├── logs/
│   │   └── logger.py
│   └── utils/
├── logs/
├── tests/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── run.py
```

Esse template já possui:

- cliente para API externa;
- service de integração;
- normalização simples de dados;
- logs estruturados com Loguru;
- arquivo de log em `logs/app.log`.

## Docker

Quando habilitado, a CLI gera:

```text
Dockerfile
docker-compose.yml
.dockerignore
```

Execução:

```bash
docker compose up --build
```

## Roadmap

Melhorias futuras previstas:

- Template Flask
- Template Django
- Template Node.js/NestJS
- Configuração de comando de editor opcional
- Integração com GitHub CLI
- Criação automática de repositório remoto
- Mais testes automatizados
- Publicação como pacote instalável
- Interface CLI com biblioteca dedicada como Typer ou Click

## Contexto técnico

Este projeto demonstra práticas aplicadas de:

- automação de tarefas repetitivas;
- organização de projetos;
- criação de CLIs em Python;
- geração de estruturas backend;
- uso de ambiente virtual;
- Docker;
- Git;
- testes automatizados;
- empacotamento com PyInstaller.

## Autor

**Victor Rossano**

Desenvolvedor com foco em backend, automação, integrações, Python, Laravel e soluções orientadas a produtividade.
