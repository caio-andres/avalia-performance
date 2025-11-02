import pytest
from fastapi import status


@pytest.mark.unit
def test_login_success(client, admin_user):
    """
    Testa login com credenciais válidas
    """
    response = client.post(
        "/api/auth/login", json={"matricula": "admin", "senha": "admin123"}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["matricula"] == "admin"
    assert data["nome"] == "Administrador Teste"


@pytest.mark.unit
def test_login_invalid_matricula(client, admin_user):
    """
    Testa login com matrícula inválida
    """
    response = client.post(
        "/api/auth/login", json={"matricula": "invalid", "senha": "admin123"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Matrícula ou senha incorretos" in response.json()["detail"]


@pytest.mark.unit
def test_login_invalid_password(client, admin_user):
    """
    Testa login com senha inválida
    """
    response = client.post(
        "/api/auth/login", json={"matricula": "admin", "senha": "wrongpassword"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Matrícula ou senha incorretos" in response.json()["detail"]


@pytest.mark.unit
def test_login_inactive_user(client, db_session, admin_user):
    """
    Testa login com usuário inativo
    """
    admin_user.ativo = False
    db_session.commit()

    response = client.post(
        "/api/auth/login", json={"matricula": "admin", "senha": "admin123"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.unit
def test_token_endpoint_success(client, admin_user):
    """
    Testa endpoint OAuth2 token
    """
    response = client.post(
        "/api/auth/token", data={"username": "admin", "password": "admin123"}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.unit
def test_token_endpoint_invalid_credentials(client, admin_user):
    """
    Testa endpoint OAuth2 token com credenciais inválidas
    """
    response = client.post(
        "/api/auth/token", data={"username": "admin", "password": "wrongpassword"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.unit
def test_access_protected_endpoint_without_token(client):
    """
    Testa acesso a endpoint protegido sem token
    """
    response = client.get("/api/colaboradores/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.unit
def test_access_protected_endpoint_with_invalid_token(client):
    """
    Testa acesso a endpoint protegido com token inválido
    """
    response = client.get(
        "/api/colaboradores/me", headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.unit
def test_access_protected_endpoint_with_valid_token(client, admin_token):
    """
    Testa acesso a endpoint protegido com token válido
    """
    response = client.get(
        "/api/colaboradores/me", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["matricula"] == "admin"
