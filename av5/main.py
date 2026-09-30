import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

load_dotenv()
Base = declarative_base()

# CLASSES 1 para N
class Editora(Base):
    __tablename__ = 'editoras'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cnpj = Column(String(20), nullable=False)
    cidade = Column(String(50), nullable=False)
    
    # Relacionamento 1 para N
    livros = relationship("Livro", back_populates="editora", cascade="all, delete-orphan")

class Livro(Base):
    __tablename__ = 'livros'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    genero = Column(String(50), nullable=False)
    preco = Column(Float, nullable=False)
    
    editora_id = Column(Integer, ForeignKey('editoras.id'), nullable=False)
    editora = relationship("Editora", back_populates="livros")

# conexão do bd

def conectar_banco():

    print("\nESCOLHA O BANCO DE DADOS")
    print("1. SQLite (Local)")
    print("2. MySQL (Remoto via .env)")
    opcao = input("Opção: ").strip()

    if opcao == '1':
        db_url = "sqlite:///biblioteca.db"

    elif opcao == '2':
        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        port = os.getenv("MYSQL_PORT")
        db = os.getenv("MYSQL_DB")
        db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"

    else:
        print("Opção inválida! Usando SQLite por padrão.")
        db_url = "sqlite:///biblioteca.db"

    engine = create_engine(db_url)
    
    # limpa as tabelas em conflitos
    Base.metadata.drop_all(engine)
    
    # Recria as tabelas do zero com a estrutura correta
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    return Session()


def inserir_dados(session):
    print("\n--- INSERIR ---")
    print("1. Inserir Editora")
    print("2. Inserir Livro")
    op = input("Opção: ").strip()

    if op == '1':
        nome = input("Nome da Editora: ")
        cnpj = input("CNPJ: ")
        cidade = input("Cidade: ")
        nova_editora = Editora(nome=nome, cnpj=cnpj, cidade=cidade)
        session.add(nova_editora)
        session.commit()
        print("Editora cadastrada com sucesso!")
        
    elif op == '2':

        # Busca todas as editoras para listar e validar
        editoras = session.query(Editora).all()
        if not editoras:
            print("\nNenhuma editora cadastrada! Cadastre ao menos uma editora primeiro.")
            return
        
        # Exibe a lista de editoras cadastradas com ID e Nome
        print("\n--- EDITORAS DISPONÍVEIS ---")
        for ed in editoras:
            print(f"ID: {ed.id} | Nome: {ed.nome} ({ed.cidade})")
            
        try:
            editora_id = int(input("\nDigite o ID da Editora para o livro: "))
        except ValueError:
            print("ID inválido! Digite apenas números.")
            return

        # Valida se a editora existe no banco
        editora_existe = session.query(Editora).filter_by(id=editora_id).first()
        if not editora_existe:
            print(f"Erro: Não existe nenhuma Editora com o ID {editora_id}!")
            return

        # Coleta os dados do livro apenas se a editora for válida
        titulo = input("Título do Livro: ")
        genero = input("Gênero: ")
        try:
            preco = float(input("Preço (R$): "))
        except ValueError:
            print("Preço inválido! Digite um valor numérico.")
            return
        
        novo_livro = Livro(titulo=titulo, genero=genero, preco=preco, editora_id=editora_id)
        session.add(novo_livro)
        session.commit()
        print(f" Livro '{titulo}' cadastrado com sucesso para a editora '{editora_existe.nome}'!")


def listar_dados(session):
    print("\nLISTAR")
    editoras = session.query(Editora).all()
    if not editoras:
        print("Nenhum registro encontrado.")
        return

    for ed in editoras:
        print(f"\n[Editora ID {ed.id}] {ed.nome} - CNPJ: {ed.cnpj} ({ed.cidade})")
        if ed.livros:
            for l in ed.livros:
                print(f"  └─ Livro ID {l.id}: {l.titulo} | Gênero: {l.genero} | R$ {l.preco:.2f}")
        else:
            print("  └─ Nenhum livro cadastrado para esta editora.")


def excluir_dados(session):
    print("\nEXCLUIR")
    print("1. Excluir Editora (e todos os seus livros)")
    print("2. Excluir Livro")
    op = input("Opção: ").strip()

    if op == '1':
        editora_id = int(input("ID da Editora a excluir: "))
        editora_obj = session.query(Editora).filter_by(id=editora_id).first()
        if editora_obj:
            session.delete(editora_obj)
            session.commit()
            print("Editora excluída com sucesso!")
        else:
            print("Editora não encontrada.")
            
    elif op == '2':
        livro_id = int(input("ID do Livro a excluir: "))
        livro_obj = session.query(Livro).filter_by(id=livro_id).first()
        if livro_obj:
            session.delete(livro_obj)
            session.commit()
            print("Livro excluído com sucesso!")
        else:
            print("Livro não encontrado.")

#menu principal
def main():
    session = conectar_banco()
    
    while True:
        print("1. Inserir dados")
        print("2. Listar dados")
        print("3. Excluir dados")
        print("4. Trocar Conexão do Banco")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == '1':
            inserir_dados(session)
        elif opcao == '2':
            listar_dados(session)
        elif opcao == '3':
            excluir_dados(session)
        elif opcao == '4':
            session.close()
            session = conectar_banco()
        elif opcao == '5':
            print("Saindo...")
            session.close()
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()