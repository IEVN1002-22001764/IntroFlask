from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    titulo = 'Hola'
    lista=['Karim', 'Mar', 'Danwars']
    return render_template('index.html',titulo=titulo,lista=lista)

@app.route("/distancia")
def distancia(): # <-- Nombre único
     return render_template("distancia.html")

@app.route("/operasbas", methods=["GET","POST"])
def operasbas(): 
    n1=0
    n2=0
    res=0
    operacion=""
    if request.method=="POST":
        n1=request.form.get("n1")
        n2=request.form.get("n2")
        if request.form.get("operacion")=="suma":
            res=float(n1)+float(n2)

    return render_template("operasbas.html",n1=n1, n2=n2, res=res)

@app.route("/Hola")
def saludos(): # <-- Nombre único
    return "<h3> Saludos desde Hola </h3>"

@app.route("/user/<string:user>")
def user(user): 
    return "Hola " + user

@app.route("/numero/<int:n>")
def numero(n):
    return "Numero: {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return "ID: {} nombre: {}".format(id, username)

@app.route("/suma/<float:n1>/<float:n2>")
def func(n1, n2):
    return "La suma es: {}".format(n1 + n2)

if __name__ == "__main__":
    app.run(debug=True)