@echo off
echo =========================================
echo Executando Testes Unitarios - Performance
echo =========================================
echo.

REM ativa o ambiente virtual
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM instala as dependencias dos testes
pip install -q pytest pytest-cov pytest-asyncio httpx

REM executa os testes com cobertura
pytest tests/ --verbose --cov=app --cov-report=html --cov-report=term-missing --cov-report=xml --cov-fail-under=80

echo.
echo =========================================
echo Relatorio de cobertura gerado em: htmlcov\index.html
echo =========================================
pause