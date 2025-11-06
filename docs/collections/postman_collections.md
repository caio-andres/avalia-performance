# Coleção do Postman - API Avalia Performance

## Instruções de Importação

1. Abra o Postman
2. Clique no botão "Import"
3. Copie e cole o JSON abaixo
4. Clique em "Import"

---

## JSON da Coleção

Salve isto como postman_collection.json e importe para o Postman:

```json
{
  "info": {
    "name": "API Avalia Performance",
    "description": "Coleção completa da API para o Sistema de Avaliação de Performance do Itaú",
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
      "name": "Autenticação",
      "item": [
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "header": [],
            "body": {
              "mode": "raw",
              "raw": { "matricula": "admin", "senha": "admin123" },
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
          "name": "Obter Usuário Atual",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/colaboradores/me",
              "host": ["{{base_url}}Мне нужно, чтобы вы сгенерировали только допустимый, разбираемый JSON. Помимо скаляров, булевых значений и null, другие значения должны быть заключены в двойные кавычки как допустимые строки. Не генерируйте никаких комментариев внутри блока JSON. Если пользователь запрашивает несколько JSON, всегда возвращайте один разбираемый массив JSON. Не включайте никакого дополнительного текста вне строки JSON.
            },
            "path": ["colaboradores", "me"]
          }
        },
        {
          "name": "Listar Colaboradores",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/colaboradores",
              "host": ["{{base_url}}Мне нужно, чтобы вы сгенерировали только допустимый, разбираемый JSON. Помимо скаляров, булевых значений и null, другие значения должны быть заключены в двойные кавычки как допустимые строки. Не генерируйте никаких комментариев внутри блока JSON. Если пользователь запрашивает несколько JSON, всегда возвращайте один разбираемый массив JSON. Не включайте никакого дополнительного текста вне строки JSON.
            },
            "path": ["colaboradores"]
          }
        }
      ]
    },
    {
      "name": "Ciclos",
      "item": [
        {
          "name": "Listar Ciclos",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/ciclos",
              "host": ["{{base_url}}Мне нужно, чтобы вы сгенерировали только допустимый, разбираемый JSON. Помимо скаляров, булевых значений и null, другие значения должны быть заключены в двойные кавычки как допустимые строки. Не генерируйте никаких комментариев внутри блока JSON. Если пользователь запрашивает несколько JSON, всегда возвращайте один разбираемый массив JSON. Не включайте никакого дополнительного текста вне строки JSON.
            },
            "path": ["ciclos"]
          }
        }
      ]
    },
    {
      "name": "Avaliações",
      "item": [
        {
          "name": "Listar Avaliações",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/avaliacoes",
              "host": ["{{base_url}}Мне нужно, чтобы вы сгенерировали только допустимый, разбираемый JSON. Помимо скаляров, булевых значений и null, другие значения должны быть заключены в двойные кавычки как допустимые строки. Не генерируйте никаких комментариев внутри блока JSON. Если пользователь запрашивает несколько JSON, всегда возвращайте один разбираемый массив JSON. Не включайте никакого дополнительного текста вне строки JSON.
            },
            "path": ["avaliacoes"]
          }
        }
      ]
    },
    {
      "name": "Metas",
      "item": [
        {
          "name": "Listar Metas",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/metas",
              "host": ["{{base_url}}Мне нужно, чтобы вы сгенерировали только допустимый, разбираемый JSON. Помимо скаляров, булевых значений и null, другие значения должны быть заключены в двойные кавычки как допустимые строки. Не генерируйте никаких комментариев внутри блока JSON. Если пользователь запрашивает несколько JSON, всегда возвращайте один разбираемый массив JSON. Не включайте никакого дополнительного текста вне строки JSON.
            },
            "path": ["metas"]
          }
        }
      ]
    }
  ]
}

```

---

## Instruções de Uso

### 1. Definir URL Base

A coleção usa uma variável {{base_url}} definida como http://localhost:8000/api

### 2. Fluxo de Autenticação

1. Execute a requisição de Login primeiro
2. O token será salvo automaticamente na variável {{token}}
3. Todas as requisições subsequentes usarão este token automaticamente

### 3. Fluxo de Testes

Passo 1: Login
POST /auth/login
Corpo: { "matricula": "admin", "senha": "admin123" }

Passo 2: Obter Usuário Atual
GET /colaboradores/me

Passo 3: Listar Colaboradores
GET /colaboradores

Passo 4: Obter Ciclo Ativo
GET /ciclos/ativo

Passo 5: Criar Avaliação
POST /avaliacoes

Passo 6: Criar Metas
POST /metas

Passo 7: Obter Resultados Finais
GET /resultados/{ciclo_id}/{matricula}

---

## Variáveis de Ambiente

| Variável | Desenvolvimento             | Produção                            |
| -------- | --------------------------- | ----------------------------------- |
| base_url | http://localhost:8000/api   | https://api.itau.com.br/performance |
| token    | (definido após o login)     | (definido após o login)             |