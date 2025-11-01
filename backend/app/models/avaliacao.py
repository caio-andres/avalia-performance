from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Float,
    Text,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.database import Base


class StatusCiclo(str, enum.Enum):
    PLANEJAMENTO = "planejamento"
    EM_ANDAMENTO = "em_andamento"
    FINALIZADO = "finalizado"


class StatusAvaliacao(str, enum.Enum):
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"


class TipoAvaliacao(str, enum.Enum):
    AUTOAVALIACAO = "autoavaliacao"
    AVALIACAO_GESTOR = "avaliacao_gestor"
    AVALIACAO_PAR = "avaliacao_par"


class Ciclo(Base):
    __tablename__ = "ciclos"

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, nullable=False, unique=True, index=True)
    descricao = Column(String(500))
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    status = Column(
        SQLEnum(StatusCiclo), default=StatusCiclo.PLANEJAMENTO, nullable=False
    )
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    avaliacoes_comportamentais = relationship(
        "AvaliacaoComportamental", back_populates="ciclo"
    )
    metas = relationship("Meta", back_populates="ciclo")


class AvaliacaoComportamental(Base):
    __tablename__ = "avaliacoes_comportamentais"

    id = Column(Integer, primary_key=True, index=True)
    ciclo_id = Column(Integer, ForeignKey("ciclos.id"), nullable=False, index=True)
    avaliado_matricula = Column(
        String(50), ForeignKey("colaboradores.matricula"), nullable=False, index=True
    )
    avaliador_matricula = Column(
        String(50), ForeignKey("colaboradores.matricula"), nullable=False, index=True
    )
    tipo_avaliacao = Column(SQLEnum(TipoAvaliacao), nullable=False)

    # Competências (escala 1-5)
    lideranca = Column(Integer, nullable=False)
    comunicacao = Column(Integer, nullable=False)
    trabalho_equipe = Column(Integer, nullable=False)
    resolucao_problemas = Column(Integer, nullable=False)
    adaptabilidade = Column(Integer, nullable=False)

    # Média calculada
    media_competencias = Column(Float, nullable=True)

    comentarios = Column(Text)
    status = Column(
        SQLEnum(StatusAvaliacao), default=StatusAvaliacao.PENDENTE, nullable=False
    )

    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    ciclo = relationship("Ciclo", back_populates="avaliacoes_comportamentais")
    avaliado = relationship(
        "Colaborador",
        foreign_keys=[avaliado_matricula],
        back_populates="avaliacoes_recebidas",
    )
    avaliador = relationship(
        "Colaborador",
        foreign_keys=[avaliador_matricula],
        back_populates="avaliacoes_realizadas",
    )


class Meta(Base):
    __tablename__ = "metas"

    id = Column(Integer, primary_key=True, index=True)
    ciclo_id = Column(Integer, ForeignKey("ciclos.id"), nullable=False, index=True)
    colaborador_matricula = Column(
        String(50), ForeignKey("colaboradores.matricula"), nullable=False, index=True
    )

    titulo = Column(String(200), nullable=False)
    descricao = Column(Text)
    peso = Column(Integer, nullable=False)  # Peso da meta (1-100)
    data_limite = Column(Date, nullable=False)

    # Resultado
    resultado_alcancado = Column(Integer)  # Percentual alcançado (0-100)
    comentarios_gestor = Column(Text)

    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    ciclo = relationship("Ciclo", back_populates="metas")
    colaborador = relationship("Colaborador", back_populates="metas")
