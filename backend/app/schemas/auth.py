from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    matricula: Optional[str] = None


class LoginRequest(BaseModel):
    matricula: str
    senha: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    matricula: str
    nome: str
    cargo: str
