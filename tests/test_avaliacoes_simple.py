import pytest
from fastapi import status
from tests.conftest import get_auth_headers


@pytest.mark.unit
def test_list_avaliacoes(client, admin_token, avaliacao_sample):
    """
    Testa listagem de avaliações
    """
    response = client.get("/api/avaliacoes/", headers=get_auth_headers(admin_token))

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1


@pytest.mark.unit
def test_get_minhas_avaliacoes(client, user_token, avaliacao_sample):
    """
    Testa listagem de minhas avaliações
    """
    response = client.get(
        "/api/avaliacoes/minhas", headers=get_auth_headers(user_token)
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1


@pytest.mark.unit
def test_get_avaliacoes_pendentes(client, admin_token, avaliacao_sample):
    """
    Testa listagem de avaliações pendentes
    """
    response = client.get(
        "/api/avaliacoes/pendentes", headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1


@pytest.mark.unit
def test_get_avaliacao_by_id(client, admin_token, avaliacao_sample):
    """
    Testa busca de avaliação por ID
    """
    response = client.get(
        f"/api/avaliacoes/{avaliacao_sample.id}", headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == avaliacao_sample.id


@pytest.mark.unit
def test_get_avaliacao_not_found(client, admin_token):
    """
    Testa busca de avaliação inexistente
    """
    response = client.get("/api/avaliacoes/9999", headers=get_auth_headers(admin_token))

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.unit
def test_create_avaliacao(client, admin_token, ciclo_ativo, regular_user):
    """
    Testa criação de avaliação
    """
    new_avaliacao = {
        "ciclo_id": ciclo_ativo.id,
        "avaliado_matricula": regular_user.matricula,
        "avaliador_matricula": "admin",
        "tipo_avaliacao": "avaliacao_gestor",
        "lideranca": 5,
        "comunicacao": 4,
        "trabalho_equipe": 5,
        "resolucao_problemas": 4,
        "adaptabilidade": 5,
        "comentarios": "Ótimo desempenho",
        "status": "pendente",
    }

    response = client.post(
        "/api/avaliacoes/", json=new_avaliacao, headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["avaliado_matricula"] == regular_user.matricula


@pytest.mark.unit
def test_update_avaliacao(client, admin_token, avaliacao_sample):
    """
    Testa atualização de avaliação
    """
    update_data = {"lideranca": 5, "comentarios": "Comentário atualizado"}

    response = client.put(
        f"/api/avaliacoes/{avaliacao_sample.id}",
        json=update_data,
        headers=get_auth_headers(admin_token),
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["lideranca"] == 5
    assert data["comentarios"] == "Comentário atualizado"


@pytest.mark.unit
def test_concluir_avaliacao(client, admin_token, avaliacao_sample):
    """
    Testa conclusão de avaliação
    """
    response = client.post(
        f"/api/avaliacoes/{avaliacao_sample.id}/concluir",
        headers=get_auth_headers(admin_token),
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "concluida"


@pytest.mark.unit
def test_delete_avaliacao(client, admin_token, db_session, ciclo_ativo, regular_user):
    """
    Testa deleção de avaliação
    """
    from app.models.avaliacao import AvaliacaoComportamental

    # Criar avaliação para deletar
    avaliacao = AvaliacaoComportamental(
        ciclo_id=ciclo_ativo.id,
        avaliado_matricula=regular_user.matricula,
        avaliador_matricula="admin",
        tipo_avaliacao="autoavaliacao",
        lideranca=3,
        comunicacao=3,
        trabalho_equipe=3,
        resolucao_problemas=3,
        adaptabilidade=3,
        status="pendente",
    )
    db_session.add(avaliacao)
    db_session.commit()
    db_session.refresh(avaliacao)

    response = client.delete(
        f"/api/avaliacoes/{avaliacao.id}", headers=get_auth_headers(admin_token)
    )

    assert response.status_code == status.HTTP_200_OK
