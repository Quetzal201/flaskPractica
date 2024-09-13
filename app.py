from flask import Flask

from flask import render_template
from flask import request

import pusher

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/evento")
def evento():
    pusher_client = pusher.Pusher(
        app_id='1767999',
        key='c41e2f5ebe527dbc13ab',
        secret='d98385671bdd57829d94',
        cluster='us2',
        ssl=True
    )
    
    pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
    

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar")
def alumnosGuardar():
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellido"]
    return f"Matrícula: {matricula} Nombre y Apellido: {nombreapellido}"

# app.run(debug=True, port=8080)
