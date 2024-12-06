from flask import render_template, request, flash, redirect, url_for
from werkzeug.security import check_password_hash
from config import conectar_bd

def manejar_login():
    email = request.form['email']
    password = request.form['password']

    connection = conectar_bd()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()

            if not usuario:
                flash('El email no está registrado.', 'error')
                return redirect(url_for('index'))

            if not check_password_hash(usuario['password'], password):
                flash('La contraseña es incorrecta.', 'error')
                return redirect(url_for('index'))

            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('dashboard'))
    finally:
        connection.close()
