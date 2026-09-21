# =============================================================================
# models/database.py
# -----------------------------------------------------------------------------
# CAMADA: Model (Backend)
#
# Este projeto usa SQL "puro", através do módulo "sqlite3" que já vem
# junto com o Python (não precisa instalar nada extra). Ou seja: NÃO usamos
# um ORM (biblioteca que "traduz" objetos Python em comandos SQL escondidos).
#
# Isso é proposital para fins didáticos: assim dá pra mostrar exatamente o
# comando SQL (SELECT, INSERT, UPDATE, DELETE) que está sendo executado em
# cada operação, o que ajuda a explicar como o backend realmente conversa
# com o banco de dados.
#
# Este arquivo concentra duas responsabilidades:
#   1) get_conexao() -> abre e devolve uma conexão com o banco SQLite.
#   2) criar_tabelas() -> cria as tabelas "setor" e "patrimonio", caso ainda
#      não existam (isso é chamado uma única vez, ao iniciar o app.py).
# =============================================================================


import os
import sqlite3
from config import Config

# Garante que a pasta do banco existe antes de conectar.
# Sem isso, o sqlite3 dá erro "unable to open database file" quando a
# pasta ainda não existe (ex: no Render, que começa do zero).
os.makedirs(os.path.dirname(Config.CAMINHO_BANCO), exist_ok=True)


def get_conexao():
    """
    Abre uma conexão com o arquivo do banco SQLite e a devolve pronta
    para uso.

    Dois detalhes importantes:

    - row_factory = sqlite3.Row: por padrão, o sqlite3 devolve cada linha
      como uma tupla (ex: linha[0], linha[1]...). Com o row_factory
      configurado, também conseguimos acessar pelo nome da coluna
      (ex: linha["nome"]), o que deixa o código muito mais legível.

    - PRAGMA foreign_keys = ON: o SQLite, por padrão, NÃO valida chaves
      estrangeiras. Precisamos ligar essa checagem manualmente em cada
      conexão para que, por exemplo, um patrimônio não possa ser criado
      apontando para um setor que não existe, e para que a exclusão em
      cascata (apagar um setor remove os patrimônios dele) funcione.
    """
    conexao = sqlite3.connect(Config.CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
    """
    Cria as tabelas do sistema caso elas ainda não existam
    (é seguro chamar esta função toda vez que o app inicia).
    """
    conexao = get_conexao()

    # Tabela SETOR: cada linha é um setor (ex: "Administrativo").
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS setor (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
        """
    )

    # Tabela PATRIMONIO: cada linha é um item de patrimônio.
    # A coluna "setor_id" é a CHAVE ESTRANGEIRA (foreign key) que cria o
    # relacionamento pedido no desafio: todo patrimônio pertence a um setor.
    # "ON DELETE CASCADE" faz o SQLite apagar automaticamente os
    # patrimônios de um setor quando esse setor é excluído.
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS patrimonio (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            nome              TEXT NOT NULL,
            numero_patrimonio TEXT NOT NULL UNIQUE,
            data_cadastro     TEXT NOT NULL,
            setor_id          INTEGER NOT NULL,
            FOREIGN KEY (setor_id) REFERENCES setor (id) 
        )
        """
    )

    conexao.commit()
    conexao.close()
