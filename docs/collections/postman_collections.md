# Postman Collection - Avalia Performance API

## Import Instructions

1. Open Postman
2. Click "Import" button
3. Copy and paste the JSON below
4. Click "Import"

---

## Collection JSON

Save this as postman_collection.json and import into Postman:

{
"info": {
"name": "Avalia Performance API",
"description": "Complete API collection for Itau Performance Evaluation System",
"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
},
"variable": [
{
"key": "base_url",
"value": "http://localhost:8000/api",
"type": "string"
},
{
"key": "token",
"value": "",
"type": "string"
}
],
"auth": {
"type": "bearer",
"bearer": [
{
"key": "token",
"value": "{{token}}",
"type": "string"
}
]
},
"item": [
{
"name": "Authentication",
"item": [
{
"name": "Login",
"request": {
"method": "POST",
"header": [],
"body": {
"mode": "raw",
"raw": "{\\n \\"matricula\\": \\"admin\\",\\n \\"senha\\": \\"admin123\\"\\n}",
"options": {
"raw": {
"language": "json"
}
}
},
"url": {
"raw": "{{base_url}}/auth/login",
"host": ["{{base_url}}"],
"path": ["auth", "login"]
}
}
}
]
},
{
"name": "Colaboradores",
"item": [
{
"name": "Get Me",
"request": {
"method": "GET",
"header": [],
"url": {
"raw": "{{base_url}}/colaboradores/me",
"host": ["{{base_url}}"],
"path": ["colaboradores", "me"]
}
}
},
{
"name": "List Colaboradores",
"request": {
"method": "GET",
"header": [],
"url": {
"raw": "{{base_url}}/colaboradores",
"host": ["{{base_url}}"],
"path": ["colaboradores"]
}
}
}
]
},
{
"name": "Ciclos",
"item": [
{
"name": "List Ciclos",
"request": {
"method": "GET",
"header": [],
"url": {
"raw": "{{base_url}}/ciclos",
"host": ["{{base_url}}"],
"path": ["ciclos"]
}
}
}
]
},
{
"name": "Avaliacoes",
"item": [
{
"name": "List Avaliacoes",
"request": {
"method": "GET",
"header": [],
"url": {
"raw": "{{base_url}}/avaliacoes",
"host": ["{{base_url}}"],
"path": ["avaliacoes"]
}
}
}
]
},
{
"name": "Metas",
"item": [
{
"name": "List Metas",
"request": {
"method": "GET",
"header": [],
"url": {
"raw": "{{base_url}}/metas",
"host": ["{{base_url}}"],
"path": ["metas"]
}
}
}
]
}
]
}

---

## Usage Instructions

### 1. Set Base URL

The collection uses a variable {{base_url}} set to http://localhost:8000/api

### 2. Authentication Flow

1. Run the Login request first
2. The token will be automatically saved to the {{token}} variable
3. All subsequent requests will use this token automatically

### 3. Testing Workflow

Step 1: Login
POST /auth/login
Body: { "matricula": "admin", "senha": "admin123" }

Step 2: Get Current User
GET /colaboradores/me

Step 3: List Colaboradores
GET /colaboradores

Step 4: Get Active Cycle
GET /ciclos/ativo

Step 5: Create Evaluation
POST /avaliacoes

Step 6: Create Goals
POST /metas

Step 7: Get Final Results
GET /resultados/{ciclo_id}/{matricula}

---

## Environment Variables

| Variable | Development               | Production                          |
| -------- | ------------------------- | ----------------------------------- |
| base_url | http://localhost:8000/api | https://api.itau.com.br/performance |
| token    | (auto-set after login)    | (auto-set after login)              |
