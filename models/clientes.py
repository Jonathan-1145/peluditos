from peluditos import cursorPeludito

class Clientes:
    def obtener_todos(self):
        consulta = "SELECT * FROM clientes"
        cursorPeludito.execute(consulta)
        clientes = cursorPeludito.fetchall()
        return clientes

