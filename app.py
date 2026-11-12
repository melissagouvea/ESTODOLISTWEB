from flask import Flask, render_template, request, session, redirect
from database import consultar_tarefas

app = Flask(__name__)
app.secret_key = "senai" #exigencia para toda vez que se cria a sessão


ADM_EMAIL = "123@gmail.com"
ADM_SENHA = "123"

@app.route("/") # Home page / Pagina inicial
def index():
    if "login" not in session:
        return redirect("/login")

    #usuário logado
    tarefas = consultar_tarefas()
    return render_template("index.html", tarefas = tarefas)

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

if __name__ == "__main__": #evita que a pessoa abra o app por outra rota sem ser o host
    app.run(debug=True, port=5000)

