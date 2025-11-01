from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from typing import Optional

from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.colaborador import Colaborador

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Colaborador:
    """
    Obtém o usuário atual a partir do token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    
    if payload is None:
        raise credentials_exception
    
    matricula: str = payload.get("sub")
    if matricula is None:
        raise credentials_exception
    
    user = db.query(Colaborador).filter(
        Colaborador.matricula == matricula,
        Colaborador.ativo == True
    ).first()
    
    if user is None:
        raise credentials_exception
    
    return user


def get_current_active_user(
    current_user: Colaborador = Depends(get_current_user)
) -> Colaborador:
    """
    Verifica se o usuário está ativo
    """
    if not current_user.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    return current_user