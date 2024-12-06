from flask import Flask, render_template, request, redirect, url_for
from config import conectar_bd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    connection = conectar_bd()
    try:
        with connection.cursor() as cursor:
            # Seleccionar todos los peluches
            sql = "SELECT * FROM peluches"
            cursor.execute(sql)
            peluches = cursor.fetchall()
        return render_template('dashboard.html', nombre_usuario='Usuario', peluches=peluches)
    finally:
        connection.close()

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        connection = conectar_bd()
        try:
            with connection.cursor() as cursor:
                # Insertar un nuevo peluche
                sql = "INSERT INTO peluches (nombre, descripcion) VALUES (%s, %s)"
                cursor.execute(sql, (nombre, descripcion))
                connection.commit()
        finally:
            connection.close()
        return redirect(url_for('dashboard'))
    return render_template('nuevo.html')

if __name__ == '__main__':
    app.run(debug=True)
