from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.db.database import get_db
from models.colaborador import Colaborador, TipoUsuario
from models.avaliacao import AvaliacaoComportamental, AvaliacaoEntregas, Ciclo
from schemas.avaliacao import ResultadoFinalResponse
from routers.auth import get_current_user
from utils.logger import setup_logger

router = APIRouter(prefix="/api/resultados", tags=["Resultados"])
logger = setup_logger(__name__)


@router.get(
    "/colaborador/{colaborador_id}/ciclo/{ciclo_id}",
    response_model=ResultadoFinalResponse,
)
def obter_resultado_final(
    colaborador_id: int,
    ciclo_id: int,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_user),
):
    if current_user.who != TipoUsuario.GESTOR and current_user.id != colaborador_id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    # buscar colaborador
    colaborador = db.query(Colaborador).filter(Colaborador.id == colaborador_id).first()
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")

    # buscar ciclo
    ciclo = db.query(Ciclo).filter(Ciclo.id == ciclo_id).first()
    if not ciclo:
        raise HTTPException(status_code=404, detail="Ciclo não encontrado")

    # media comportamental
    media_comportamental = (
        db.query(func.avg(AvaliacaoComportamental.media_final))
        .filter(
            AvaliacaoComportamental.colaborador_id == colaborador_id,
            AvaliacaoComportamental.ciclo_id == ciclo_id,
        )
        .scalar()
    )

    # media entregas
    media_entregas = (
        db.query(func.avg(AvaliacaoEntregas.media_final))
        .filter(
            AvaliacaoEntregas.colaborador_id == colaborador_id,
            AvaliacaoEntregas.ciclo_id == ciclo_id,
        )
        .scalar()
    )

    if media_comportamental is None or media_entregas is None:
        raise HTTPException(
            status_code=404,
            detail="Avaliações não encontradas para este colaborador e ciclo",
        )

    # media final
    nota_final = (media_comportamental + media_entregas) / 2

    logger.info(
        f"Resultado calculado para colaborador {colaborador_id}, ciclo {ciclo_id}: {nota_final}"
    )

    return ResultadoFinalResponse(
        colaborador_id=colaborador_id,
        colaborador_nome=colaborador.nome,
        ciclo_id=ciclo_id,
        ciclo_nome=ciclo.nome,
        media_comportamental=round(media_comportamental, 2),
        media_entregas=round(media_entregas, 2),
        nota_final=round(nota_final, 2),
    )
