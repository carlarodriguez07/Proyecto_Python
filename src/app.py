from flask import Flask, render_template, request, redirect, url_for,flash
import database as db
import os
import mysql.connector

database = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='recetas'
)
secret_key = os.urandom(24)

template_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(template_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = secret_key


#RUTA PARA MOSTRAR LAS RECETAS

@app.route('/')
def home():
    cursor = database.cursor(dictionary=True)
    cursor.execute("SELECT * FROM recetas")
    recetas = cursor.fetchall()
    cursor.close()
    return render_template('tureceta.html',data=recetas)


#RUTA PARA AGREGAR LAS RECETAS
@app.route('/store', methods=['POST'])
def agregar_receta():
    nombre = request.form['nombre_receta']
    ingredientes = request.form['ingredientes']
    pasos = request.form['pasos_receta']
    tipo = request.form['tipo_receta']
    tiempo = request.form['tiempo_elaboracion']

    if nombre and ingredientes and pasos and tipo and tiempo:
        cursor = database.cursor()
        sql = "INSERT INTO recetas (nombre_receta, ingredientes, pasos_receta, tipo_receta, tiempo_elaboracion) VALUES (%s, %s, %s, %s, %s)"
        data = (nombre, ingredientes, pasos, tipo, tiempo)
        cursor.execute(sql, data)
        database.commit()
        cursor.close()
        flash('Receta agregada correctamente', 'success')
    else:
        flash('Todos los campos son obligatorios', 'error')

    return redirect(url_for('home'))

#RUTA PARA ELIMINAR
@app.route('/eliminar_receta/<int:id>', methods=['POST'])
def eliminar_receta(id):
    if request.method == 'POST':
        cursor = database.cursor()
        sql = "DELETE FROM recetas WHERE id_receta = %s"
        data = (id,)
        cursor.execute(sql, data)
        database.commit()
        cursor.close()

    return redirect(url_for('home'))

#RUTA PARA EDITAR
@app.route('/editar_receta/<int:id>', methods=['GET'])
def editar_receta(id):
    cursor = database.cursor(dictionary=True)
    cursor.execute("SELECT * FROM recetas WHERE id_receta = %s", (id,))
    receta = cursor.fetchone()
    cursor.close()
    return render_template('editar_receta.html', receta=receta)

# RUTA PARA ACTUALIZAR
@app.route('/actualizar_receta/<int:id>', methods=['POST'])
def actualizar_receta(id):
    nombre = request.form['nombre_receta']
    ingredientes = request.form['ingredientes']
    pasos = request.form['pasos_receta']
    tipo = request.form['tipo_receta']
    tiempo = request.form['tiempo_elaboracion']

    cursor = database.cursor()
    sql = "UPDATE recetas SET nombre_receta = %s, ingredientes = %s, pasos_receta = %s, tipo_receta = %s, tiempo_elaboracion = %s WHERE id_receta = %s"
    data = (nombre, ingredientes, pasos, tipo, tiempo, id)
    cursor.execute(sql, data)
    database.commit()
    cursor.close()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)