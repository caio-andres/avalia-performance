# Avalia Performance

Sistema backend de avaliacao de desempenho de colaboradores desenvolvido com FastAPI, SLQAlchemy e RDS (PostgreSQL).

---

## Funcionalidades

- Autenticacao JWT - Login seguro com tokens
- Gestao de Colaboradores - CRUD completo com hierarquia (gestor/subordinados)
- Ciclos de Avaliacao - Gerenciamento de periodos avaliativos
- Avaliacoes Comportamentais - Avaliacao de competencias (lideranca, comunicacao, etc.)
- Metas - Definicao e acompanhamento de objetivos
- Resultados - Calculo automatico de nota final (comportamental + metas)
- Logging Estruturado - Rastreamento de todas as operacoes
- Testes Automatizados - Cobertura de 77%+ com pytest

---

## Tecnologias

- FastAPI - Framework web moderno e rapido
- SQLAlchemy - ORM para banco de dados
- PostgreSQL - Banco de dados relacional
- Pydantic - Validacao de dados
- JWT - Autenticacao segura
- Pytest - Framework de testes
- Uvicorn - Servidor ASGI

---

## Pre-requisitos

- Python 3.12+
- PostgreSQL 13+ (ou SQLite para desenvolvimento)
- Git

---

## Instalacao

### 1. Clone o repositorio

git clone https://github.com/seu-usuario/performance.git
cd performance

### 2. Crie e ative o ambiente virtual

Windows:
python -m venv .venv
.venv\\Scripts\\activate

Linux/Mac:
python3 -m venv .venv
source .venv/bin/activate

### 3. Instale as dependencias

pip install -r requirements.txt

### 4. Configure as variaveis de ambiente

Copie o arquivo .env.example para .env:

cp .env.example .env

Edite o .env com suas configuracoes:

# Database

DATABASE_URL=sqlite:///./test.db # Para desenvolvimento

# DATABASE_URL=postgresql://user:password@localhost/dbname # Para producao

# JWT

SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application

APP_NAME=Avalia Performance
VERSION=1.0.0
DEBUG=True

### 5. Inicialize o banco de dados

python app/db/init_db.py

Isso criara as tabelas e dados iniciais:

- Admin: matricula=admin, senha=admin123
- Gestor: matricula=gestor1, senha=senha123
- Colaborador: matricula=12345, senha=senha123

---

## Executando a Aplicacao

### Modo Desenvolvimento

uvicorn app.main:app --reload

A API estara disponivel em: http://localhost:8000

### Documentacao Interativa

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Testes

### Executar todos os testes

Windows:
.\\run_tests.bat

Linux/Mac:
./run_tests.sh

### Executar testes especificos

pytest tests/test_auth.py -v
pytest tests/test_colaboradores.py -v
pytest tests/test_ciclos.py -v
pytest tests/test_avaliacoes_simple.py -v
pytest tests/test_metas.py -v

### Ver relatorio de cobertura

pytest --cov=app --cov-report=html

Abra htmlcov/index.html no navegador.

---

## Documentacao da API

Consulte a documentacao completa em:

- docs/API.md - Documentacao detalhada de todos os endpoints
- docs/collections/postman_collections.md - Collection para testes

---

## Estrutura do Projeto
```
performance/
├── app/
│ ├── core/ # Configuracoes e seguranca
│ │ ├── config.py # Configuracoes da aplicacao
│ │ ├── security.py # JWT e hashing de senhas
│ │ ├── logging.py # Logging estruturado
│ │ └── dependencies.py # Injecao de dependencias
│ ├── db/ # Banco de dados
│ │ ├── database.py # Conexao e sessao
│ │ └── init_db.py # Inicializacao e seed
│ ├── models/ # Modelos SQLAlchemy
│ │ ├── colaborador.py # Modelo de colaborador
│ │ └── avaliacao.py # Modelos de avaliacao
│ ├── schemas/ # Schemas Pydantic
│ │ ├── auth.py # Schemas de autenticacao
│ │ ├── colaborador.py # Schemas de colaborador
│ │ └── avaliacao.py # Schemas de avaliacao
│ ├── routers/ # Endpoints da API
│ │ ├── auth.py # Autenticacao
│ │ ├── colaboradores.py # Gestao de colaboradores
│ │ ├── ciclos.py # Ciclos de avaliacao
│ │ ├── avaliacoes.py # Avaliacoes comportamentais
│ │ ├── metas.py # Metas
│ │ └── resultados.py # Resultados finais
│ └── main.py # Aplicacao principal
├── tests/ # Testes automatizados
│ ├── conftest.py # Fixtures do pytest
│ ├── test_auth.py # Testes de autenticacao
│ ├── test_colaboradores.py # Testes de colaboradores
│ ├── test_ciclos.py # Testes de ciclos
│ ├── test_avaliacoes_simple.py # Testes de avaliacoes
│ └── test_metas.py # Testes de metas
├── docs/ # Documentacao
│ ├── API.md # Documentacao da API
│ └── collections/ # Collections Postman
├── .env.example # Exemplo de variaveis de ambiente
├── .gitignore # Arquivos ignorados pelo Git
├── requirements.txt # Dependencias Python
├── pytest.ini # Configuracao do pytest
├── run_tests.sh # Script de testes (Unix)
├── run_tests.bat # Script de testes (Windows)
└── README.md # Este arquivo
```

---

## Usuarios Padrao

| Matricula | Senha    | Papel       | Descricao                   |
| --------- | -------- | ----------- | --------------------------- |
| admin     | admin123 | ADMIN       | Acesso total ao sistema     |
| gestor1   | senha123 | GESTOR      | Pode gerenciar subordinados |
| 12345     | senha123 | COLABORADOR | Acesso basico               |

---

## Endpoints Principais

### Autenticacao

- POST /api/auth/login - Login
- POST /api/auth/token - Token OAuth2

### Colaboradores

- GET /api/colaboradores/me - Dados do usuario atual
- GET /api/colaboradores - Listar colaboradores
- POST /api/colaboradores - Criar colaborador (Admin)
- PUT /api/colaboradores/{matricula} - Atualizar colaborador (Admin)
- DELETE /api/colaboradores/{matricula} - Deletar colaborador (Admin)

### Ciclos

- GET /api/ciclos - Listar ciclos
- GET /api/ciclos/ativo - Ciclo ativo
- POST /api/ciclos - Criar ciclo (Admin)

### Avaliacoes

- GET /api/avaliacoes/minhas - Minhas avaliacoes
- GET /api/avaliacoes/pendentes - Avaliacoes pendentes
- POST /api/avaliacoes - Criar avaliacao (Gestor/Admin)
- POST /api/avaliacoes/{id}/concluir - Concluir avaliacao

### Metas

- GET /api/metas/minhas - Minhas metas
- POST /api/metas - Criar meta (Gestor/Admin)
- PUT /api/metas/{id} - Atualizar meta

### Resultados

- GET /api/resultados/{ciclo_id}/{matricula} - Resultado final

---

## Seguranca

- JWT Authentication - Tokens seguros com expiracao
- Password Hashing - Senhas criptografadas com bcrypt
- Role-Based Access Control - Controle de acesso por papel
- SQL Injection Protection - Uso de ORM SQLAlchemy
- CORS - Configurado para seguranca

---

## Proximos Passos

- Adicionar testes E2E
- Implementar CI/CD com GitHub Actions
- Deploy em AWS com Terraform
- Adicionar cache com Redis
- Implementar notificacoes por email
- Adicionar relatorios em PDF
- Dashboard de metricas

---

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (git checkout -b feature/AmazingFeature)
3. Commit suas mudancas (git commit -m 'feat: Add some AmazingFeature')
4. Push para a branch (git push origin feature/AmazingFeature)
5. Abra um Pull Request

---

## Convencao de Commits

Seguimos o padrao Conventional Commits:

- feat: - Nova funcionalidade
- fix: - Correcao de bug
- docs: - Documentacao
- test: - Testes
- chore: - Tarefas de manutencao
- refactor: - Refatoracao de codigo
- style: - Formatacao de codigo

---

## Licenca

Este projeto e propriedade do Itau Unibanco.

---

## Equipe

Desenvolvido pela equipe de TI do Itau Unibanco.

---

## Suporte

Para duvidas ou problemas, entre em contato com a equipe de desenvolvimento.
