from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import get_logger, log_info
from app.routers import auth, colaboradores, ciclos, avaliacoes, metas

# Inicializar logger
logger = get_logger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para gerenciamento de avaliações de performance de colaboradores",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(
    colaboradores.router, prefix="/api/colaboradores", tags=["Colaboradores"]
)
app.include_router(ciclos.router, prefix="/api/ciclos", tags=["Ciclos"])
app.include_router(avaliacoes.router, prefix="/api/avaliacoes", tags=["Avaliações"])
app.include_router(metas.router, prefix="/api/metas", tags=["Metas"])


@app.on_event("startup")
async def startup_event():
    """Evento executado ao iniciar a aplicação"""
    log_info(
        "Aplicação iniciada", app_name=settings.APP_NAME, version=settings.APP_VERSION
    )


@app.on_event("shutdown")
async def shutdown_event():
    """Evento executado ao encerrar a aplicação"""
    log_info("Aplicação encerrada")


@app.get("/")
def root():
    """Endpoint raiz"""
    log_info("Acesso ao endpoint raiz")
    return {
        "message": "API de Avaliação de Performance - Itaú",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
