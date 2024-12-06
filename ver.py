from config import conectar_bd
from flask import flash

def manejar_ver(id):
    connection = conectar_bd()
    try:
        with connection.cursor() as cursor:
            # Incrementar el contador de visitas
            cursor.execute("UPDATE peluches SET visitas = visitas + 1 WHERE id = %s", (id,))
            connection.commit()
            
            # Obtener los datos del peluche para mostrar en la página
            cursor.execute("SELECT p.*, u.nombre AS dueno FROM peluches p LEFT JOIN usuarios u ON p.dueno_id = u.id WHERE p.id = %s", (id,))
            peluche = cursor.fetchone()
            if peluche is None:
                flash('Peluche no encontrado.', 'error')
                return None
            return peluche
    finally:
        connection.close()
