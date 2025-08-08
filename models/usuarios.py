from peluditos import cursorPeludito
import hashlib

class Usuarios:
    def login(self, usuario, contrasena):
        contrasena_cifrada = hashlib.sha512(contrasena.encode()).hexdigest()
        consultar = "SELECT * FROM usuarios WHERE nombre = %s AND contrasena = %s"
        cursorPeludito.execute(consultar, (usuario, contrasena_cifrada))
        
        usuario_exist = cursorPeludito.fetchone()
        return usuario_exist

    def todos(self):
        consultar = "SELECT id_usuario, nombre, rol FROM usuarios"
        cursorPeludito.execute(consultar)
        usuarios = cursorPeludito.fetchall()
        return usuarios