from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.models.colaborador import Colaborador
from app.models.avaliacao import Meta, Ciclo
from app.schemas.avaliacao import MetaCreate, MetaUpdate, MetaResponse
from app.core.dependencies import get_current_active_user
from app.core.logging import log_info, log_error, log_warning

router = APIRouter()


@router.get("/", response_model=List[MetaResponse])
def get_metas(
    skip: int = 0,
    limit: int = 100,
    ciclo_id: Optional[int] = None,
    colaborador_matricula: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Lista todas as metas com filtros opcionais
    """
    log_info(
        "Listando metas",
        usuario=current_user.matricula,
        ciclo_id=ciclo_id,
        colaborador=colaborador_matricula,
    )

    query = db.query(Meta)

    if ciclo_id:
        query = query.filter(Meta.ciclo_id == ciclo_id)
    if colaborador_matricula:
        query = query.filter(Meta.colaborador_matricula == colaborador_matricula)

    metas = query.offset(skip).limit(limit).all()

    log_info("Metas listadas", total=len(metas))

    return metas


@router.get("/minhas", response_model=List[MetaResponse])
def get_minhas_metas(
    ciclo_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Lista as metas do colaborador logado
    """
    log_info("Buscando minhas metas", usuario=current_user.matricula, ciclo_id=ciclo_id)

    query = db.query(Meta).filter(Meta.colaborador_matricula == current_user.matricula)

    if ciclo_id:
        query = query.filter(Meta.ciclo_id == ciclo_id)

    metas = query.all()

    log_info("Minhas metas encontradas", total=len(metas))

    return metas


@router.get("/{meta_id}", response_model=MetaResponse)
def get_meta(
    meta_id: int,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Busca uma meta específica por ID
    """
    log_info("Buscando meta por ID", meta_id=meta_id, usuario=current_user.matricula)

    meta = db.query(Meta).filter(Meta.id == meta_id).first()

    if not meta:
        log_warning("Meta não encontrada", meta_id=meta_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Meta não encontrada"
        )

    log_info("Meta encontrada", meta_id=meta.id, titulo=meta.titulo)

    return meta


@router.post("/", response_model=MetaResponse, status_code=status.HTTP_201_CREATED)
def create_meta(
    meta: MetaCreate,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Cria uma nova meta
    """
    log_info(
        "Criando nova meta",
        colaborador=meta.colaborador_matricula,
        ciclo_id=meta.ciclo_id,
        titulo=meta.titulo,
        criado_por=current_user.matricula,
    )

    ciclo = db.query(Ciclo).filter(Ciclo.id == meta.ciclo_id).first()
    if not ciclo:
        log_warning(
            "Tentativa de criar meta com ciclo inexistente", ciclo_id=meta.ciclo_id
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ciclo não encontrado"
        )

    colaborador = (
        db.query(Colaborador)
        .filter(Colaborador.matricula == meta.colaborador_matricula)
        .first()
    )
    if not colaborador:
        log_warning(
            "Tentativa de criar meta para colaborador inexistente",
            matricula=meta.colaborador_matricula,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado"
        )

    db_meta = Meta(**meta.dict())

    db.add(db_meta)
    db.commit()
    db.refresh(db_meta)

    log_info(
        "Meta criada com sucesso",
        meta_id=db_meta.id,
        colaborador=db_meta.colaborador_matricula,
        titulo=db_meta.titulo,
    )

    return db_meta


@router.put("/{meta_id}", response_model=MetaResponse)
def update_meta(
    meta_id: int,
    meta_update: MetaUpdate,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Atualiza uma meta
    """
    log_info("Atualizando meta", meta_id=meta_id, atualizado_por=current_user.matricula)

    meta = db.query(Meta).filter(Meta.id == meta_id).first()

    if not meta:
        log_warning("Tentativa de atualizar meta inexistente", meta_id=meta_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Meta não encontrada"
        )

    update_data = meta_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(meta, field, value)

    db.commit()
    db.refresh(meta)

    log_info("Meta atualizada com sucesso", meta_id=meta.id, titulo=meta.titulo)

    return meta


@router.delete("/{meta_id}", status_code=status.HTTP_200_OK)
def delete_meta(
    meta_id: int,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Deleta uma meta
    """
    log_info("Deletando meta", meta_id=meta_id, deletado_por=current_user.matricula)

    meta = db.query(Meta).filter(Meta.id == meta_id).first()

    if not meta:
        log_warning("Tentativa de deletar meta inexistente", meta_id=meta_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Meta não encontrada"
        )

    db.delete(meta)
    db.commit()

    log_info("Meta deletada com sucesso", meta_id=meta_id, titulo=meta.titulo)

    return {"message": "Meta deletada com sucesso", "meta_id": meta_id}
