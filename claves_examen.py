from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

# Inicializa la base de datos
def init_db():
    conn = sqlite3.connect('usuarios_hash.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            contrasena_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Ruta principal
@app.route('/')
def home():
    return "Servidor operativo en puerto 5800"

# Ruta para registrar usuarios (con hash)
@app.route('/registro', methods=['POST'])
def registrar():
    nombre = request.form.get('nombre')
    contrasena = request.form.get('contrasena')

    if not nombre or not contrasena:
        return jsonify({'mensaje': 'Faltan datos'}), 400

    contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()

    try:
        conn = sqlite3.connect('usuarios_hash.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nombre, contrasena_hash) VALUES (?, ?)', (nombre, contrasena_hash))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': f'Usuario {nombre} registrado con hash'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'mensaje': 'El usuario ya existe'}), 409

# Ruta para login (verifica hash)
@app.route('/login', methods=['POST'])
def login():
    nombre = request.form.get('nombre')
    contrasena = request.form.get('contrasena')

    contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()

    conn = sqlite3.connect('usuarios_hash.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nombre = ? AND contrasena_hash = ?', (nombre, contrasena_hash))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        return jsonify({'mensaje': f'Bienvenido, {nombre}!'}), 200
    else:
        return jsonify({'mensaje': 'Credenciales incorrectas'}), 401

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5800)
