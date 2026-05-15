@echo off
setlocal

echo ============================
echo  Dev Starter CLI - Build EXE
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

echo Instalando PyInstaller...
pip install pyinstaller

echo Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist dev-starter.spec del dev-starter.spec

echo Gerando executavel...
pyinstaller --onefile --name dev-starter dev_starter.py

echo.
echo ============================
echo Build finalizado.
echo Executavel em: dist\dev-starter.exe
echo ============================
echo.

pause
