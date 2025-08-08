import os
import mysql.connector
import secrets
import hashlib
from datetime import timedelta
from flask import Flask, redirect, render_template, request, session, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(16))
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=60)

# --------------------
# Conexión a base de datos
# --------------------
def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST").split(":")[0],
        port=int(os.environ.get("DB_HOST").split(":")[1]),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

# --------------------
# Login
# --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        clave_cifrada = hashlib.sha512(clave.encode()).hexdigest()

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM usuarios WHERE nombre = %s AND contrasena = %s",
            (usuario, clave_cifrada)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session.permanent = True
            session['usuario'] = user['nombre']
            session['rol'] = user['rol']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Credenciales incorrectas")

    return render_template('login.html')

# --------------------
# Dashboard
# --------------------
@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    rol = int(session['rol'])

    if rol == 1:
        return render_template('admin.html', usuario=session['usuario'])
    elif rol == 2:
        return render_template('operador.html', usuario=session['usuario'])
    else:
        return "Rol desconocido"

# --------------------
# Secciones protegidas
# --------------------
@app.route('/clientes')
def clientes():
    if 'usuario' in session:
        return render_template('clientes.html', usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/mascotas')
def mascotas():
    if 'usuario' in session:
        return render_template('mascotas.html', usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/servicios')
def servicios():
    if 'usuario' in session:
        return render_template('servicios.html', usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/serv_realizados')
def serv_realizados():
    if 'usuario' in session:
        return render_template('serv_realizados.html', usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/usuarios')
def usuarios():
    if 'usuario' in session and int(session['rol']) == 1:
        return render_template('usuarios.html', usuario=session['usuario'])
    return "Acceso solo para administrador"

# --------------------
# Logout
# --------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --------------------
# Ejecución
# --------------------
if __name__ == '__main__':
    app.run(debug=True)
