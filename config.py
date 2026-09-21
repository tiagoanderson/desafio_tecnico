# =============================================================================
# config.py
# -----------------------------------------------------------------------------
# CAMADA: Configuração (apoio ao Backend)
#
# Este arquivo concentra as configurações do sistema (caminho do banco de
# dados, chave secreta do Flask, etc). Manter isso separado do app.py é uma
# boa prática: se um dia o banco mudar de lugar, mexemos em um único ponto.
# =============================================================================

import os

# Diretório base do projeto (pasta onde este arquivo está)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configurações gerais da aplicação Flask."""

    # Chave usada pelo Flask para assinar sessões e mensagens "flash".
    # Em um projeto real de produção, isso viria de uma variável de ambiente.
    SECRET_KEY = "senai-cadastro-patrimonio-2026"

    # Caminho do arquivo do banco SQLite (fica dentro da pasta /database).
    # É lido diretamente pelo models/database.py, que usa a biblioteca
    # padrão "sqlite3" (sem ORM) para conversar com o banco.
    CAMINHO_BANCO = os.path.join(BASE_DIR, "database", "patrimonio.db")
