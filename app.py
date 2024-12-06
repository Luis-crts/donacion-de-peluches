from flask import Flask, render_template, redirect, url_for, request, flash, session
from registro import manejar_registro
from login import manejar_login
from nuevo import manejar_nuevo
from utils import login_required
from config import conectar_bd

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

if __name__ == '__main__':
    app.run(debug=True)

