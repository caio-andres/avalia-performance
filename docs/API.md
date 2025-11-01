# API Documentation - Avalia Performance

## Base URL

http://localhost:8000/api

## Authentication

All endpoints (except /auth/login and /auth/token) require JWT authentication.

### Headers

Authorization: Bearer <token>

---

## Authentication Endpoints

### POST /auth/login

Login with credentials and receive JWT token.

**Request Body:**
{
"matricula": "admin",
"senha": "admin123"
}

**Response (200 OK):**
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

**Error Responses:**

- 401 Unauthorized - Invalid credentials
- 403 Forbidden - Inactive user

---

### POST /auth/token

OAuth2 compatible token endpoint.

**Request Body (form-data):**
username: admin
password: admin123

**Response (200 OK):**
{
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
"token_type": "bearer"
}

---

## Colaboradores Endpoints

### GET /colaboradores/me

Get current authenticated user information.

### GET /colaboradores

List all employees (paginated).

**Query Parameters:**

- skip (int, default: 0) - Number of records to skip
- limit (int, default: 100) - Maximum number of records to return

### GET /colaboradores/{matricula}

Get employee by registration number.

### POST /colaboradores

Create new employee (Admin only).

### PUT /colaboradores/{matricula}

Update employee information (Admin only).

### DELETE /colaboradores/{matricula}

Soft delete employee (Admin only).

### GET /colaboradores/{matricula}/subordinados

Get employee's subordinates.

### GET /colaboradores/{matricula}/gestor

Get employee's manager.

---

## Ciclos Endpoints

### GET /ciclos

List all evaluation cycles.

### GET /ciclos/ativo

Get current active cycle.

### GET /ciclos/{ciclo_id}

Get cycle by ID.

### POST /ciclos

Create new evaluation cycle (Admin only).

### PUT /ciclos/{ciclo_id}

Update cycle (Admin only).

### DELETE /ciclos/{ciclo_id}

Delete cycle (Admin only).

---

## Avaliacoes Endpoints

### GET /avaliacoes

List all behavioral evaluations.

### GET /avaliacoes/minhas

Get evaluations for current user.

### GET /avaliacoes/pendentes

Get pending evaluations for current user (as evaluator).

### GET /avaliacoes/{avaliacao_id}

Get evaluation by ID.

### POST /avaliacoes

Create new evaluation (Manager/Admin only).

### PUT /avaliacoes/{avaliacao_id}

Update evaluation.

### POST /avaliacoes/{avaliacao_id}/concluir

Mark evaluation as completed.

### DELETE /avaliacoes/{avaliacao_id}

Delete evaluation (Admin only).

---

## Metas Endpoints

### GET /metas

List all goals.

### GET /metas/minhas

Get goals for current user.

### GET /metas/{meta_id}

Get goal by ID.

### POST /metas

Create new goal (Manager/Admin only).

### PUT /metas/{meta_id}

Update goal.

### DELETE /metas/{meta_id}

Delete goal (Admin only).

---

## Resultados Endpoints

### GET /resultados/{ciclo_id}/{matricula}

Get final evaluation results for employee in cycle.

---

## Status Codes

- 200 OK - Request successful
- 201 Created - Resource created successfully
- 400 Bad Request - Invalid request data
- 401 Unauthorized - Authentication required
- 403 Forbidden - Insufficient permissions
- 404 Not Found - Resource not found
- 422 Unprocessable Entity - Validation error
- 500 Internal Server Error - Server error

---

## User Roles

- ADMIN - Full access to all endpoints
- GESTOR - Can manage subordinates and evaluations
- COLABORADOR - Can view own data and evaluations
