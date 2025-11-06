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
- AWS - RDS (em PostgreSQL)
- Pydantic - Validacao de dados
- JWT - Autenticacao segura
- Pytest - Framework de testes
- Uvicorn - Servidor ASGI

---

## Pre-requisitos

Para rodar este projeto, voce precisara ter instalado:

- **Python 3.12+**: Recomendamos usar a versao mais recente do Python 3.12. Voce pode baixa-lo em [python.org](https://www.python.org/downloads/).
- **PostgreSQL 13+**: Para o banco de dados de producao. Para desenvolvimento, SQLite pode ser usado (configurado no `.env.example`).
- **Git**: Para clonar o repositorio.
- **Conta AWS (opcional)**: Se for utilizar o AWS RDS para o banco de dados.

---

## Instalacao

Siga os passos abaixo para configurar o ambiente de desenvolvimento:

### 1. Clone o repositorio

Abra seu terminal ou prompt de comando e execute:

```bash
git clone https://github.com/caio-andres/avalia-performance.git
cd avalia-performance
```

### 2. Crie e ative o ambiente virtual

E altamente recomendado usar um ambiente virtual para isolar as dependencias do projeto.

**No Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**No Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependencias

Com o ambiente virtual ativado, instale todas as dependencias necessarias usando `pip`:

```bash
pip install -r requirements.txt
```

### 4. Configure as variaveis de ambiente

Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env` na raiz do projeto:

```bash
cp .env.example .env
```

Em seguida, edite o arquivo `.env` com suas configuracoes. As variaveis mais importantes sao:

```ini
# Database Configuration
DATABASE_URL=sqlite:///./test.db # Para desenvolvimento local com SQLite
# Ou para PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/dbname
# Ou para AWS RDS:
# DATABASE_URL=postgresql://{user}:{senha}@your-rds-endpoint.region.rds.amazonaws.com:5432/{seu_app}

# JWT Configuration
SECRET_KEY="sua_chave_secreta_aqui" # Gerar uma string aleatoria e segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
APP_NAME="Avalia Performance"
APP_VERSION="1.0.0"
DEBUG=True # Mudar para False em producao

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000 # Ajuste conforme necessario

# AWS (se aplicavel)
AWS_REGION=""
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""

# Log
LOG_LEVEL=INFO
```

**Importante:** Para `SECRET_KEY`, gere uma string longa e aleatoria. Voce pode usar `openssl rand -hex 32` no Linux/macOS ou um gerador online.

### 5. Inicialize o banco de dados

Este passo criara as tabelas no banco de dados e populara com alguns dados iniciais (usuarios padrao):

```bash
python -m app.db.init_db
```

Usuarios padrao criados:

- **Admin**: `matricula=admin`, `senha=admin123`
- **Gestor**: `matricula=gestor1`, `senha=senha123`
- **Colaborador**: `matricula=12345`, `senha=senha123`

---

## Executando a Aplicacao

### Modo Desenvolvimento

Para iniciar o servidor da API em modo de desenvolvimento (com recarregamento automatico):

```bash
uvicorn app.main:app --reload
```

A API estara disponivel em: [http://localhost:8000](http://localhost:8000)

### Documentacao Interativa da API

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Testes

### Executar todos os testes

**No Windows:**

```bash
.\run_tests.bat
```

**No Linux/macOS:**

```bash
./run_tests.sh
```

### Executar testes especificos

Voce pode executar testes individualmente ou por grupo:

```bash
pytest tests/test_auth.py -v
pytest tests/test_colaboradores.py -v
pytest tests/test_ciclos.py -v
pytest tests/test_avaliacoes_simple.py -v
pytest tests/test_metas.py -v
```

### Ver relatorio de cobertura de codigo

Para gerar um relatorio de cobertura de testes em HTML:

```bash
pytest --cov=app --cov-report=html
```

Abra o arquivo `htmlcov/index.html` no seu navegador para visualizar o relatorio.

---

## Documentação

Para detalhes completos sobre os endpoints da API, modelos, arquitetura e autenticação, consulte:

- [Documentação Detalhada da API](docs/API.md)
- [Arquitetura do Projeto](docs/ARCHITECTURE.md)
- [Solução de Problemas](docs/TROUBLESHOOTING.md)
- [Coleções Postman](docs/collections/postman_collections.md)


---

## Usuarios Padrao (para ambiente de desenvolvimento)

| Matricula | Senha    | Papel       | Descricao                   |
| --------- | -------- | ----------- | --------------------------- |
| admin     | admin123 | ADMIN       | Acesso total ao sistema     |
| gestor1   | senha123 | GESTOR      | Pode gerenciar subordinados |
| 12345     | senha123 | COLABORADOR | Acesso basico               |
---

## Endpoints Principais da API

### Endpoints Gerais

- `GET /` - Endpoint raiz da API.
- `GET /health` - Verifica a saude da aplicacao.

### Autenticação (`/api/auth`)

- `POST /api/auth/token` - Obtém um token de acesso OAuth2 (usado principalmente pelo Swagger UI).
- `POST /api/auth/login` - Realiza o login do usuário e retorna um token de acesso.

### Colaboradores (`/api/colaboradores`)

- `GET /api/colaboradores/me` - Retorna os dados do colaborador atualmente logado.
- `GET /api/colaboradores/` - Lista todos os colaboradores (com filtros opcionais).
- `GET /api/colaboradores/{matricula}` - Busca um colaborador específico pela matrícula.
- `POST /api/colaboradores/` - Cria um novo colaborador.
- `PUT /api/colaboradores/{matricula}` - Atualiza os dados de um colaborador existente.
- `DELETE /api/colaboradores/{matricula}` - Desativa um colaborador (soft delete).
- `GET /api/colaboradores/{matricula}/subordinados` - Lista os subordinados de um gestor.
- `GET /api/colaboradores/{matricula}/gestor` - Retorna o gestor de um colaborador.

### Ciclos de Avaliação (`/api/ciclos`)

- `GET /api/ciclos/` - Lista todos os ciclos de avaliação.
- `GET /api/ciclos/ativo` - Retorna o ciclo de avaliação que está ativo no momento.
- `GET /api/ciclos/{ciclo_id}` - Busca um ciclo de avaliação específico por ID.
- `POST /api/ciclos/` - Cria um novo ciclo de avaliação.
- `PUT /api/ciclos/{ciclo_id}` - Atualiza um ciclo de avaliação existente.
- `DELETE /api/ciclos/{ciclo_id}` - Deleta um ciclo de avaliação.

### Avaliações (`/api/avaliacoes`)

- `GET /api/avaliacoes/` - Lista todas as avaliações com filtros opcionais.
- `GET /api/avaliacoes/minhas` - Lista as avaliações onde o usuário logado é o avaliado.
- `GET /api/avaliacoes/pendentes` - Lista as avaliações pendentes para o usuário logado (como avaliador).
- `GET /api/avaliacoes/{avaliacao_id}` - Busca uma avaliação específica por ID.
- `POST /api/avaliacoes/` - Cria uma nova avaliação comportamental.
- `PUT /api/avaliacoes/{avaliacao_id}` - Atualiza uma avaliação comportamental existente.
- `DELETE /api/avaliacoes/{avaliacao_id}` - Deleta uma avaliação comportamental.
- `POST /api/avaliacoes/{avaliacao_id}/concluir` - Marca uma avaliação como concluída.

### Metas (`/api/metas`)

- `GET /api/metas/` - Lista todas as metas com filtros opcionais.
- `GET /api/metas/minhas` - Lista as metas do colaborador logado.
- `GET /api/metas/{meta_id}` - Busca uma meta específica por ID.
- `POST /api/metas/` - Cria uma nova meta.
- `PUT /api/metas/{meta_id}` - Atualiza uma meta existente.
- `DELETE /api/metas/{meta_id}` - Deleta uma meta.

---

## Seguranca

O projeto implementa as seguintes medidas de seguranca:

- **JWT Authentication**: Utiliza JSON Web Tokens para autenticacao segura com tokens de acesso com expiracao.
- **Password Hashing**: Senhas de usuarios sao armazenadas de forma segura usando hash bcrypt.
- **Role-Based Access Control (RBAC)**: O acesso a diferentes endpoints e funcionalidades e controlado com base no papel do usuario (Admin, Gestor, Colaborador).
- **SQL Injection Protection**: O uso do ORM SQLAlchemy ajuda a prevenir ataques de injecao SQL.
- **CORS Configuration**: O CORS esta configurado para permitir apenas origens especificas, prevenindo ataques de cross-site scripting.

---

## Conventional Commits

- `feat:` - Nova funcionalidade
- `fix:` - Correcao de bug
- `docs:` - Alteracoes na documentacao
- `test:` - Adicao ou correcao de testes
- `chore:` - Tarefas de manutencao, sem alteracao no codigo da aplicacao
- `refactor:` - Refatoracao de codigo, sem mudanca de funcionalidade
- `style:` - Alteracoes de formatacao de codigo

---

`Desenvolvido por Caio André 😼`