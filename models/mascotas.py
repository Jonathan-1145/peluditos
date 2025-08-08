from peluditos import cursorPeludito

class Mascotas:
    def obtener_todas(self):
        consulta = "SELECT * FROM mascotas"
        cursorPeludito.execute(consulta)
        mascotas = cursorPeludito.fetchall()
        return mascotas