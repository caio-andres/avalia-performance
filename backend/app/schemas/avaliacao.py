from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class StatusCiclo(str, Enum):
    PLANEJAMENTO = "planejamento"
    EM_ANDAMENTO = "em_andamento"
    FINALIZADO = "finalizado"


class StatusAvaliacao(str, Enum):
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"


class TipoAvaliacao(str, Enum):
    AUTOAVALIACAO = "autoavaliacao"
    AVALIACAO_GESTOR = "avaliacao_gestor"
    AVALIACAO_PAR = "avaliacao_par"


# Ciclo Schemas
class CicloBase(BaseModel):
    ano: int = Field(..., ge=2020, le=2100)
    descricao: Optional[str] = None
    data_inicio: date
    data_fim: date


class CicloCreate(CicloBase):
    status: StatusCiclo = StatusCiclo.PLANEJAMENTO


class CicloUpdate(BaseModel):
    descricao: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    status: Optional[str] = None


class CicloResponse(CicloBase):
    id: int
    status: StatusCiclo
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True


# Avaliação Comportamental Schemas
class AvaliacaoComportamentalBase(BaseModel):
    ciclo_id: int
    avaliado_matricula: str
    avaliador_matricula: str
    tipo_avaliacao: TipoAvaliacao

    # Competências (1-5)
    lideranca: int = Field(..., ge=1, le=5)
    comunicacao: int = Field(..., ge=1, le=5)
    trabalho_equipe: int = Field(..., ge=1, le=5)
    resolucao_problemas: int = Field(..., ge=1, le=5)
    adaptabilidade: int = Field(..., ge=1, le=5)

    comentarios: Optional[str] = None


class AvaliacaoComportamentalCreate(AvaliacaoComportamentalBase):
    pass


class AvaliacaoComportamentalUpdate(BaseModel):
    lideranca: Optional[int] = Field(None, ge=1, le=5)
    comunicacao: Optional[int] = Field(None, ge=1, le=5)
    trabalho_equipe: Optional[int] = Field(None, ge=1, le=5)
    resolucao_problemas: Optional[int] = Field(None, ge=1, le=5)
    adaptabilidade: Optional[int] = Field(None, ge=1, le=5)
    comentarios: Optional[str] = None
    status: Optional[StatusAvaliacao] = None


class AvaliacaoComportamentalResponse(AvaliacaoComportamentalBase):
    id: int
    media_competencias: Optional[float] = None
    status: StatusAvaliacao
    criado_em: datetime
    atualizado_em: datetime
    
    class Config:
        from_attributes = True


# Meta Schemas
class MetaBase(BaseModel):
    ciclo_id: int
    colaborador_matricula: str
    titulo: str
    descricao: Optional[str] = None
    peso: int
    data_limite: date
    resultado_alcancado: Optional[float] = None


class MetaCreate(MetaBase):
    pass


class MetaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    descricao: Optional[str] = None
    peso: Optional[int] = Field(None, ge=1, le=100)
    data_limite: Optional[date] = None
    resultado_alcancado: Optional[float] = None
    comentarios_gestor: Optional[str] = None


class MetaResponse(MetaBase):
    id: int
    resultado_alcancado: Optional[int] = None
    comentarios_gestor: Optional[str] = None
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True
