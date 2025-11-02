from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.colaborador import Colaborador
from app.schemas.colaborador import (
    ColaboradorCreate,
    ColaboradorUpdate,
    ColaboradorResponse,
)
from app.core.dependencies import get_current_active_user
from app.core.security import get_password_hash
from app.core.logging import log_info, log_error, log_warning

router = APIRouter()


@router.get("/me", response_model=ColaboradorResponse)
def get_me(current_user: Colaborador = Depends(get_current_active_user)):
    """
    Retorna os dados do colaborador logado
    """
    log_info("Buscando dados do usuário logado", matricula=current_user.matricula)
    return current_user


@router.get("/", response_model=List[ColaboradorResponse])
def get_colaboradores(
    skip: int = 0,
    limit: int = 100,
    incluir_inativos: bool = False,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Lista todos os colaboradores
    """
    log_info(
        "Listando colaboradores",
        usuario=current_user.matricula,
        skip=skip,
        limit=limit,
        incluir_inativos=incluir_inativos,
    )

    query = db.query(Colaborador)

    if not incluir_inativos:
        query = query.filter(Colaborador.ativo == True)

    colaboradores = query.offset(skip).limit(limit).all()

    log_info("Colaboradores listados", total=len(colaboradores))

    return colaboradores


@router.get("/{matricula}", response_model=ColaboradorResponse)
def get_colaborador(
    matricula: str,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Busca um colaborador específico por matrícula
    """
    log_info(
        "Buscando colaborador por matrícula",
        matricula=matricula,
        usuario=current_user.matricula,
    )

    colaborador = (
        db.query(Colaborador).filter(Colaborador.matricula == matricula).first()
    )

    if not colaborador:
        log_warning("Colaborador não encontrado", matricula=matricula)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado"
        )

    log_info(
        "Colaborador encontrado", matricula=colaborador.matricula, nome=colaborador.nome
    )

    return colaborador


@router.post(
    "/", response_model=ColaboradorResponse, status_code=status.HTTP_201_CREATED
)
def create_colaborador(
    colaborador: ColaboradorCreate,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Cria um novo colaborador
    """
    log_info(
        "Criando novo colaborador",
        matricula=colaborador.matricula,
        criado_por=current_user.matricula,
    )

    existing = (
        db.query(Colaborador)
        .filter(Colaborador.matricula == colaborador.matricula)
        .first()
    )

    if existing:
        log_warning(
            "Tentativa de criar colaborador com matrícula duplicada",
            matricula=colaborador.matricula,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Matrícula já cadastrada"
        )

    existing_email = (
        db.query(Colaborador).filter(Colaborador.email == colaborador.email).first()
    )

    if existing_email:
        log_warning(
            "Tentativa de criar colaborador com email duplicado",
            email=colaborador.email,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado"
        )

    # Criar colaborador
    db_colaborador = Colaborador(
        matricula=colaborador.matricula,
        nome=colaborador.nome,
        email=colaborador.email,
        senha_hash=get_password_hash(colaborador.senha),
        cargo=colaborador.cargo,
        departamento=colaborador.departamento,
        gestor_matricula=colaborador.gestor_matricula,
        ativo=True,
    )

    db.add(db_colaborador)
    db.commit()
    db.refresh(db_colaborador)

    log_info(
        "Colaborador criado com sucesso",
        matricula=db_colaborador.matricula,
        nome=db_colaborador.nome,
    )

    return db_colaborador


@router.put("/{matricula}", response_model=ColaboradorResponse)
def update_colaborador(
    matricula: str,
    colaborador_update: ColaboradorUpdate,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Atualiza os dados de um colaborador
    """
    log_info(
        "Atualizando colaborador",
        matricula=matricula,
        atualizado_por=current_user.matricula,
    )

    colaborador = (
        db.query(Colaborador).filter(Colaborador.matricula == matricula).first()
    )

    if not colaborador:
        log_warning(
            "Tentativa de atualizar colaborador inexistente", matricula=matricula
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado"
        )

    update_data = colaborador_update.dict(exclude_unset=True)

    # se a senha foi fornecida, faz hash
    if "senha" in update_data and update_data["senha"]:
        update_data["senha_hash"] = get_password_hash(update_data.pop("senha"))

    for field, value in update_data.items():
        setattr(colaborador, field, value)

    db.commit()
    db.refresh(colaborador)

    log_info(
        "Colaborador atualizado com sucesso",
        matricula=colaborador.matricula,
        nome=colaborador.nome,
    )

    return colaborador


@router.delete("/{matricula}", status_code=status.HTTP_200_OK)
def delete_colaborador(
    matricula: str,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Desativa um colaborador (soft delete)
    """
    log_info(
        "Desativando colaborador",
        matricula=matricula,
        desativado_por=current_user.matricula,
    )

    colaborador = (
        db.query(Colaborador).filter(Colaborador.matricula == matricula).first()
    )

    if not colaborador:
        log_warning(
            "Tentativa de desativar colaborador inexistente", matricula=matricula
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado"
        )

    if not colaborador.ativo:
        log_warning(
            "Tentativa de desativar colaborador já inativo", matricula=matricula
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Colaborador já está inativo",
        )

    # total delete
    # db.delete(colaborador)
    # db.commit()

    # soft delete
    colaborador.ativo = False
    db.commit()
    db.refresh(colaborador)

    log_info(
        "Colaborador desativado com sucesso",
        matricula=colaborador.matricula,
        nome=colaborador.nome,
    )

    return {
        "message": "Colaborador desativado com sucesso",
        "matricula": colaborador.matricula,
        "nome": colaborador.nome,
        "ativo": colaborador.ativo,
    }


@router.get("/{matricula}/subordinados", response_model=List[ColaboradorResponse])
def get_subordinados(
    matricula: str,
    incluir_inativos: bool = False,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Lista os subordinados de um gestor

    - **matricula**: Matrícula do gestor
    - **incluir_inativos**: Se True, inclui colaboradores inativos (padrão: False)
    """
    # verificar se o gestor existe
    gestor = db.query(Colaborador).filter(Colaborador.matricula == matricula).first()

    if not gestor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gestor não encontrado"
        )

    # buscar subordinados
    query = db.query(Colaborador).filter(Colaborador.gestor_matricula == matricula)

    if not incluir_inativos:
        query = query.filter(Colaborador.ativo == True)

    subordinados = query.all()

    return subordinados


@router.get("/{matricula}/gestor", response_model=ColaboradorResponse)
def get_gestor(
    matricula: str,
    db: Session = Depends(get_db),
    current_user: Colaborador = Depends(get_current_active_user),
):
    """
    Retorna o gestor de um colaborador

    - **matricula**: Matrícula do colaborador
    """
    colaborador = (
        db.query(Colaborador).filter(Colaborador.matricula == matricula).first()
    )

    if not colaborador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado"
        )

    if not colaborador.gestor_matricula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não possui gestor cadastrado",
        )

    gestor = (
        db.query(Colaborador)
        .filter(Colaborador.matricula == colaborador.gestor_matricula)
        .first()
    )

    if not gestor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gestor não encontrado no sistema",
        )

    return gestor
