# =============================================================================
# controllers/setor_controller.py
# -----------------------------------------------------------------------------
# CAMADA: Controller (Backend)
#
# Implementa o CRUD (Create, Read, Update, Delete) do Setor:
#   - GET  /setores                -> lista todos os setores
#   - GET  /setores/novo           -> exibe formulário de cadastro
#   - POST /setores/novo           -> grava o novo setor no banco
#   - GET  /setores/editar/<id>    -> exibe formulário preenchido para edição
#   - POST /setores/editar/<id>    -> grava as alterações no banco
#   - POST /setores/deletar/<id>   -> remove o setor do banco
# =============================================================================

import sqlite3

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from models import setor_model


setor_bp = Blueprint("setor", __name__, url_prefix="/setores")


@setor_bp.route("/")
def listar():
    """Lista todos os setores cadastrados (equivalente à tela de exemplo do PDF)."""
    setores = setor_model.listar_todos()
    return render_template("setor/listar.html", setores=setores)


@setor_bp.route("/novo", methods=["GET", "POST"])
def novo():
    """Formulário de cadastro de um novo setor."""

    if request.method == "POST":
        # --- BACKEND: lê os dados enviados pelo formulário HTML (FRONTEND) ---
        nome = request.form.get("nome", "").strip()

        # Validação simples: o nome é obrigatório.
        if not nome:
            flash("O nome do setor é obrigatório.", "danger")
            return render_template("setor/form.html", setor=None)

        try:
            setor_model.criar(nome)
        except sqlite3.IntegrityError:
            # A coluna "nome" da tabela setor tem uma restrição UNIQUE no
            # banco. Este erro acontece quando já existe um setor com o
            # mesmo nome — é o próprio banco garantindo a integridade dos
            # dados, e o Controller só precisa avisar o usuário.
            flash(f'Já existe um setor chamado "{nome}".', "danger")
            return render_template("setor/form.html", setor=None)

        flash(f'Setor "{nome}" cadastrado com sucesso!', "success")
        return redirect(url_for("setor.listar"))

    # Método GET: apenas mostra o formulário vazio.
    return render_template("setor/form.html", setor=None)


@setor_bp.route("/editar/<int:setor_id>", methods=["GET", "POST"])
def editar(setor_id):
    """Formulário de edição de um setor existente."""

    setor = setor_model.buscar_por_id(setor_id)
    if setor is None:
        abort(404)

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()

        if not nome:
            flash("O nome do setor é obrigatório.", "danger")
            return render_template("setor/form.html", setor=setor)

        try:
            setor_model.atualizar(setor_id, nome)
        except sqlite3.IntegrityError:
            flash(f'Já existe um setor chamado "{nome}".', "danger")
            return render_template("setor/form.html", setor=setor)

        flash(f'Setor "{nome}" atualizado com sucesso!', "success")
        return redirect(url_for("setor.listar"))

    return render_template("setor/form.html", setor=setor)


@setor_bp.route("/deletar/<int:setor_id>", methods=["POST"])
def deletar(setor_id):
    """Remove um setor, só se não tiver patrimônios vinculados."""
    setor = setor_model.buscar_por_id(setor_id)
    if setor is None:
        abort(404)

    qtd = setor_model.contar_patrimonios_vinculados(setor_id)

    if qtd > 0:
        flash(
            f'Não é possível excluir o setor "{setor["nome"]}": '
            f'existem {qtd} patrimônio(s) vinculado(s) a ele. '
            f'Remova ou transfira esses itens primeiro.',
            "danger",
        )
        return redirect(url_for("setor.listar"))   # ← 8 espaços = DENTRO do if ✅

    setor_model.excluir(setor_id)                  # ← 4 espaços = fora do if
    flash(f'Setor "{setor["nome"]}" excluído com sucesso!', "success")
    return redirect(url_for("setor.listar"))
