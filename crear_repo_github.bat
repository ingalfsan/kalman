@echo off
setlocal

set REPO_NAME=kalman
set GITHUB_USER=ingalfsan

echo.
echo Inicializando repositorio Git...
git init

echo.
echo Agregando archivos...
git add .

echo.
echo Creando commit inicial...
git commit -m "Initial commit: Filtro de Kalman + ejemplo CO2 Mauna Loa"

echo.
echo Configurando rama principal como 'main'...
git branch -M main

echo.
echo Conectando con repositorio remoto...
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git

echo.
echo Subiendo archivos a GitHub...
git push -u origin main

echo.
echo Listo. Repositorio disponible en: https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
pause
endlocal
