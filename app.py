from flask import Flask, render_template, redirect, url_for
from registro import manejar_registro
from login import manejar_login  # En caso de que tengas otra funcionalidad para login

app = Flask(__name__)
app.secret_key = 'tu_secreto'  # Necesario para flash

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    return manejar_registro()

@app.route('/login', methods=['POST'])
def login():
    return manejar_login()  # Esto debería estar en un archivo llamado login.py

if __name__ == '__main__':
    app.run(debug=True)

