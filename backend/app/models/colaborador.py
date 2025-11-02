from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


class Colaborador(Base):
    __tablename__ = "colaboradores"

    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String(50), unique=True, nullable=False, index=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    cargo = Column(String(100), nullable=False)
    departamento = Column(String(100), nullable=False)
    gestor_matricula = Column(String(50), nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint("matricula", name="uq_colaborador_matricula"),
        UniqueConstraint("email", name="uq_colaborador_email"),
    )

    # Relacionamentos
    subordinados = relationship(
        "Colaborador",
        backref="gestor",
        remote_side=[matricula],
        foreign_keys=[gestor_matricula],
        primaryjoin="Colaborador.gestor_matricula==Colaborador.matricula",
    )

    # Avaliações
    avaliacoes_recebidas = relationship(
        "AvaliacaoComportamental",
        foreign_keys="AvaliacaoComportamental.avaliado_matricula",
        back_populates="avaliado",
    )
    avaliacoes_realizadas = relationship(
        "AvaliacaoComportamental",
        foreign_keys="AvaliacaoComportamental.avaliador_matricula",
        back_populates="avaliador",
    )

    # Metas
    metas = relationship("Meta", back_populates="colaborador")
