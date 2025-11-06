# Documentação da API - Avalia Performance

## URL Base

http://localhost:8000/api

## Autenticação

Todos os endpoints (exceto /auth/login e /auth/token) requerem autenticação JWT.

### Cabeçalhos

Authorization: Bearer <token>

---

## Endpoints de Autenticação

### POST /auth/login

Login com credenciais e recebimento de token JWT.

**Corpo da Requisição:**
{
"matricula": "admin",
"senha": "admin123"
}

**Resposta (200 OK):**
{
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
"token_type": "bearer",
"user": {
"matricula": "admin",
"nome": "Administrador",
"email": "admin@itau.com.br",
"cargo": "Administrador",
"papel": "ADMIN"
}
}

**Respostas de Erro:**

- 401 Unauthorized - Credenciais inválidas
- 403 Forbidden - Usuário inativo

---

### POST /auth/token

Endpoint de token compatível com OAuth2.

**Corpo da Requisição (form-data):**
username: admin
password: admin123

**Resposta (200 OK):**
{
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
"token_type": "bearer"
}

---

## Endpoints de Colaboradores

### GET /colaboradores/me

Obter informações do usuário autenticado atual.

### GET /colaboradores

Listar todos os colaboradores (paginado).

**Parâmetros de Query:**

- skip (int, default: 0) - Número de registros a pular
- limit (int, default: 100) - Número máximo de registros a retornar

### GET /colaboradores/{matricula}

Obter colaborador pelo número de matrícula.

### POST /colaboradores

Criar novo colaborador (Somente Admin).

### PUT /colaboradores/{matricula}

Atualizar informações do colaborador (Somente Admin).

### DELETE /colaboradores/{matricula}

Excluir (soft delete) colaborador (Somente Admin).

### GET /colaboradores/{matricula}/subordinados

Obter subordinados do colaborador.

### GET /colaboradores/{matricula}/gestor

Obter gestor do colaborador.

---

## Endpoints de Ciclos

### GET /ciclos

Listar todos os ciclos de avaliação.

### GET /ciclos/ativo

Obter ciclo ativo atual.

### GET /ciclos/{ciclo_id}

Obter ciclo por ID.

### POST /ciclos

Criar novo ciclo de avaliação (Somente Admin).

### PUT /ciclos/{ciclo_id}

Atualizar ciclo (Somente Admin).

### DELETE /ciclos/{ciclo_id}

Excluir ciclo (Somente Admin).

---

## Endpoints de Avaliações

### GET /avaliacoes

Listar todas as avaliações de comportamento.

### GET /avaliacoes/minhas

Obter avaliações para o usuário atual.

### GET /avaliacoes/pendentes

Obter avaliações pendentes para o usuário atual (como avaliador).

### GET /avaliacoes/{avaliacao_id}

Obter avaliação por ID.

### POST /avaliacoes

Criar nova avaliação (Somente Gestor/Admin).

### PUT /avaliacoes/{avaliacao_id}

Atualizar avaliação.

### POST /avaliacoes/{avaliacao_id}/concluir

Marcar avaliação como concluída.

### DELETE /avaliacoes/{avaliacao_id}

Excluir avaliação (Somente Admin).

---

## Endpoints de Metas

### GET /metas

Listar todas as metas.

### GET /metas/minhas

Obter metas para o usuário atual.

### GET /metas/{meta_id}

Obter meta por ID.

### POST /metas

Criar nova meta (Somente Gestor/Admin).

### PUT /metas/{meta_id}

Atualizar meta.

### DELETE /metas/{meta_id}

Excluir meta (Somente Admin).

---

## Endpoints de Resultados

### GET /resultados/{ciclo_id}/{matricula}

Obter resultados finais da avaliação para o colaborador no ciclo.

---

## Códigos de Status

- 200 OK - Requisição bem-sucedida
- 201 Created - Recurso criado com sucesso
- 400 Bad Request - Dados da requisição inválidos
- 401 Unauthorized - Autenticação necessária
- 403 Forbidden - Permissões insuficientes
- 404 Not Found - Recurso não encontrado
- 422 Unprocessable Entity - Erro de validação
- 500 Internal Server Error - Erro interno do servidor

---

## Papéis de Usuário

- ADMIN - Acesso total a todos os endpoints
- GESTOR - Pode gerenciar subordinados e avaliações
- COLABORADOR - Pode visualizar seus próprios dados e avaliações