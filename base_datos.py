import sqlite3


class BaseDatos:

    def __init__(self, nombre="sistema.db"):
        self.nombre = nombre
        self.crear_tablas()

    def conectar(self):
        return sqlite3.connect(self.nombre)

    def crear_tablas(self):

        conexion = self.conectar()
        cursor = conexion.cursor()

        # Tabla de vehículos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                anio INTEGER NOT NULL,
                patente TEXT NOT NULL
            )
        """)

        # Tabla de propietarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS propietarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                dni TEXT NOT NULL,
                telefono TEXT NOT NULL
            )
        """)

        conexion.commit()
        conexion.close()

    def insertar(self, tabla, campos, valores):

        conexion = self.conectar()
        cursor = conexion.cursor()

        nombres = ", ".join(campos)
        signos = ", ".join(["?"] * len(valores))

        consulta = f"""
            INSERT INTO {tabla} ({nombres})
            VALUES ({signos})
        """

        cursor.execute(consulta, valores)

        conexion.commit()
        conexion.close()

    def consultar(self, tabla):

        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute(f"SELECT * FROM {tabla}")

        datos = cursor.fetchall()

        conexion.close()

        return datos

    def modificar(self, tabla, campos, valores, id_registro):

        conexion = self.conectar()
        cursor = conexion.cursor()

        modificaciones = ", ".join(
            [f"{campo} = ?" for campo in campos]
        )

        consulta = f"""
            UPDATE {tabla}
            SET {modificaciones}
            WHERE id = ?
        """

        cursor.execute(
            consulta,
            valores + [id_registro]
        )

        conexion.commit()
        conexion.close()

    def eliminar(self, tabla, id_registro):

        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute(
            f"DELETE FROM {tabla} WHERE id = ?",
            (id_registro,)
        )

        conexion.commit()
        conexion.close()