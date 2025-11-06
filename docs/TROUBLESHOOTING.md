# Troubleshooting (Resolucao de Problemas)

- **Erro `psycopg2.OperationalError: connection to server at ... failed`:**
  - **Causa:** Geralmente indica que o banco de dados PostgreSQL nao esta acessivel ou configurado incorretamente.
  - **Solucao:**
    - Verifique se o servidor PostgreSQL esta em execucao.
    - Confirme se as credenciais (usuario, senha, host, porta, nome do DB) em `DATABASE_URL` no seu arquivo `.env` estao corretas e correspondem a sua configuracao do PostgreSQL.
    - Certifique-se de que o firewall do seu sistema ou da rede nao esta bloqueando a conexao com a porta do PostgreSQL (padrao 5432).
    - Se estiver usando Docker, verifique se o container do PostgreSQL esta rodando e se as portas estao mapeadas corretamente.

- **Erro `ModuleNotFoundError: No module named '...'`:**
  - **Causa:** Uma dependencia Python nao foi instalada ou o ambiente virtual nao esta ativado.
  - **Solucao:**
    - Verifique se o ambiente virtual (`.venv`) esta ativado. Voce deve ver `(.venv)` no inicio da linha de comando.
    - Execute `pip install -r requirements.txt` novamente para garantir que todas as dependencias listadas foram instaladas corretamente.

- **Erro `ImportError: cannot import name '...' from '...'`:**
  - **Causa:** Pode ser devido a versoes incompativeis de bibliotecas ou um problema na instalacao.
  - **Solucao:**
    - Tente atualizar as dependencias com `pip install --upgrade -r requirements.txt`.
    - Se o problema persistir, pode ser necessario recriar o ambiente virtual e reinstalar as dependencias.

- **Problemas com Variaveis de Ambiente:**
  - **Causa:** O arquivo `.env` nao foi criado, esta com erros de sintaxe, ou as variaveis nao estao sendo carregadas.
  - **Solucao:**
    - Certifique-se de que o arquivo `.env` existe na raiz do projeto e que voce o copiou de `.env.example`.
    - Verifique se nao ha espacos extras ou caracteres invalidos nos nomes das variaveis ou nos valores.
    - Reinicie o servidor da aplicacao apos qualquer alteracao no arquivo `.env`.
