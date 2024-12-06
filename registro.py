from flask import render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from config import conectar_bd

def manejar_registro():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Validaciones
    if len(nombre) < 2 or len(apellido) < 2:
        flash('Nombre y apellido deben tener al menos 2 caracteres.', 'error')
        return render_template('index.html', nombre=nombre, apellido=apellido, email=email)

    if '@' not in email or '.' not in email:
        flash('El email debe tener un formato válido.', 'error')
        return render_template('index.html', nombre=nombre, apellido=apellido, email=email)

    if password != confirm_password:
        flash('las contraseñas deben coincidir.', 'error')
        return render_template('index.html', nombre=nombre, apellido=apellido, email=email)

    # Verificar si el email ya está registrado
    connection = conectar_bd()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()
            if usuario:
                flash('El email ya está registrado.', 'error')
                return render_template('index.html', nombre=nombre, apellido=apellido, email=email)

            # Registrar al usuario
            hashed_password = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)",
                (nombre, apellido, email, hashed_password)
            )
            connection.commit()
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('index'))
    finally:
        connection.close()
