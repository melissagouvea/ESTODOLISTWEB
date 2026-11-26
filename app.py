# Importa date, que permite trabalhar com datas.
from datetime import date

# Importa as ferramentas necessárias do Flask:
# Flask: cria a aplicação.
# render_template: exibe páginas HTML.
# request: recebe informações enviadas pelos formulários.
# session: armazena informações da sessão do usuário.
# redirect: redireciona o usuário para outra rota.
# flash: armazena mensagens temporárias para exibição.
from flask import Flask, render_template, request, session, redirect, flash

# Importa funções responsáveis por consultar e inserir tarefas no banco de dados.
from database import (consultar_tarefas, inserir_tarefa, buscar_tarefa, concluir_tarefa, apagar_tarefa)


# Cria a aplicação Flask.
# __name__ identifica o arquivo principal da aplicação.
app = Flask(__name__)

# Chave secreta necessária para proteger e utilizar as sessões do Flask.
app.secret_key = "senai"


# Define o e-mail e a senha do administrador.
ADM_EMAIL = "123@gmail.com"
ADM_SENHA = "123"

# Cria uma lista com as categorias disponíveis para as tarefas.
CATEGORIAS = ["Escola", "Trabalho", "Projetos", "Pessoal", "Saúde", "Outros"]


# ---------------------------------------------------------
# FUNÇÃO DE VALIDAÇÃO DAS TAREFAS
# ---------------------------------------------------------

# Recebe as informações da tarefa e verifica se estão corretas.
def validar_tarefa(nome, descricao, categoria, prazo, prioridade):

    # Cria uma lista vazia para armazenar os erros encontrados.
    erros = []

    # Verifica se o nome tem menos de 5 caracteres,
    # mais de 30 caracteres ou contém somente números.
    if len(nome) < 5 or len(nome) > 30 or nome.isdigit():
        erros.append("Nome: de 5 a 30 caracteres, não só números.")

    # Verifica se a descrição ultrapassa 100 caracteres.
    if len(descricao) > 100:
        erros.append("Descrição: no máximo 100 caracteres.")

    # Verifica se a categoria tem menos de 5 caracteres,
    # mais de 30 caracteres ou contém somente números.
    if len(categoria) < 5 or len(categoria) > 30 or categoria.isdigit():
        erros.append("Categoria: de 5 a 30 caracteres, não só números.")

    # Verifica se a prioridade é uma das três opções permitidas.
    if prioridade not in ("ALTA", "MEDIA", "BAIXA"):
        erros.append("Prioridade inválida.")

    # Tenta converter o prazo recebido em uma data válida.
    try:
        data = date.fromisoformat(prazo)

        # Verifica se a data informada é anterior à data atual.
        if data < date.today():
            erros.append("Prazo: a data não pode ser no passado")

    # Caso a conversão da data apresente erro, executa este bloco.
    except ValueError:
        erros.append("Prazo: informe uma data válida")

    # Devolve a lista com os erros encontrados.
    # Se estiver vazia, significa que não existem erros.
    return erros


# ---------------------------------------------------------
# ROTA DA PÁGINA INICIAL
# ---------------------------------------------------------

# Define a rota "/" como endereço da página inicial.
@app.route("/")
def index():

    # Verifica se a chave "login" não existe na sessão.
    # Se não existir, significa que o usuário não está logado.
    if "login" not in session:

        # Redireciona o usuário para a página de login.
        return redirect("/login")

    # Consulta as tarefas armazenadas no banco de dados.
    tarefas = consultar_tarefas()

    # Envia as tarefas para o arquivo index.html.
    return render_template("index.html", tarefas=tarefas)


# ---------------------------------------------------------
# ROTA DE LOGIN
# ---------------------------------------------------------

# Define a rota "/login" e permite requisições GET e POST.
@app.route("/login", methods=["GET", "POST"])
def login():

    # Verifica se o usuário já está logado.
    if "login" in session:

        # Se já estiver logado, redireciona para a página inicial.
        return redirect("/")

    # Verifica se a requisição é GET.
    if request.method == "GET":

        # Exibe a página de login.
        return render_template("login.html")

    # Se não for GET, será tratada como POST.
    # Obtém o e-mail digitado no formulário.
    email = request.form.get("email")

    # Obtém a senha digitada no formulário.
    senha = request.form.get("senha")

    # Compara os dados informados com os dados do administrador.
    if email == ADM_EMAIL and senha == ADM_SENHA:

        # Cria a chave "login" na sessão e atribui o valor True.
        session["login"] = True

        # Redireciona o usuário para a página inicial.
        return redirect("/")

    else:
        # Se os dados estiverem incorretos, exibe novamente
        # a página de login com uma mensagem de erro.
        return render_template(
            "login.html",
            msgerro="ERRO: Email OU Senha INCORRETOS!"
        )


# ---------------------------------------------------------
# ROTA DE LOGOUT
# ---------------------------------------------------------

# Define a rota responsável por sair da conta.
@app.route("/logout")
def logout():

    # Limpa todas as informações armazenadas na sessão.
    session.clear()

    # Redireciona o usuário para a página de login.
    return redirect("/login")


# ---------------------------------------------------------
# TRATAMENTO DE ERRO 404
# ---------------------------------------------------------

# Identifica quando acontece um erro HTTP 404.
# Esse erro significa que a página solicitada não foi encontrada.
@app.errorhandler(404)
def not_found(erro):

    # Exibe uma página personalizada para o erro 404.
    return render_template("erro404.html")


# ---------------------------------------------------------
# ROTA PARA ADICIONAR TAREFAS
# ---------------------------------------------------------

# Define a rota "/adicionar".
# GET: abre o formulário.
# POST: recebe os dados enviados pelo formulário.
@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():

    # Verifica se o usuário está apenas acessando a página.
    if request.method == "GET":

        # Exibe o formulário HTML.
        # Envia a lista de categorias, dados vazios e uma lista
        # de erros vazia para a página.
        return render_template(
            "formulario.html",
            categorias=CATEGORIAS,
            dados={},
            erros=[]
        )

    # -----------------------------------------------------
    # POST: RECEBENDO OS DADOS DO FORMULÁRIO
    # -----------------------------------------------------

    # Obtém o nome da tarefa enviado pelo formulário.
    # strip() remove espaços em branco do início e do final.
    nome_tarefa = request.form.get("nome_tarefa", "").strip()

    # Obtém a descrição e remove os espaços das extremidades.
    descricao = request.form.get("descricao", "").strip()

    # Obtém a categoria e remove os espaços das extremidades.
    categoria = request.form.get("categoria", "").strip()

    # Obtém a data de prazo informada pelo usuário.
    data_prazo = request.form.get("data_prazo", "")

    # Obtém a prioridade selecionada.
    prioridade = request.form.get("prioridade", "")

    # -----------------------------------------------------
    # VALIDANDO OS DADOS
    # -----------------------------------------------------

    # Chama a função validar_tarefa e envia os cinco campos.
    # A função verifica se as informações estão corretas.
    # Os erros encontrados são armazenados na variável erros.
    erros = validar_tarefa(
        nome_tarefa,
        descricao,
        categoria,
        data_prazo,
        prioridade
    )

    # Verifica se a lista de erros contém alguma informação.
    if erros:

        # Se houver erros, exibe novamente o formulário.
        # categorias: disponibiliza as opções de categoria.
        # dados: mantém as informações que o usuário digitou.
        # erros: envia as mensagens de erro para o HTML.
        return render_template(
            "formulario.html",
            categorias=CATEGORIAS,
            dados=request.form,
            erros=erros
        )

    # -----------------------------------------------------
    # SALVANDO A TAREFA NO BANCO DE DADOS
    # -----------------------------------------------------

    # Chama a função inserir_tarefa e envia os dados da tarefa.
    # Verifica se a função conseguiu inserir a tarefa no banco.
    if inserir_tarefa(
        nome_tarefa,
        descricao,
        categoria,
        data_prazo,
        prioridade
    ):

        # Se a inserção funcionar, armazena uma mensagem de sucesso.
        flash("Tarefa adicionada com sucesso!")

    else:

        # Se a inserção falhar, armazena uma mensagem de erro.
        flash("Não foi possível salvar. Confira a conexão com o banco.")

    # Após tentar salvar, redireciona o usuário para a página inicial.
    return redirect("/")

@app.route("/concluir/<int:idtarefa>", methods=["POST"])
def concluir(idtarefa):


# ---------------------------------------------------------
# EXECUÇÃO DA APLICAÇÃO
# ---------------------------------------------------------

# Verifica se este arquivo está sendo executado diretamente.
# Isso evita que o servidor seja iniciado quando o arquivo
# for importado por outro arquivo Python.
if __name__ == "__main__":

    # Inicia o servidor Flask.
    # debug=True ativa o modo de depuração.
    # port=5000 define a porta utilizada pela aplicação.
    app.run(debug=True, port=5000)