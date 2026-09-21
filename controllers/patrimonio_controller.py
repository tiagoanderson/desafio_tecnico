# =============================================================================
# controllers/patrimonio_controller.py
# -----------------------------------------------------------------------------
# CAMADA: Controller (Backend)
#
# Implementa o CRUD (Create, Read, Update, Delete) do Patrimônio.
# É praticamente igual ao setor_controller.py, mas aqui também precisamos
# tratar o relacionamento: todo patrimônio pertence a um setor, então o
# formulário precisa oferecer a lista de setores para o usuário escolher.
# =============================================================================

import sqlite3

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from models import patrimonio_model, setor_model

patrimonio_bp = Blueprint("patrimonio", __name__, url_prefix="/patrimonios")


@patrimonio_bp.route("/")
def listar():
    """Lista todos os patrimônios cadastrados, já com o nome do setor (JOIN)."""
    patrimonios = patrimonio_model.listar_todos()
    return render_template("patrimonio/listar.html", patrimonios=patrimonios)


@patrimonio_bp.route("/novo", methods=["GET", "POST"])
def novo():
    """Formulário de cadastro de um novo patrimônio."""

    # A lista de setores é necessária tanto no GET (para montar o <select>)
    # quanto no POST, caso a validação falhe e o formulário precise
    # ser exibido novamente.
    setores = setor_model.listar_todos()

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_patrimonio = request.form.get("numero_patrimonio", "").strip()
        setor_id = request.form.get("setor_id")

        # --- Validações básicas do backend ---
        if not nome or not numero_patrimonio or not setor_id:
            flash("Todos os campos são obrigatórios.", "danger")
            return render_template("patrimonio/form.html", patrimonio=None, setores=setores)

        try:
            patrimonio_model.criar(nome, numero_patrimonio, int(setor_id))
        except sqlite3.IntegrityError:
            # A coluna "numero_patrimonio" tem restrição UNIQUE no banco.
            flash(f'Já existe um patrimônio com o número "{numero_patrimonio}".', "danger")
            return render_template("patrimonio/form.html", patrimonio=None, setores=setores)

        flash(f'Patrimônio "{nome}" cadastrado com sucesso!', "success")
        return redirect(url_for("patrimonio.listar"))

    return render_template("patrimonio/form.html", patrimonio=None, setores=setores)


@patrimonio_bp.route("/editar/<int:patrimonio_id>", methods=["GET", "POST"])
def editar(patrimonio_id):
    """Formulário de edição de um patrimônio existente."""

    patrimonio = patrimonio_model.buscar_por_id(patrimonio_id)
    if patrimonio is None:
        abort(404)

    setores = setor_model.listar_todos()

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_patrimonio = request.form.get("numero_patrimonio", "").strip()
        setor_id = request.form.get("setor_id")

        if not nome or not numero_patrimonio or not setor_id:
            flash("Todos os campos são obrigatórios.", "danger")
            return render_template("patrimonio/form.html", patrimonio=patrimonio, setores=setores)

        try:
            patrimonio_model.atualizar(patrimonio_id, nome, numero_patrimonio, int(setor_id))
        except sqlite3.IntegrityError:
            flash(f'Já existe um patrimônio com o número "{numero_patrimonio}".', "danger")
            return render_template("patrimonio/form.html", patrimonio=patrimonio, setores=setores)

        flash(f'Patrimônio "{nome}" atualizado com sucesso!', "success")
        return redirect(url_for("patrimonio.listar"))

    return render_template("patrimonio/form.html", patrimonio=patrimonio, setores=setores)


@patrimonio_bp.route("/deletar/<int:patrimonio_id>", methods=["POST"])
def deletar(patrimonio_id):
    """Remove um patrimônio do banco de dados."""
    patrimonio = patrimonio_model.buscar_por_id(patrimonio_id)
    if patrimonio is None:
        abort(404)

    patrimonio_model.excluir(patrimonio_id)

    flash(f'Patrimônio "{patrimonio["nome"]}" excluído com sucesso!', "success")
    return redirect(url_for("patrimonio.listar"))
