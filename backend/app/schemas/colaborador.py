from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class ColaboradorBase(BaseModel):
    matricula: str = Field(..., min_length=1, max_length=50)
    nome: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    cargo: str = Field(..., min_length=1, max_length=100)
    departamento: str = Field(..., min_length=1, max_length=100)
    gestor_matricula: Optional[str] = Field(None, max_length=50)


class ColaboradorCreate(ColaboradorBase):
    senha: str = Field(..., min_length=6, max_length=100)


class ColaboradorUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    cargo: Optional[str] = Field(None, min_length=1, max_length=100)
    departamento: Optional[str] = Field(None, min_length=1, max_length=100)
    gestor_matricula: Optional[str] = Field(None, max_length=50)
    ativo: Optional[bool] = None


class ColaboradorResponse(ColaboradorBase):
    id: int
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True


class ColaboradorLogin(BaseModel):
    matricula: str
    senha: str
