from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.models.colaborador import Colaborador
from app.models.avaliacao import AvaliacaoComportamental, Ciclo
from app.schemas.avaliacao import (
    AvaliacaoComportamentalCreate,
    AvaliacaoComportamentalUpdate,
    AvaliacaoComportamentalResponse,
)
from app.core.dependencies import get_current_active_user
from app.core.logging import log_info, log_error, log_warning

router = APIRouter()


@router.get("/", response_model=List[AvaliacaoComportamentalResponse])
def get_avaliacoes(
    skip: int = 0,
    limit: int = 100,
    ciclo_id: Optional[int] = None,
    avaliado_matricula: Optional[str] = None,
    avaliador_matricula: Optional[str] = None,
    status_avaliacao: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Lista todas as avaliações com filtros opcionais
    """
    log_info(
        "Listando avaliações",
        usuario=current_user.matricula,
        ciclo_id=ciclo_id,
        avaliado=avaliado_matricula,
        avaliador=avaliador_matricula,
        status=status_avaliacao,
    )

    query = db.query(AvaliacaoComportamental)

    if ciclo_id:
        query = query.filter(AvaliacaoComportamental.ciclo_id == ciclo_id)
    if avaliado_matricula:
        query = query.filter(
            AvaliacaoComportamental.avaliado_matricula == avaliado_matricula
        )
    if avaliador_matricula:
        query = query.filter(
            AvaliacaoComportamental.avaliador_matricula == avaliador_matricula
        )
    if status_avaliacao:
        query = query.filter(AvaliacaoComportamental.status == status_avaliacao)

    avaliacoes = query.offset(skip).limit(limit).all()

    log_info("Avaliações listadas", total=len(avaliacoes))

    return avaliacoes


@router.get("/minhas", response_model=List[AvaliacaoComportamentalResponse])
def get_minhas_avaliacoes(
    ciclo_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Lista as avaliações do colaborador logado (como avaliado)
    """
    log_info(
        "Buscando minhas avaliações", usuario=current_user.matricula, ciclo_id=ciclo_id
    )

    query = db.query(AvaliacaoComportamental).filter(
        AvaliacaoComportamental.avaliado_matricula == current_user.matricula
    )

    if ciclo_id:
        query = query.filter(AvaliacaoComportamental.ciclo_id == ciclo_id)

    avaliacoes = query.all()

    log_info("Minhas avaliações encontradas", total=len(avaliacoes))

    return avaliacoes


@router.get("/pendentes", response_model=List[AvaliacaoComportamentalResponse])
def get_avaliacoes_pendentes(
    ciclo_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Lista as avaliações pendentes do colaborador logado (como avaliador)
    """
    log_info(
        "Buscando avaliações pendentes",
        usuario=current_user.matricula,
        ciclo_id=ciclo_id,
    )

    query = db.query(AvaliacaoComportamental).filter(
        AvaliacaoComportamental.avaliador_matricula == current_user.matricula,
        AvaliacaoComportamental.status == "pendente",
    )

    if ciclo_id:
        query = query.filter(AvaliacaoComportamental.ciclo_id == ciclo_id)

    avaliacoes = query.all()

    log_info("Avaliações pendentes encontradas", total=len(avaliacoes))

    return avaliacoes


@router.get("/{avaliacao_id}", response_model=AvaliacaoComportamentalResponse)
def get_avaliacao(
    avaliacao_id: int,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Busca uma avaliação específica por ID
    """
    log_info(
        "Buscando avaliação por ID",
        avaliacao_id=avaliacao_id,
        usuario=current_user.matricula,
    )

    avaliacao = (
        db.query(AvaliacaoComportamental)
        .filter(AvaliacaoComportamental.id == avaliacao_id)
        .first()
    )

    if not avaliacao:
        log_warning("Avaliação não encontrada", avaliacao_id=avaliacao_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação não encontrada"
        )

    log_info("Avaliação encontrada", avaliacao_id=avaliacao.id)

    return avaliacao


@router.post(
    "/",
    response_model=AvaliacaoComportamentalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_avaliacao(
    avaliacao: AvaliacaoComportamentalCreate,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Cria uma nova avaliação comportamental
    """
    log_info(
        "Criando nova avaliação",
        avaliado=avaliacao.avaliado_matricula,
        avaliador=avaliacao.avaliador_matricula,
        ciclo_id=avaliacao.ciclo_id,
        criado_por=current_user.matricula,
    )

    # Verificar se o ciclo existe
    ciclo = db.query(Ciclo).filter(Ciclo.id == avaliacao.ciclo_id).first()
    if not ciclo:
        log_warning(
            "Tentativa de criar avaliação com ciclo inexistente",
            ciclo_id=avaliacao.ciclo_id,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ciclo não encontrado"
        )

    # Verificar se o avaliado existe
    avaliado = (
        db.query(Colaborador)
        .filter(Colaborador.matricula == avaliacao.avaliado_matricula)
        .first()
    )
    if not avaliado:
        log_warning(
            "Tentativa de criar avaliação para colaborador inexistente",
            matricula=avaliacao.avaliado_matricula,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador avaliado não encontrado",
        )

    # Verificar se o avaliador existe
    avaliador = (
        db.query(Colaborador)
        .filter(Colaborador.matricula == avaliacao.avaliador_matricula)
        .first()
    )
    if not avaliador:
        log_warning(
            "Tentativa de criar avaliação com avaliador inexistente",
            matricula=avaliacao.avaliador_matricula,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador avaliador não encontrado",
        )

    # Criar avaliação
    db_avaliacao = AvaliacaoComportamental(**avaliacao.dict())

    db.add(db_avaliacao)
    db.commit()
    db.refresh(db_avaliacao)

    log_info(
        "Avaliação criada com sucesso",
        avaliacao_id=db_avaliacao.id,
        avaliado=db_avaliacao.avaliado_matricula,
        avaliador=db_avaliacao.avaliador_matricula,
    )

    return db_avaliacao


@router.put("/{avaliacao_id}", response_model=AvaliacaoComportamentalResponse)
def update_avaliacao(
    avaliacao_id: int,
    avaliacao_update: AvaliacaoComportamentalUpdate,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Atualiza uma avaliação comportamental
    """
    log_info(
        "Atualizando avaliação",
        avaliacao_id=avaliacao_id,
        atualizado_por=current_user.matricula,
    )

    avaliacao = (
        db.query(AvaliacaoComportamental)
        .filter(AvaliacaoComportamental.id == avaliacao_id)
        .first()
    )

    if not avaliacao:
        log_warning(
            "Tentativa de atualizar avaliação inexistente", avaliacao_id=avaliacao_id
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação não encontrada"
        )

    # Atualizar campos
    update_data = avaliacao_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(avaliacao, field, value)

    db.commit()
    db.refresh(avaliacao)

    log_info("Avaliação atualizada com sucesso", avaliacao_id=avaliacao.id)

    return avaliacao


@router.delete("/{avaliacao_id}", status_code=status.HTTP_200_OK)
def delete_avaliacao(
    avaliacao_id: int,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Deleta uma avaliação comportamental
    """
    log_info(
        "Deletando avaliação",
        avaliacao_id=avaliacao_id,
        deletado_por=current_user.matricula,
    )

    avaliacao = (
        db.query(AvaliacaoComportamental)
        .filter(AvaliacaoComportamental.id == avaliacao_id)
        .first()
    )

    if not avaliacao:
        log_warning(
            "Tentativa de deletar avaliação inexistente", avaliacao_id=avaliacao_id
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação não encontrada"
        )

    db.delete(avaliacao)
    db.commit()

    log_info("Avaliação deletada com sucesso", avaliacao_id=avaliacao_id)

    return {"message": "Avaliação deletada com sucesso", "avaliacao_id": avaliacao_id}


@router.post("/{avaliacao_id}/concluir", response_model=AvaliacaoComportamentalResponse)
def concluir_avaliacao(
    avaliacao_id: int,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Marca uma avaliação como concluída
    """
    log_info(
        "Concluindo avaliação",
        avaliacao_id=avaliacao_id,
        concluido_por=current_user.matricula,
    )

    avaliacao = (
        db.query(AvaliacaoComportamental)
        .filter(AvaliacaoComportamental.id == avaliacao_id)
        .first()
    )

    if not avaliacao:
        log_warning(
            "Tentativa de concluir avaliação inexistente", avaliacao_id=avaliacao_id
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação não encontrada"
        )

    if avaliacao.status == "concluida":
        log_warning(
            "Tentativa de concluir avaliação já concluída", avaliacao_id=avaliacao_id
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avaliação já está concluída",
        )

    avaliacao.status = "concluida"
    db.commit()
    db.refresh(avaliacao)

    log_info("Avaliação concluída com sucesso", avaliacao_id=avaliacao.id)

    return avaliacao
