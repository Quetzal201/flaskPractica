from flask import Flask

from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hola, Mundo!</p>"

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar")
def alumnosGuardar():
    return f"Matrícula: {request.form["txtMatriculaFA"]} Nombre y Apellido: {request.form["txtNombreApellido"]}"

app.run(debug=True, port=8080)
