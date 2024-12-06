from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', nombre_usuario='Usuario')

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        # Lógica para guardar los datos...
        return redirect(url_for('dashboard'))
    return render_template('nuevo.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        # Lógica para actualizar la donación en la base de datos usando el ID...
        return redirect(url_for('dashboard'))
    
    donacion = {
        'id': id,
        'nombre': 'Pikachu',
        'descripcion': 'Peluche de Pikachu',
        'dueno': 'Miyagi'
    }

    return render_template('editar.html', id=donacion['id'], nombre=donacion['nombre'], descripcion=donacion['descripcion'])

@app.route('/ver/<int:id>')
def ver(id):
    # Supongamos que estamos buscando los datos del peluche por ID
    # Esto es solo un ejemplo, y deberías reemplazarlo con tu lógica real de base de datos
    donacion = {
        'id': id,
        'nombre': 'Gatito Peluchón',
        'dueno': 'Cynthia',
        'descripcion': 'Gatito adorable y muy peludito en color blanco.',
        'adoptado_por': 'Elena',  # Si no ha sido adoptado, este campo podría ser None o ''
        'visitas': 3  # Número de visitas a la página de este peluche
    }

    return render_template('ver.html',
                           nombre=donacion['nombre'],
                           dueno=donacion['dueno'],
                           descripcion=donacion['descripcion'],
                           adoptado_por=donacion.get('adoptado_por', None),
                           visitas=donacion['visitas'])

if __name__ == '__main__':
    app.run(debug=True)
