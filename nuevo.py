from flask import render_template, request, redirect, flash, url_for, session
from config import conectar_bd

# Verificar que el nombre del peluche sea único
def manejar_nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip().lower()
        descripcion = request.form['descripcion']
        dueno_id = session.get('usuario_id')

        connection = conectar_bd()
        try:
            with connection.cursor() as cursor:
                # Revisar si ya existe un peluche con el mismo nombre
                cursor.execute("SELECT * FROM peluches WHERE LOWER(nombre) = %s", (nombre,))
                peluche_existente = cursor.fetchone()
                if peluche_existente:
                    flash('Ya existe un peluche con ese nombre. Por favor elige otro.', 'error')
                    return render_template('nuevo.html', nombre=nombre, descripcion=descripcion)

                # Insertar el nuevo peluche en la base de datos
                cursor.execute("""
                    INSERT INTO peluches (nombre, descripcion, dueno_id)
                    VALUES (%s, %s, %s)
                """, (nombre, descripcion, dueno_id))
                connection.commit()

                flash('Peluche registrado exitosamente.', 'success')
                return redirect(url_for('dashboard'))
        finally:
            connection.close()

    return render_template('nuevo.html')
