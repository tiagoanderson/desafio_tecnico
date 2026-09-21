# =============================================================================
# models/patrimonio_model.py
# -----------------------------------------------------------------------------
# CAMADA: Model (Backend)
#
# Funções que leem e gravam dados da tabela "patrimonio", em SQL puro.
# O relacionamento com "setor" aparece de duas formas aqui:
#   - a coluna "setor_id" (chave estrangeira) é gravada em criar()/atualizar();
#   - em listar_todos(), usamos um JOIN para trazer também o NOME do setor,
#     já que a tela de listagem precisa mostrar "Administrativo" e não
#     apenas o número "1".
#
# Assim como em setor_model.py, cada função usa try/finally para garantir
# que a conexão seja fechada mesmo se o comando SQL falhar (ex: violação
# da restrição UNIQUE em "numero_patrimonio").
# =============================================================================

from datetime import datetime

from models.database import get_conexao


def listar_todos():
    """
    Retorna todos os patrimônios, cada um já acompanhado do nome do seu
    setor. O JOIN "liga" a linha de patrimonio com a linha de setor
    correspondente através de patrimonio.setor_id = setor.id.
    """
    conexao = get_conexao()
    try:
        return conexao.execute(
            """
            SELECT
                patrimonio.id,
                patrimonio.nome,
                patrimonio.numero_patrimonio,
                patrimonio.setor_id,
                setor.nome AS setor_nome
            FROM patrimonio
            JOIN setor ON setor.id = patrimonio.setor_id
            ORDER BY patrimonio.id
            """
        ).fetchall()
    finally:
        conexao.close()


def buscar_por_id(patrimonio_id):
    """Retorna um único patrimônio pelo id, ou None se ele não existir."""
    conexao = get_conexao()
    try:
        return conexao.execute(
            """
            SELECT id, nome, numero_patrimonio, setor_id
            FROM patrimonio
            WHERE id = ?
            """,
            (patrimonio_id,),
        ).fetchone()
    finally:
        conexao.close()


def contar():
    """Retorna a quantidade total de patrimônios cadastrados (usado no dashboard)."""
    conexao = get_conexao()
    try:
        linha = conexao.execute("SELECT COUNT(*) AS total FROM patrimonio").fetchone()
        return linha["total"]
    finally:
        conexao.close()

def contar_por_setor():
    """Retorna a quantidade total de patrimônios cadastrados no setor """
    conexao = get_conexao()
    try:
        linha = conexao.execute("SELECT COUNT(*) AS total FROM patrimonio where ?"()).fetchone()
        return linha["total"]
    finally:
        conexao.close()


def criar(nome, numero_patrimonio, setor_id):
    """
    Insere um novo patrimônio. Se já existir um patrimônio com o mesmo
    "numero_patrimonio", o SQLite recusa a inserção (coluna UNIQUE) — esse
    erro é tratado pelo Controller.
    """
    conexao = get_conexao()
    try:
        cursor = conexao.execute(
            """
            INSERT INTO patrimonio (nome, numero_patrimonio, data_cadastro, setor_id)
            VALUES (?, ?, ?, ?)
            """,
            (nome, numero_patrimonio, datetime.now().isoformat(timespec="seconds"), setor_id),
        )
        conexao.commit()
        return cursor.lastrowid
    finally:
        conexao.close()


def atualizar(patrimonio_id, nome, numero_patrimonio, setor_id):
    """Atualiza nome, número de patrimônio e setor de um item existente."""
    conexao = get_conexao()
    try:
        conexao.execute(
            """
            UPDATE patrimonio
            SET nome = ?, numero_patrimonio = ?, setor_id = ?
            WHERE id = ?
            """,
            (nome, numero_patrimonio, setor_id, patrimonio_id),
        )
        conexao.commit()
    finally:
        conexao.close()


def excluir(patrimonio_id):
    """Remove um patrimônio do banco de dados."""
    conexao = get_conexao()
    try:
        conexao.execute("DELETE FROM patrimonio WHERE id = ?", (patrimonio_id,))
        conexao.commit()
    finally:
        conexao.close()
