
# =============================================================================
# app.py
# -----------------------------------------------------------------------------
# CAMADA: Controller / Ponto de entrada (Backend)
#
# Este é o arquivo que "liga tudo": cria a aplicação Flask, registra os
# Controllers (Blueprints) e inicia o servidor. O banco de dados é criado
# e populado por models/database.py e pelos próprios Models, usando SQL
# puro (sqlite3) — sem ORM.
#
# Como executar:
#   1) pip install -r requirements.txt
#   2) python app.py
#   3) Abrir http://127.0.0.1:5000 no navegador
#
# Na primeira execução, o banco de dados e as tabelas são criados
# automaticamente e alguns dados de exemplo são inseridos.
# =============================================================================
import os

from flask import Flask
from config import Config
from models import patrimonio_model, setor_model
from models.database import criar_tabelas


def criar_app():
    """
    Application Factory: função que cria e configura a aplicação Flask.
    Usar uma função para isso (em vez de criar o app direto no módulo)
    facilita testes automatizados e reaproveitamento do código no futuro.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- Registro dos Controllers (Blueprints) ---
    # Cada Blueprint cuida de um pedaço do sistema (rotas /, /setores, /patrimonios).
    from controllers.main_controller import main_bp
    from controllers.setor_controller import setor_bp
    from controllers.patrimonio_controller import patrimonio_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(setor_bp)
    app.register_blueprint(patrimonio_bp)

    # --- Banco de dados ---
    # Cria as tabelas e popula os dados de exemplo SEMPRE que o app é criado.
    # Isso é essencial para o Render, onde o gunicorn importa este arquivo
    # (então o bloco "if __name__ == '__main__'" NÃO é executado).
    criar_tabelas()
    popular_dados_iniciais()

    return app


def popular_dados_iniciais():
    """
    Cria alguns registros de exemplo (mesmos do PDF de orientações) caso o
    banco esteja vazio. Isso é só para facilitar a demonstração do sistema
    na aula-teste — não é obrigatório para o funcionamento do CRUD.
    """
    if setor_model.contar() > 0:
        return  # já existem dados, não precisa popular de novo

    id_administrativo = setor_model.criar("Administrativo")
    id_biblioteca = setor_model.criar("Biblioteca")
    setor_model.criar("Secretaria")

    patrimonio_model.criar("Cadeira", "7305477760", id_administrativo)
    patrimonio_model.criar("Mesa", "7305477750", id_biblioteca)
    patrimonio_model.criar("Armário", "7305477780", id_administrativo)


# Instância da aplicação usada pelo servidor.
app = criar_app()


if __name__ == "__main__":
    # O bloco abaixo só roda no desenvolvimento local (python app.py).
    # No Render, o gunicorn usa "app:app" e ignora este bloco.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)