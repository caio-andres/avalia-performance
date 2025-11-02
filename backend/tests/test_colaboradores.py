import pytest
from fastapi import status
from tests.conftest import get_auth_headers


@pytest.mark.unit
def test_get_me(client, admin_token):
    """
    Testa endpoint GET /me
    """
    response = client.get(
        "/api/colaboradores/me", headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["matricula"] == "admin"
    assert data["nome"] == "Administrador Teste"


@pytest.mark.unit
def test_list_colaboradores(client, admin_token, regular_user, another_user):
    """
    Testa listagem de colaboradores
    """
    response = client.get("/api/colaboradores/", headers=get_auth_headers(admin_token))

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 3  # admin + regular_user + another_user


@pytest.mark.unit
def test_get_colaborador_by_matricula(client, admin_token, regular_user):
    """
    Testa busca de colaborador por matrícula
    """
    response = client.get(
        f"/api/colaboradores/{regular_user.matricula}",
        headers=get_auth_headers(admin_token),
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["matricula"] == regular_user.matricula
    assert data["nome"] == regular_user.nome


@pytest.mark.unit
def test_get_colaborador_not_found(client, admin_token):
    """
    Testa busca de colaborador inexistente
    """
    response = client.get(
        "/api/colaboradores/NOTFOUND", headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.unit
def test_create_colaborador(client, admin_token):
    """
    Testa criação de colaborador
    """
    new_colaborador = {
        "matricula": "NEW001",
        "nome": "Novo Colaborador",
        "email": "novo@test.com",
        "senha": "senha123",
        "cargo": "Analista",
        "departamento": "TI",
        "gestor_matricula": "admin",
    }

    response = client.post(
        "/api/colaboradores/",
        json=new_colaborador,
        headers=get_auth_headers(admin_token),
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["matricula"] == "NEW001"
    assert data["nome"] == "Novo Colaborador"
    assert data["ativo"] is True


@pytest.mark.unit
def test_create_colaborador_duplicate_matricula(client, admin_token, regular_user):
    """
    Testa criação de colaborador com matrícula duplicada
    """
    new_colaborador = {
        "matricula": regular_user.matricula,
        "nome": "Duplicado",
        "email": "duplicado@test.com",
        "senha": "senha123",
        "cargo": "Analista",
        "departamento": "TI",
    }

    response = client.post(
        "/api/colaboradores/",
        json=new_colaborador,
        headers=get_auth_headers(admin_token),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Matrícula já cadastrada" in response.json()["detail"]


@pytest.mark.unit
def test_create_colaborador_duplicate_email(client, admin_token, regular_user):
    """
    Testa criação de colaborador com email duplicado
    """
    new_colaborador = {
        "matricula": "NEW002",
        "nome": "Duplicado Email",
        "email": regular_user.email,
        "senha": "senha123",
        "cargo": "Analista",
        "departamento": "TI",
    }

    response = client.post(
        "/api/colaboradores/",
        json=new_colaborador,
        headers=get_auth_headers(admin_token),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email já cadastrado" in response.json()["detail"]


@pytest.mark.unit
def test_update_colaborador(client, admin_token, regular_user):
    """
    Testa atualização de colaborador
    """
    update_data = {"nome": "Nome Atualizado", "cargo": "Coordenador"}

    response = client.put(
        f"/api/colaboradores/{regular_user.matricula}",
        json=update_data,
        headers=get_auth_headers(admin_token),
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["nome"] == "Nome Atualizado"
    assert data["cargo"] == "Coordenador"


@pytest.mark.unit
def test_delete_colaborador(client, admin_token, regular_user):
    """
    Testa desativação de colaborador (soft delete)
    """
    response = client.delete(
        f"/api/colaboradores/{regular_user.matricula}",
        headers=get_auth_headers(admin_token),
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["ativo"] is False


@pytest.mark.unit
def test_delete_colaborador_already_inactive(
    client, admin_token, regular_user, db_session
):
    """
    Testa desativação de colaborador já inativo
    """
    regular_user.ativo = False
    db_session.commit()

    response = client.delete(
        f"/api/colaboradores/{regular_user.matricula}",
        headers=get_auth_headers(admin_token),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.unit
def test_get_subordinados(client, admin_token, regular_user, another_user):
    """
    Testa listagem de subordinados
    """
    response = client.get(
        "/api/colaboradores/admin/subordinados", headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2  # regular_user e another_user


@pytest.mark.unit
def test_get_gestor(client, user_token, regular_user, admin_user):
    """
    Testa busca de gestor
    """
    response = client.get(
        f"/api/colaboradores/{regular_user.matricula}/gestor",
        headers=get_auth_headers(user_token),
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["matricula"] == admin_user.matricula
