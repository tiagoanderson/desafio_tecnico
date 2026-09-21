# =============================================================================
# controllers/main_controller.py
# -----------------------------------------------------------------------------
# CAMADA: Controller (Backend)
#
# Controller responsável pela tela inicial (Dashboard) do sistema.
# Ele não faz nada muito complexo: apenas busca alguns números (totais)
# para exibir na página inicial e entrega o template "index.html".
# =============================================================================

from flask import Blueprint, render_template

from models import patrimonio_model, setor_model

# Um "Blueprint" é como um mini módulo de rotas do Flask. Ele permite
# organizar o sistema em pedaços (main, setor, patrimonio) e depois
# registrar todos eles juntos em app.py.
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Tela inicial: mostra um resumo (quantidade de setores e patrimônios)."""

    # --- BACKEND: consulta ao banco de dados (SELECT COUNT...) ---
    total_patrimonios = patrimonio_model.contar()
    total_setores = setor_model.contar()

    # --- FRONTEND: os valores acima são passados para o template Jinja2,
    # que é quem realmente monta o HTML mostrado ao usuário ---
    return render_template(
        "index.html",
        total_patrimonios=total_patrimonios,
        total_setores=total_setores,
    )
