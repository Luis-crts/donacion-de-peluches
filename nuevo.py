from flask import render_template, request, flash, redirect, url_for, session
from config import conectar_bd

def manejar_nuevo():
    # Verificar si el usuario está logueado
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        dueno_id = session['user_id']  # Obtiene el ID del usuario logueado

        if not nombre or not descripcion:
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('nuevo.html')

        connection = conectar_bd()
        try:
            with connection.cursor() as cursor:
                # Insertar nuevo peluche en la base de datos
                sql = "INSERT INTO peluches (nombre, descripcion, dueno_id) VALUES (%s, %s, %s)"
                cursor.execute(sql, (nombre, descripcion, dueno_id))
                connection.commit()
                flash('Peluche donado exitosamente.', 'success')
                return redirect(url_for('dashboard'))
        finally:
            connection.close()

    return render_template('nuevo.html')