from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import engine, Base, SessionLocal
from app.models.colaborador import Colaborador
from app.models.avaliacao import Ciclo, AvaliacaoComportamental, Meta
from app.core.security import get_password_hash
from datetime import date


def init_db():
    """
    Inicializa o banco de dados:
    - Cria todas as tabelas
    - Cria usuário admin padrão
    - Cria ciclo de exemplo
    """
    print("🔄 Dropando todas as tabelas existentes...")

    # Dropar schema public com CASCADE para remover todas as dependências
    try:
        with engine.connect() as conn:
            conn.execute(text("DROP SCHEMA public CASCADE"))
            conn.execute(text("CREATE SCHEMA public"))
            # Não precisa do GRANT para postgres, só para o usuário atual
            conn.execute(text("GRANT ALL ON SCHEMA public TO usuario"))
            conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
            conn.commit()
        print("✅ Tabelas antigas removidas!")
    except Exception as e:
        print(f"⚠️  Aviso ao dropar schema: {e}")

    print("🔄 Criando tabelas no banco de dados...")

    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)

    print("✅ Tabelas criadas com sucesso!")

    # Criar sessão
    db = SessionLocal()

    try:
        # Verificar se já existe usuário admin
        admin = db.query(Colaborador).filter(Colaborador.matricula == "admin").first()

        if not admin:
            print("🔄 Criando usuário administrador...")

            # Criar usuário admin
            admin = Colaborador(
                matricula="admin",
                nome="Administrador",
                email="admin@itau.com.br",
                senha_hash=get_password_hash("admin123"),
                cargo="Administrador",
                departamento="TI",
                ativo=True,
            )

            db.add(admin)
            db.commit()
            db.refresh(admin)

            print("✅ Usuário admin criado!")
            print("   Matrícula: admin")
            print("   Senha: admin123")
        else:
            print("ℹ️  Usuário admin já existe")

        # Criar colaboradores de exemplo
        print("🔄 Criando colaboradores de exemplo...")

        colaboradores_exemplo = [
            {
                "matricula": "12345",
                "nome": "João Silva",
                "email": "joao.silva@itau.com.br",
                "senha": "senha123",
                "cargo": "Analista",
                "departamento": "Tecnologia",
                "gestor_matricula": "admin",
            },
            {
                "matricula": "67890",
                "nome": "Maria Santos",
                "email": "maria.santos@itau.com.br",
                "senha": "senha123",
                "cargo": "Gerente",
                "departamento": "Operações",
                "gestor_matricula": "admin",
            },
            {
                "matricula": "11111",
                "nome": "Pedro Oliveira",
                "email": "pedro.oliveira@itau.com.br",
                "senha": "senha123",
                "cargo": "Coordenador",
                "departamento": "Tecnologia",
                "gestor_matricula": "67890",
            },
        ]

        for colab_data in colaboradores_exemplo:
            existing = (
                db.query(Colaborador)
                .filter(Colaborador.matricula == colab_data["matricula"])
                .first()
            )

            if not existing:
                colaborador = Colaborador(
                    matricula=colab_data["matricula"],
                    nome=colab_data["nome"],
                    email=colab_data["email"],
                    senha_hash=get_password_hash(colab_data["senha"]),
                    cargo=colab_data["cargo"],
                    departamento=colab_data["departamento"],
                    gestor_matricula=colab_data["gestor_matricula"],
                    ativo=True,
                )
                db.add(colaborador)

        db.commit()
        print("✅ Colaboradores de exemplo criados!")

        # Criar ciclo de exemplo
        print("🔄 Criando ciclo de avaliação de exemplo...")

        ciclo_atual = db.query(Ciclo).filter(Ciclo.ano == 2025).first()

        if not ciclo_atual:
            ciclo = Ciclo(
                ano=2025,
                descricao="Ciclo de Avaliação 2025",
                data_inicio=date(2025, 1, 1),
                data_fim=date(2025, 12, 31),
                status="em_andamento",
            )

            db.add(ciclo)
            db.commit()
            db.refresh(ciclo)

            print("✅ Ciclo 2025 criado!")
        else:
            print("ℹ️  Ciclo 2025 já existe")

        print("\n" + "=" * 50)
        print("✅ Banco de dados inicializado com sucesso!")
        print("=" * 50)
        print("\n📋 Credenciais de acesso:")
        print("   Matrícula: admin")
        print("   Senha: admin123")
        print("\n📋 Colaboradores de exemplo:")
        print("   Matrícula: 12345 | Senha: senha123")
        print("   Matrícula: 67890 | Senha: senha123")
        print("   Matrícula: 11111 | Senha: senha123")
        print("\n🚀 Inicie o servidor com: uvicorn app.main:app --reload")
        print("📖 Documentação: http://127.0.0.1:8000/docs")
        print("=" * 50 + "\n")

    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
