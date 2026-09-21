# Cadastro de Patrimônio — SENAI

Sistema web para cadastro, visualização, edição e exclusão de **Patrimônios**
e **Setores**, com relacionamento entre eles. Desenvolvido em **Python
(Flask)** seguindo o padrão de arquitetura **MVC**, com banco de dados
**SQLite** acessado via **SQL puro** (biblioteca `sqlite3` do próprio
Python, sem ORM) — escolha proposital para deixar os comandos SQL visíveis
e facilitar a explicação do projeto em sala de aula.

Projeto feito para a Etapa 2 (Avaliação Prática) do processo seletivo SENAI
SP — cargo Instrutor de Formação Profissional III (Tecnologia da Informação).

## Como rodar o projeto

Pré-requisito: Python 3.10+ instalado.

```bash
# 1. Entrar na pasta do projeto
cd cadastro_patrimonio_senai

# 2. (Recomendado) Criar um ambiente virtual
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Linux/Mac

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Rodar o sistema
python app.py
```

Depois de rodar, abra o navegador em **http://127.0.0.1:5000**.

Na primeira execução, o arquivo `database/patrimonio.db` é criado
automaticamente, com as tabelas e alguns dados de exemplo (os mesmos do
exemplo do PDF de orientações: setores Administrativo/Biblioteca/Secretaria
e os itens Cadeira/Mesa/Armário).

## O que é Backend e o que é Frontend neste projeto

| Camada | Onde fica | O que faz |
|---|---|---|
| **Backend** | `app.py`, `config.py`, `models/`, `controllers/` | Roda no servidor. Cuida das regras de negócio, valida dados, conversa com o banco SQLite e decide qual página devolver. |
| **Frontend** | `templates/` (HTML + Jinja2), `static/css`, `static/js` | Roda no navegador do usuário. É o que a pessoa vê e interage: telas, formulários, cores, menu, confirmação de exclusão. |

O Flask entrega o HTML já "pronto" (renderizado no servidor, via Jinja2) —
por isso não existe uma pasta separada de "API" com JSON: o Controller
já devolve a página HTML diretamente para o navegador.

## Arquitetura MVC — como o projeto está organizado

```
cadastro_patrimonio_senai/
│
├── app.py                        # Ponto de entrada: cria o Flask, liga tudo
├── config.py                     # Configurações (banco de dados, chave secreta)
│
├── models/                       # MODEL — regras de dados (Backend)
│   ├── database.py               #   conexão sqlite3 + criação das tabelas (SQL puro)
│   ├── setor_model.py            #   funções SQL da tabela "setor"
│   └── patrimonio_model.py       #   funções SQL da tabela "patrimonio" (com FK para setor)
│
├── controllers/                  # CONTROLLER — rotas/regras de negócio (Backend)
│   ├── main_controller.py        #   tela inicial (dashboard)
│   ├── setor_controller.py       #   CRUD de Setor
│   └── patrimonio_controller.py  #   CRUD de Patrimônio
│
├── templates/                    # VIEW — telas HTML (Frontend, usando Jinja2)
│   ├── base.html                 #   layout base com o menu superior
│   ├── index.html                #   tela inicial
│   ├── setor/
│   │   ├── listar.html
│   │   └── form.html
│   └── patrimonio/
│       ├── listar.html
│       └── form.html
│
├── static/                       # Frontend: arquivos estáticos
│   ├── css/style.css             #   cores institucionais do SENAI
│   └── js/script.js              #   confirmação de exclusão, fecha alertas
│
├── database/
│   └── patrimonio.db             # arquivo do banco SQLite (criado ao rodar)
│
└── requirements.txt
```

**Fluxo de uma requisição** (exemplo: cadastrar um novo setor):

1. Usuário preenche o formulário em `templates/setor/form.html` (**View**) e clica em Salvar.
2. O navegador envia um `POST /setores/novo`, recebido pela função `novo()` em `controllers/setor_controller.py` (**Controller**).
3. O Controller valida os dados e chama `setor_model.criar(nome)`, definida em `models/setor_model.py` (**Model**), que executa um `INSERT INTO setor (nome) VALUES (?)` no banco SQLite.
4. O Controller redireciona de volta para a listagem, que busca os dados atualizados no Model (`SELECT * FROM setor`) e os exibe através de `templates/setor/listar.html` (**View**).

## Funcionalidades

- **Setores**: cadastrar, listar, editar e excluir.
- **Patrimônios**: cadastrar, listar, editar e excluir — cada patrimônio
  pertence a um setor (relacionamento 1:N entre Setor e Patrimônio).
- Ao excluir um setor, os patrimônios vinculados a ele são excluídos
  automaticamente (evita registros "órfãos" no banco).
- Validação de campos obrigatórios e de número de patrimônio único.
- Mensagens de feedback (sucesso/erro) após cada ação.
- Layout responsivo (Bootstrap 5), com a paleta de cores do SENAI
  (vermelho institucional, branco e cinza escuro).

## Segurança: consultas SQL parametrizadas

Todas as consultas em `models/setor_model.py` e `models/patrimonio_model.py`
usam `?` no lugar dos valores (ex: `"SELECT * FROM setor WHERE id = ?"`),
e passam os dados reais separadamente (`(setor_id,)`). Isso é chamado de
**query parametrizada** e é a forma correta de evitar **SQL Injection**:
o valor digitado pelo usuário nunca é "colado" diretamente dentro do texto
do comando SQL.

## Acesso em nível de desenvolvedor

Para demonstrar o funcionamento interno durante a apresentação:

- `debug=True` em `app.py` mostra o *debugger* interativo do Flask em caso de erro.
- O arquivo `database/patrimonio.db` pode ser aberto com qualquer visualizador
  de SQLite (ex: extensão "SQLite Viewer" do VS Code, ou DB Browser for SQLite)
  para mostrar as tabelas sendo alteradas em tempo real.
