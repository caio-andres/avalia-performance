from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.colaborador import Colaborador
from app.models.avaliacao import Ciclo
from app.schemas.avaliacao import CicloCreate, CicloUpdate, CicloResponse
from app.core.dependencies import get_current_active_user
from app.core.logging import log_info, log_error, log_warning

router = APIRouter()


@router.get("/", response_model=List[CicloResponse])
def get_ciclos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Lista todos os ciclos de avaliação
    """
    log_info("Listando ciclos", usuario=current_user.matricula, skip=skip, limit=limit)

    ciclos = db.query(Ciclo).offset(skip).limit(limit).all()

    log_info("Ciclos listados", total=len(ciclos))

    return ciclos


@router.get("/ativo", response_model=CicloResponse)
def get_ciclo_ativo(
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Retorna o ciclo de avaliação ativo
    """
    log_info("Buscando ciclo ativo", usuario=current_user.matricula)

    ciclo = db.query(Ciclo).filter(Ciclo.status == "em_andamento").first()

    if not ciclo:
        log_warning("Nenhum ciclo ativo encontrado")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum ciclo ativo encontrado",
        )

    log_info("Ciclo ativo encontrado", ciclo_id=ciclo.id, ano=ciclo.ano)

    return ciclo


@router.get("/{ciclo_id}", response_model=CicloResponse)
def get_ciclo(
    ciclo_id: int,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Busca um ciclo específico por ID
    """
    log_info("Buscando ciclo por ID", ciclo_id=ciclo_id, usuario=current_user.matricula)

    ciclo = db.query(Ciclo).filter(Ciclo.id == ciclo_id).first()

    if not ciclo:
        log_warning("Ciclo não encontrado", ciclo_id=ciclo_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ciclo não encontrado"
        )

    log_info("Ciclo encontrado", ciclo_id=ciclo.id, ano=ciclo.ano)

    return ciclo


@router.post("/", response_model=CicloResponse, status_code=status.HTTP_201_CREATED)
def create_ciclo(
    ciclo: CicloCreate,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Cria um novo ciclo de avaliação
    """
    log_info("Criando novo ciclo", ano=ciclo.ano, criado_por=current_user.matricula)

    existing = db.query(Ciclo).filter(Ciclo.ano == ciclo.ano).first()

    if existing:
        log_warning("Tentativa de criar ciclo duplicado", ano=ciclo.ano)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Já existe um ciclo para o ano {ciclo.ano}",
        )

    db_ciclo = Ciclo(
        ano=ciclo.ano,
        descricao=ciclo.descricao,
        data_inicio=ciclo.data_inicio,
        data_fim=ciclo.data_fim,
        status=ciclo.status,
    )

    db.add(db_ciclo)
    db.commit()
    db.refresh(db_ciclo)

    log_info("Ciclo criado com sucesso", ciclo_id=db_ciclo.id, ano=db_ciclo.ano)

    return db_ciclo


@router.put("/{ciclo_id}", response_model=CicloResponse)
def update_ciclo(
    ciclo_id: int,
    ciclo_update: CicloUpdate,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Atualiza um ciclo de avaliação
    """
    log_info(
        "Atualizando ciclo", ciclo_id=ciclo_id, atualizado_por=current_user.matricula
    )

    ciclo = db.query(Ciclo).filter(Ciclo.id == ciclo_id).first()

    if not ciclo:
        log_warning("Tentativa de atualizar ciclo inexistente", ciclo_id=ciclo_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ciclo não encontrado"
        )

    update_data = ciclo_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(ciclo, field, value)

    db.commit()
    db.refresh(ciclo)

    log_info("Ciclo atualizado com sucesso", ciclo_id=ciclo.id, ano=ciclo.ano)

    return ciclo


@router.delete("/{ciclo_id}", status_code=status.HTTP_200_OK)
def delete_ciclo(
    ciclo_id: int,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Deleta um ciclo de avaliação
    """
    log_info("Deletando ciclo", ciclo_id=ciclo_id, deletado_por=current_user.matricula)

    ciclo = db.query(Ciclo).filter(Ciclo.id == ciclo_id).first()

    if not ciclo:
        log_warning("Tentativa de deletar ciclo inexistente", ciclo_id=ciclo_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ciclo não encontrado"
        )

    db.delete(ciclo)
    db.commit()

    log_info("Ciclo deletado com sucesso", ciclo_id=ciclo_id, ano=ciclo.ano)

    return {"message": "Ciclo deletado com sucesso", "ciclo_id": ciclo_id}
