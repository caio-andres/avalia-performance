import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configurações do RDS
DB_HOST = "database-01.cqpgw4ac089h.us-east-1.rds.amazonaws.com"
DB_PORT = 5432
DB_USER = "usuario"
DB_PASSWORD = "senha1234!"
DB_NAME = "itau_avaliacoes"

def create_database():
    """
    Cria o banco de dados no RDS se não existir
    """
    try:
        # Conectar ao banco padrão 'postgres'
        print(f"🔌 Conectando ao RDS em {DB_HOST}...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database="postgres"  # Conecta ao banco padrão
        )
        
        # Necessário para executar CREATE DATABASE
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cursor = conn.cursor()
        
        # Verificar se o banco já existe
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DB_NAME,)
        )
        
        exists = cursor.fetchone()
        
        if exists:
            print(f"ℹ️  Banco de dados '{DB_NAME}' já existe!")
        else:
            # Criar o banco
            print(f"🚀 Criando banco de dados '{DB_NAME}'...")
            cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f"✅ Banco de dados '{DB_NAME}' criado com sucesso!")
        
        cursor.close()
        conn.close()
        
        print(f"\n✅ Pronto! Agora atualize o .env com:")
        print(f"DATABASE_URL=postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        raise

if __name__ == "__main__":
    create_database()