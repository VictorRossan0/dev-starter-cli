# Dev Starter CLI

CLI em Python para gerar estruturas iniciais de projetos de forma padronizada e rápida.

## Objetivo

O `dev-starter-cli` foi criado para acelerar a criação de projetos Python e Laravel, mantendo uma estrutura organizada desde o início.

A ideia é reduzir tarefas repetitivas como criação de pastas, arquivos base, `.env`, `.gitignore`, `README.md`, `requirements.txt`, Dockerfile e estruturas comuns para automações, APIs e scraping.

## Status do projeto

MVP inicial em desenvolvimento.

Nesta primeira versão, o CLI permite criar:

- Projeto Python de automação simples
- Projeto Python com FastAPI
- Projeto Python para scraping
- Projeto Laravel usando Composer

## Estrutura do projeto

```text
dev-starter-cli/
├── src/
│   ├── main.py
│   ├── menu.py
│   ├── utils.py
│   └── generators/
│       ├── python_generator.py
│       └── laravel_generator.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Como executar

Clone o repositório:

```bash
git clone https://github.com/VictorRossan0/dev-starter-cli.git
cd dev-starter-cli
```

Execute:

```bash
python src/main.py
```

## Próximas melhorias planejadas

- Criar ambiente virtual `.venv` automaticamente
- Instalar dependências automaticamente
- Adicionar Docker opcional
- Gerar projetos Flask e Django
- Criar opção para projetos de integração/API Worker
- Gerar executável com PyInstaller
- Adicionar testes automatizados

## Autor

Victor Rossano
