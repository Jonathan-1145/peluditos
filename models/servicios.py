from peluditos import cursorPeludito

class ServiciosPrestados:
    def obtener_todos(self):
        consulta = "SELECT * FROM serviciosprestados"
        cursorPeludito.execute(consulta)
        registros = cursorPeludito.fetchall()
        return registros