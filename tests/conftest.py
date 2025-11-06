import pytest
from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.models.colaborador import Colaborador
from app.models.avaliacao import Ciclo, AvaliacaoComportamental, Meta
from app.core.security import get_password_hash

# Criar banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Cria uma sessão de banco de dados para cada teste
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Cria um cliente de teste do FastAPI
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def admin_user(db_session):
    """
    Cria um usuário admin para testes
    """
    admin = Colaborador(
        matricula="admin",
        nome="Administrador Teste",
        email="admin@test.com",
        senha_hash=get_password_hash("admin123"),
        cargo="Administrador",
        departamento="TI",
        ativo=True,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture(scope="function")
def regular_user(db_session):
    """
    Cria um usuário regular para testes
    """
    user = Colaborador(
        matricula="user001",
        nome="Usuário Teste",
        email="user@test.com",
        senha_hash=get_password_hash("user123"),
        cargo="Analista",
        departamento="Tecnologia",
        gestor_matricula="admin",
        ativo=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def another_user(db_session):
    """
    Cria outro usuário para testes de relacionamento
    """
    user = Colaborador(
        matricula="user002",
        nome="Outro Usuário",
        email="outro@test.com",
        senha_hash=get_password_hash("user123"),
        cargo="Coordenador",
        departamento="Operações",
        gestor_matricula="admin",
        ativo=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def admin_token(client, admin_user):
    """
    Retorna token de autenticação do admin
    """
    response = client.post(
        "/api/auth/login", json={"matricula": "admin", "senha": "admin123"}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def user_token(client, regular_user):
    """
    Retorna token de autenticação do usuário regular
    """
    response = client.post(
        "/api/auth/login", json={"matricula": "user001", "senha": "user123"}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def ciclo_ativo(db_session):
    """
    Cria um ciclo ativo para testes
    """
    ciclo = Ciclo(
        ano=2025,
        descricao="Ciclo de Teste 2025",
        data_inicio=date(2025, 1, 1),
        data_fim=date(2025, 12, 31),
        status="em_andamento",
    )
    db_session.add(ciclo)
    db_session.commit()
    db_session.refresh(ciclo)
    return ciclo


@pytest.fixture
def avaliacao_sample(db_session, ciclo_ativo, regular_user, admin_user):
    """
    Cria uma avaliação de exemplo
    """
    avaliacao = AvaliacaoComportamental(
        ciclo_id=ciclo_ativo.id,
        avaliado_matricula=regular_user.matricula,
        avaliador_matricula=admin_user.matricula,
        tipo_avaliacao="AVALIACAO_GESTOR",
        lideranca=4,
        comunicacao=5,
        trabalho_equipe=4,
        resolucao_problemas=5,
        adaptabilidade=4,
        media_competencias=4.4,
        comentarios="Excelente desempenho",
        status="PENDENTE"
    )
    db_session.add(avaliacao)
    db_session.commit()
    db_session.refresh(avaliacao)
    return avaliacao


@pytest.fixture(scope="function")
def meta_sample(db_session, ciclo_ativo, regular_user):
    """
    Cria uma meta de exemplo para testes
    """
    meta = Meta(
        ciclo_id=ciclo_ativo.id,
        colaborador_matricula=regular_user.matricula,
        titulo="Meta de Teste",
        descricao="Descrição da meta de teste",
        peso=30,
        data_limite=date(2025, 6, 30),
        resultado_alcancado=None,
        comentarios_gestor=None,
    )
    db_session.add(meta)
    db_session.commit()
    db_session.refresh(meta)
    return meta


def get_auth_headers(token: str):
    """
    Helper para criar headers de autenticação
    """
    return {"Authorization": f"Bearer {token}"}
