from flask import Flask

from flask import render_template
from flask import request

import pusher

import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
  host="185.232.14.52",
  database="u760464709_tst_sep",
  user="u760464709_tst_sep_usr",
  password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()
    return render_template("app.html")


@app.route("/Formulario",methods=["GET"])
def renderizarFormulario():
    con.close()
    return render_template("formulario.html")

@app.route("/EncuestaExperiencia",methods=["GET"])
def renderizarEncuesta():
    con.close()
    return render_template("encuesta.html")

@app.route("/EventoGET",methods=["POST"])
def informacionEncuesta():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()

    nombre_completo = request.form["NombreCompleto"]
    comentario = request.form["Comentario"]
    calificacion = request.form["Calificacion"]
  
    sql = "INSERT INTO tst0_experiencias (Nombre_Apellido, Comentario, Calificacion) VALUES (%s, %s, %s)"
    val = (nombre_completo, comentario, calificacion)
    cursor.execute(sql, val)
    
    con.commit()
    con.close()
      
    pusher_client = pusher.Pusher(
        app_id='1767999',
        key='c41e2f5ebe527dbc13ab',
        secret='d98385671bdd57829d94',
        cluster='us2',
        ssl=True
    )
    
    pusher_client.trigger('my-channel', 'my-event', {'NombreCompleto': nombre_completo, 'Comentario': comentario, 'Calificacion': calificacion})

    return render_template("formulario.html")

@app.route("/instrucciones")
def instrucciones():
    con.close()
    return render_template("instrucciones.html")

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM sensor_log")
    
    registros = cursor.fetchall()

    con.close()

    return registros

@app.route("/buscarComentarios")
def buscarComentarios():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_experiencias")
    
    registros = cursor.fetchall()
    con.close()

    return registros

@app.route("/evento",methods=["GET"])
def evento():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()

    args = request.args
  
    sql = "INSERT INTO sensor_log (Temperatura, Humedad, Fecha_Hora) VALUES (%s, %s, %s)"
    val = (args["temperatura"], args["humedad"], datetime.datetime.now())
    cursor.execute(sql, val)
    
    con.commit()
    con.close()
      
    pusher_client = pusher.Pusher(
        app_id='1767999',
        key='c41e2f5ebe527dbc13ab',
        secret='d98385671bdd57829d94',
        cluster='us2',
        ssl=True
    )
    
    pusher_client.trigger('my-channel', 'my-event', {request.args})

    return args
    

@app.route("/alumnos")
def alumnos():
    con.close()
    return render_template("alumnos.html")

@app.route("/alumnos/guardar")
def alumnosGuardar():
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellido"]
    con.close()
    return f"Matrícula: {matricula} Nombre y Apellido: {nombreapellido}"

# app.run(debug=True, port=8080)
