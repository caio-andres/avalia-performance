echo "========================================="
echo "Executando Testes Unitarios"
echo "========================================="
echo ""

# ativa o ambiente virtual
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# instala as dependencias dos testes
pip install -q pytest pytest-cov pytest-asyncio httpx

# executa os testes com cobertura
pytest tests/ \
    --verbose \
    --cov=app \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=xml \
    --cov-fail-under=80

echo ""
echo "========================================="
echo "Relatório de cobertura gerado em: htmlcov/index.html"
echo "========================================="