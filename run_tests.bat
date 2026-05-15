@echo off
setlocal

echo ============================
echo  Dev Starter CLI - Tests
echo ============================
echo.

if not exist .venv (
    echo Criando ambiente virtual...
    python -m venv .venv
)

echo Ativando ambiente virtual...
call .venv\Scripts\activate

echo Atualizando pip...
python -m pip install --upgrade pip

echo Instalando dependencias de desenvolvimento...
pip install -r requirements-dev.txt

echo Executando testes...
pytest

echo.
pause
