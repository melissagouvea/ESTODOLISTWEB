from datetime import date 
from flask import Flask, render_template, request, session, redirect, flash
from database import consultar_tarefas, inserir_tarefa

app = Flask(__name__)
app.secret_key = "senai" #exigencia para toda vez que se cria a sessão


ADM_EMAIL = "123@gmail.com"
ADM_SENHA = "123"
CATEGORIAS = ["Escola","Trabalho","Projetos","Pessoal","Saúde","Outros"]

#---------------------------------------------------------------------------------------------------------------
def validar_tarefa(nome, descricao, categoria, prazo, prioridade):
    erros = []
    if len(nome) < 5 or len(nome) > 30 or nome.isdigit():
        erros.append("Nome: de 5 a 30 caracteres, não só números.")
    if len(descricao) > 100:
        erros.append("Descrição: no máximo 100 caracteres.")
    if len(categoria) < 5 or len(categoria) > 30 or categoria.isdigit():
        erros.append("Categoria: de 5 a 30 caracteres, não só números.")
    if prioridade not in ("ALTA", "MEDIA", "BAIXA"):
        erros.append("Prioridade inválida.")
    try:
        data = date.fromisoformat(prazo)
        if data < date.today():
            erros.append("Prazo: a data não pode ser no passado")
    except ValueError:
         erros.append("Prazo: informe uma data válida")
    return erros 


#---------------------------------------------------------------------------------------------------------------

@app.route("/") # Home page / Pagina inicial
def index():
    if "login" not in session:
        return redirect("/login")

    #usuário logado
    tarefas = consultar_tarefas()
    return render_template("index.html", tarefas=tarefas)

#rota login
@app.route("/login", methods=["GET","POST"])
def login():
    if "login" in session:
        return redirect("/")
    if request.method == "GET":
        return render_template("login.html")
    # POST
    email = request.form.get("email") #pegando a informação que esta no form
    senha = request.form.get("senha")


    if email == ADM_EMAIL and senha == ADM_SENHA:
        session["login"] = True
        return redirect("/") #redireciona para a rota inicial
    else :
        return render_template("login.html", msgerro = "ERRO: Email OU Senha INCORRETOS!")

#-------------------------------------------------------------------------------------------------------------------------------

#rota logout
@app.route("/logout")
def logout():
    session.clear() #apaga a lista da sessão
    return redirect("/login")

#-------------------------------------------------------------------------------------------------------------------------------

#rota tratamento de erro - código 404
@app.errorhandler(404)
def not_found(erro):
    return render_template("erro404.html")

#-------------------------------------------------------------------------------------------------------------------------------
#rota que mostra o formulário
@app.route("/adicionar",methods=["GET",'POST'])
def adicionar():
    if request.method == "GET":
        return render_template("formulario.html",categorias=CATEGORIAS,dados={}, erros=[])
    
    #POST: LER O QUE VEIO DO FORMULÁRIO
    nome_tarefa = request.form.get("nome_tarefa","").strip()
    descricao = request.form.get("descricao","").strip()
    categoria = request.form.get("categoria","").strip()
    data_prazo = request.form.get("data_prazo","")
    prioridade = request.form.get("prioridade","")

    erros = validar_tarefa(nome_tarefa, descricao, categoria,
                       data_prazo, prioridade)

    if erros:
        return render_template("formulario.html", categorias=CATEGORIAS,
                           dados=request.form, erros=erros)

    if inserir_tarefa(nome_tarefa, descricao, categoria, data_prazo, prioridade):
        flash("Tarefa adicionada com sucesso!")
    else:
        flash("Não foi possível salvar. Confira a conexão com o banco.")
    return redirect("/")

#-------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__": #evita que a pessoa abra o app por outra rota sem ser o host
    app.run(debug=True, port=5000)


    

