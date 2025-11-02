import pytest
from fastapi import status
from tests.conftest import get_auth_headers
from datetime import date


@pytest.mark.unit
def test_list_ciclos(client, admin_token, ciclo_ativo):
    """
    Testa listagem de ciclos
    """
    response = client.get("/api/ciclos/", headers=get_auth_headers(admin_token))

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1


@pytest.mark.unit
def test_get_ciclo_ativo(client, admin_token, ciclo_ativo):
    """
    Testa busca de ciclo ativo
    """
    response = client.get("/api/ciclos/ativo", headers=get_auth_headers(admin_token))

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "em_andamento"
    assert data["ano"] == 2025


@pytest.mark.unit
def test_get_ciclo_by_id(client, admin_token, ciclo_ativo):
    """
    Testa busca de ciclo por ID
    """
    response = client.get(
        f"/api/ciclos/{ciclo_ativo.id}", headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == ciclo_ativo.id
    assert data["ano"] == ciclo_ativo.ano


@pytest.mark.unit
def test_get_ciclo_not_found(client, admin_token):
    """
    Testa busca de ciclo inexistente
    """
    response = client.get("/api/ciclos/9999", headers=get_auth_headers(admin_token))

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.unit
def test_create_ciclo(client, admin_token):
    """
    Testa criação de ciclo
    """
    new_ciclo = {
        "ano": 2026,
        "descricao": "Ciclo de Teste 2026",
        "data_inicio": "2026-01-01",
        "data_fim": "2026-12-31",
        "status": "planejamento",
    }

    response = client.post(
        "/api/ciclos/", json=new_ciclo, headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["ano"] == 2026
    assert data["status"] == "planejamento"


@pytest.mark.unit
def test_create_ciclo_duplicate_year(client, admin_token, ciclo_ativo):
    """
    Testa criação de ciclo com ano duplicado
    """
    new_ciclo = {
        "ano": ciclo_ativo.ano,
        "descricao": "Ciclo Duplicado",
        "data_inicio": "2025-01-01",
        "data_fim": "2025-12-31",
        "status": "planejamento",
    }

    response = client.post(
        "/api/ciclos/", json=new_ciclo, headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.unit
def test_update_ciclo(client, admin_token, ciclo_ativo):
    """
    Testa atualização de ciclo
    """
    update_data = {
        "descricao": "Descrição Atualizada",
        "status": "FINALIZADO"
    }

    response = client.put(
        f"/api/ciclos/{ciclo_ativo.id}",
        json=update_data,
        headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["descricao"] == "Descrição Atualizada"
    assert data["status"].upper() == "FINALIZADO"


@pytest.mark.unit
def test_delete_ciclo(client, admin_token, db_session):
    """
    Testa deleção de ciclo
    """
    from app.models.avaliacao import Ciclo

    # Criar ciclo para deletar
    ciclo = Ciclo(
        ano=2027,
        descricao="Ciclo para Deletar",
        data_inicio=date(2027, 1, 1),
        data_fim=date(2027, 12, 31),
        status="planejamento",
    )
    db_session.add(ciclo)
    db_session.commit()
    db_session.refresh(ciclo)

    response = client.delete(
        f"/api/ciclos/{ciclo.id}", headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_200_OK
