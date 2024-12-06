from flask import render_template, request, redirect, flash, url_for, session
from utils import login_required
from config import conectar_bd

@login_required
def manejar_editar(id):
    connection = conectar_bd()
    if request.method == 'POST':
        nuevo_nombre = request.form['nombre'].strip().lower()
        descripcion = request.form['descripcion']
        dueno_id = session.get('usuario_id')

        try:
            with connection.cursor() as cursor:
                # Obtener el nombre original del peluche
                cursor.execute("SELECT nombre FROM peluches WHERE id = %s", (id,))
                peluche_existente = cursor.fetchone()

                if not peluche_existente:
                    flash('Peluche no encontrado.', 'error')
                    return redirect(url_for('dashboard'))

                nombre_original = peluche_existente['nombre']

                # Verificar si el nuevo nombre es diferente al original
                if nuevo_nombre != nombre_original:
                    # Revisar si ya existe un peluche con el mismo nombre
                    cursor.execute("SELECT * FROM peluches WHERE LOWER(nombre) = %s AND id != %s", (nuevo_nombre, id))
                    otro_peluche = cursor.fetchone()
                    if otro_peluche:
                        flash('Ya existe otro peluche con ese nombre. Por favor elige otro.', 'error')
                        return render_template('editar.html', id=id, nombre=nuevo_nombre, descripcion=descripcion)

                # Actualizar el peluche en la base de datos
                cursor.execute("""
                    UPDATE peluches 
                    SET nombre = %s, descripcion = %s 
                    WHERE id = %s
                """, (nuevo_nombre, descripcion, id))
                connection.commit()

                flash('Peluche actualizado correctamente.', 'success')
                return redirect(url_for('dashboard'))
        finally:
            connection.close()
    else:
        try:
            with connection.cursor() as cursor:
                # Obtener los datos actuales del peluche para editar
                cursor.execute("SELECT * FROM peluches WHERE id = %s", (id,))
                peluche = cursor.fetchone()
                if peluche is None:
                    flash('Peluche no encontrado.', 'error')
                    return redirect(url_for('dashboard'))
        finally:
            connection.close()

        # Pasar los datos actuales del peluche a la plantilla editar.html
        return render_template('editar.html', id=peluche['id'], nombre=peluche['nombre'], descripcion=peluche['descripcion'])
