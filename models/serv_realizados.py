from peluditos import cursorPeludito

class Servicios:
    def obtener_todos(self):
        consulta = "SELECT * FROM servicios"
        cursorPeludito.execute(consulta)
        servicios = cursorPeludito.fetchall()
        return servicios