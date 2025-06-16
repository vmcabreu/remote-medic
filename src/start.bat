@echo off
echo ========================================
echo   Docker Build Frontend y Backend
echo ========================================

echo.
echo [1/3] Construyendo imagen del Frontend...
docker build -f Dockerfile.frontend -t vue-frontend .

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker build frontend fallo
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Construyendo imagen del Backend...
docker build -f Dockerfile.backend -t py-backend .

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker build backend fallo
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [3/3] Ejecutando docker compose up...
docker compose up

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker compose up fallo
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Proceso completado exitosamente!
pause