from datetime import timedelta
from random import randint
from flask import Flask, redirect, render_template, request, session
import mysql.connector
import hashlib
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=60)

bddPeluditos = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",
    database="peluditos"
)
cursorPeludito = bddPeluditos.cursor()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        cifra_contra = hashlib.sha512(clave.encode()).hexdigest()

        cursor = bddPeluditos.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE nombre=%s AND contrasena=%s", (usuario, cifra_contra))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session.permanent = True
            session['usuario'] = user['nombre']
            session['rol'] = user['rol']
            return redirect('/dashboard')
        else:
            return "Credenciales incorrectas"

    return render_template('usuarios.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'usuario' not in session:
        return redirect('/')

    rol = session.get('rol')

    if rol == 1:
        return render_template('admin.html', usuario=session['usuario'])
    elif rol == 2:
        return render_template('operador.html', usuario=session['usuario'])
    else:
        return "Rol desconocido"

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)