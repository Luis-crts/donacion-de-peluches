from flask import Flask, render_template, redirect, url_for, request, flash, session
from registro import manejar_registro
from login import manejar_login
from nuevo import manejar_nuevo
from utils import login_required
from config import conectar_bd
from editar import manejar_editar


app = Flask(__name__)
app.secret_key = 'tu_secreto'  # Necesario para flash

@app.route('/dashboard')
@login_required
def dashboard():
    connection = conectar_bd()
    try:
        with connection.cursor() as cursor:
            # Utilizamos JOIN para obtener el nombre del usuario que donó cada peluche
            cursor.execute("""
                SELECT p.id, p.nombre, p.descripcion, u.nombre AS donador
                FROM peluches p
                JOIN usuarios u ON p.dueno_id = u.id
            """)
            peluches = cursor.fetchall()
    finally:
        connection.close()

    # Pasar los datos de los peluches a la plantilla dashboard.html
    return render_template('dashboard.html', peluches=peluches, nombre_usuario=session.get('nombre_usuario'))



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    return manejar_registro()

@app.route('/login', methods=['POST'])
def login():
    return manejar_login()

@app.route('/logout')
def logout():
    session.clear()  # Limpia toda la sesión
    flash('Sesión cerrada exitosamente.', 'success')
    return redirect(url_for('index'))

@app.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    return manejar_nuevo()

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    return manejar_editar(id)

@app.route('/ver/<int:id>', methods=['GET'])
@login_required
def ver(id):
    connection = conectar_bd()
    try:
        with connection.cursor() as cursor:
            # Obtener los datos del peluche por su id
            cursor.execute("SELECT p.*, u.nombre AS dueno FROM peluches p JOIN usuarios u ON p.dueno_id = u.id WHERE p.id = %s", (id,))
            peluche = cursor.fetchone()
            if peluche is None:
                flash('Peluche no encontrado.', 'error')
                return redirect(url_for('dashboard'))
    finally:
        connection.close()

    # Pasar los datos del peluche a la plantilla ver.html
    return render_template('ver.html', nombre=peluche['nombre'], descripcion=peluche['descripcion'], dueno=peluche['dueno'], visitas=peluche['visitas'], adoptado_por=peluche.get('adoptado_por'))



if __name__ == '__main__':
    app.run(debug=True)

