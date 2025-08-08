from datetime import timedelta
import hashlib
from flask import Flask, render_template, request, redirect, session
import mysql.connector
from random import randint

app = Flask(__name__)
app.secret_key = str(randint(100000, 99999))
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
        clave_cifrada = hashlib.sha512(clave.encode()).hexdigest()

        cursor = bddPeluditos.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE nombre = %s AND contrasena = %s", (usuario, clave_cifrada))
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

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect('/')
    
    rol = session['rol']

    if rol == 1:
        return render_template('admin.html', usuario=session['usuario'])
    elif rol == 2:
        return render_template('operador.html', usuario=session['usuario'])
    else:
        return "Rol desconocido"

@app.route('/clientes')
def clientes():
    if 'usuario' in session:
        return render_template('clientes.html', usuario=session['usuario'])
    else:
        return redirect('/')

@app.route('/mascotas')
def mascotas():
    if 'usuario' in session:
        return render_template('mascotas.html', usuario=session['usuario'])
    else:
        return redirect('/')

@app.route('/servicios')
def servicios():
    if 'usuario' in session:
        return render_template('servicios.html', usuario=session['usuario'])
    else:
        return redirect('/')

@app.route('/serv_realizados')
def serv_realizados():
    if 'usuario' in session:
        return render_template('serv_realizados.html', usuario=session['usuario'])
    else:
        return redirect('/')

@app.route('/usuarios')
def usuarios():
    if 'usuario' in session and session['rol'] == 1:
        return render_template('usuarios.html', usuario=session['usuario'])
    else:
        return "Acceso solo para administrador"

if __name__ == '__main__':
    app.run(debug=True)