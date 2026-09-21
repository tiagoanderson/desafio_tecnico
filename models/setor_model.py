# =============================================================================
# models/setor_model.py
# -----------------------------------------------------------------------------
# CAMADA: Model (Backend)
#
# Funções que leem e gravam dados da tabela "setor", usando comandos SQL
# escritos à mão (sem ORM). Repare no uso do "?" dentro das strings SQL:
# isso é uma QUERY PARAMETRIZADA. O sqlite3 substitui o "?" pelo valor de
# forma segura, evitando SQL Injection (nunca fazemos f"...{nome}..." para
# montar SQL com dado vindo do usuário).
#
# Todas as funções abrem a conexão e a fecham dentro de um bloco
# try/finally: isso garante que a conexão SEMPRE seja fechada, mesmo se o
# comando SQL falhar (ex: violação da restrição UNIQUE). Sem isso, uma
# conexão "esquecida" aberta pode travar o banco para as próximas operações
# (erro "database is locked").
# =============================================================================

from models.database import get_conexao


def listar_todos():
    """Retorna todos os setores cadastrados, ordenados por nome."""
    conexao = get_conexao()
    try:
        return conexao.execute("SELECT id, nome FROM setor ORDER BY nome").fetchall()
    finally:
        conexao.close()


def buscar_por_id(setor_id):
    """Retorna um único setor pelo id, ou None se ele não existir."""
    conexao = get_conexao()
    try:
        return conexao.execute(
            "SELECT id, nome FROM setor WHERE id = ?", (setor_id,)
        ).fetchone()
    finally:
        conexao.close()


def contar():
    """Retorna a quantidade total de setores cadastrados (usado no dashboard)."""
    conexao = get_conexao()
    try:
        linha = conexao.execute("SELECT COUNT(*) AS total FROM setor").fetchone()
        return linha["total"]
    finally:
        conexao.close()


def criar(nome):
    """
    Insere um novo setor no banco e devolve o id gerado automaticamente
    (cursor.lastrowid). Se já existir um setor com o mesmo nome, o SQLite
    recusa a inserção com um erro (a coluna "nome" tem restrição UNIQUE) —
    esse erro é tratado pelo Controller, não aqui no Model.
    """
    conexao = get_conexao()
    try:
        cursor = conexao.execute("INSERT INTO setor (nome) VALUES (?)", (nome,))
        conexao.commit()
        return cursor.lastrowid
    finally:
        conexao.close()


def atualizar(setor_id, nome):
    """Atualiza o nome de um setor já existente."""
    conexao = get_conexao()
    try:
        conexao.execute("UPDATE setor SET nome = ? WHERE id = ?", (nome, setor_id))
        conexao.commit()
    finally:
        conexao.close()


def excluir(setor_id):
    """
    Remove um setor do banco. Graças ao "ON DELETE CASCADE" definido na
    tabela patrimonio (veja models/database.py), os patrimônios ligados a
    este setor são apagados automaticamente pelo próprio SQLite.
    """
    conexao = get_conexao()
    try:
        conexao.execute("DELETE FROM setor WHERE id = ?", (setor_id,))
        conexao.commit()
    finally:
        conexao.close()

def contar_patrimonios_vinculados(setor_id):
    """ Retorna a quantidade de patrimonios vinculados ao setor selecionado"""
    conexao = get_conexao()
    try:
        linha = conexao.execute(
                "SELECT COUNT(*) as total FROM patrimonio WHERE setor_id = ?",
                (setor_id,),
                ).fetchone()
        return linha["total"]
    finally:
        conexao.close()