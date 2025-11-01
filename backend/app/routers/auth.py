from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.database import get_db
from app.models.colaborador import Colaborador
from app.schemas.auth import Token, LoginRequest, LoginResponse
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.core.logging import log_info, log_error, log_warning

router = APIRouter()


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Endpoint OAuth2 para obter token de acesso (usado pelo Swagger UI)
    """
    log_info("Tentativa de login OAuth2", username=form_data.username)

    colaborador = (
        db.query(Colaborador)
        .filter(Colaborador.matricula == form_data.username, Colaborador.ativo == True)
        .first()
    )

    if not colaborador:
        log_warning(
            "Login falhou - colaborador não encontrado", matricula=form_data.username
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Matrícula ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, colaborador.senha_hash):
        log_warning("Login falhou - senha incorreta", matricula=form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Matrícula ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": colaborador.matricula}, expires_delta=access_token_expires
    )

    log_info(
        "Login bem-sucedido", matricula=colaborador.matricula, nome=colaborador.nome
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint de login customizado
    """
    log_info("Tentativa de login", matricula=login_data.matricula)

    colaborador = (
        db.query(Colaborador)
        .filter(
            Colaborador.matricula == login_data.matricula, Colaborador.ativo == True
        )
        .first()
    )

    if not colaborador:
        log_warning(
            "Login falhou - colaborador não encontrado", matricula=login_data.matricula
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Matrícula ou senha incorretos",
        )

    if not verify_password(login_data.senha, colaborador.senha_hash):
        log_warning("Login falhou - senha incorreta", matricula=login_data.matricula)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Matrícula ou senha incorretos",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": colaborador.matricula}, expires_delta=access_token_expires
    )

    log_info(
        "Login bem-sucedido", matricula=colaborador.matricula, nome=colaborador.nome
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "matricula": colaborador.matricula,
        "nome": colaborador.nome,
        "cargo": colaborador.cargo,
    }
