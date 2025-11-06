import pytest
from fastapi import status
from tests.conftest import get_auth_headers
from datetime import date


@pytest.mark.unit
def test_list_metas(client, admin_token, meta_sample):
    """
    Testa listagem de metas
    """
    response = client.get("/api/metas/", headers=get_auth_headers(admin_token))

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1


@pytest.mark.unit
def test_get_minhas_metas(client, user_token, meta_sample):
    """
    Testa listagem de minhas metas
    """
    response = client.get("/api/metas/minhas", headers=get_auth_headers(user_token))

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1


@pytest.mark.unit
def test_get_meta_by_id(client, admin_token, meta_sample):
    """
    Testa busca de meta por ID
    """
    response = client.get(
        f"/api/metas/{meta_sample.id}", headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == meta_sample.id


@pytest.mark.unit
def test_get_meta_not_found(client, admin_token):
    """
    Testa busca de meta inexistente
    """
    response = client.get("/api/metas/9999", headers=get_auth_headers(admin_token))

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.unit
def test_create_meta(client, admin_token, ciclo_ativo, regular_user):
    """
    Testa criação de meta
    """
    new_meta = {
        "ciclo_id": ciclo_ativo.id,
        "colaborador_matricula": regular_user.matricula,
        "titulo": "Nova Meta",
        "descricao": "Descrição da nova meta",
        "peso": 40,
        "data_limite": "2025-06-30",
    }

    response = client.post(
        "/api/metas/", json=new_meta, headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["titulo"] == "Nova Meta"
    assert data["peso"] == 40


@pytest.mark.unit
def test_update_meta(client, admin_token, meta_sample):
    """
    Testa atualização de meta
    """
    update_data = {"titulo": "Meta Atualizada", "resultado_alcancado": 85.5}

    response = client.put(
        f"/api/metas/{meta_sample.id}",
        json=update_data,
        headers=get_auth_headers(admin_token),
    )

    print(f"Status Code: {response.status_code}")  # ← ADICIONAR
    print(f"Response: {response.json()}")  # ← ADICIONAR

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["titulo"] == "Meta Atualizada"
    assert data["resultado_alcancado"] == 85.5


@pytest.mark.unit
def test_delete_meta(client, admin_token, db_session, ciclo_ativo, regular_user):
    """
    Testa deleção de meta
    """
    from app.models.avaliacao import Meta

    # Criar meta para deletar
    meta = Meta(
        ciclo_id=ciclo_ativo.id,
        colaborador_matricula=regular_user.matricula,
        titulo="Meta para Deletar",
        descricao="Descrição",
        peso=20,
        data_limite=date(2025, 12, 31),
    )
    db_session.add(meta)
    db_session.commit()
    db_session.refresh(meta)

    response = client.delete(
        f"/api/metas/{meta.id}", headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_200_OK
