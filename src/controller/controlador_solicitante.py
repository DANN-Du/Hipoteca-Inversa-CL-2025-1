import os
import sys
sys.path.append("src")
sys.path.append(".")

from model.solicitante import Solicitante
import psycopg2

try:
    import secret_config
except ImportError:
    secret_config = None


class ControladorSolicitante:

    @staticmethod
    def crear_tabla():
        cursor = ControladorSolicitante.obtener_cursor()
        posibles_rutas = [
            "sql/crear_tabla_solicitantes.sql",
            "../sql/crear_tabla_solicitantes.sql",
            "backend/sql/crear_tabla_solicitantes.sql"
        ]
        sql = None
        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                with open(ruta, "r", encoding="utf-8") as archivo_sql:
                    sql = archivo_sql.read()
                break

        if not sql:
            sql = """
            CREATE TABLE IF NOT EXISTS solicitantes (
                nombre VARCHAR(100) NOT NULL,
                identificacion VARCHAR(20) PRIMARY KEY NOT NULL,
                fecha_nacimiento DATE NOT NULL,
                edad INT NOT NULL
            );
            """
        cursor.execute(sql)
        cursor.connection.commit()

    @staticmethod
    def eliminar_tabla():
        cursor = ControladorSolicitante.obtener_cursor()
        try:
            cursor.execute("DROP TABLE IF EXISTS viviendas CASCADE;")
        except Exception:
            pass
        sql = "DROP TABLE IF EXISTS solicitantes CASCADE;"
        cursor.execute(sql)
        cursor.connection.commit()

    @staticmethod
    def borrar_datos_tabla():
        cursor = ControladorSolicitante.obtener_cursor()
        sql = "DELETE FROM solicitantes;"
        cursor.execute(sql)
        cursor.connection.commit()

    @staticmethod
    def insertar(solicitante: Solicitante):
        """Recibe una instancia de la clase Solicitante y la inserta en la tabla respectiva."""
        cursor = ControladorSolicitante.obtener_cursor()
        consulta = "INSERT INTO solicitantes (nombre, identificacion, fecha_nacimiento, edad) VALUES (%s, %s, %s, %s)"
        cursor.execute(consulta, (solicitante.nombre, solicitante.identificacion, solicitante.fecha_nacimiento, solicitante.edad))
        cursor.connection.commit()

    @staticmethod
    def buscar_por_cedula(identificacion_solicitante: str) -> Solicitante:
        """Retorna una instancia de la clase Solicitante con los datos obtenidos de la BD
        a partir de la cedula suministrada como parametro de forma parametrizada y segura."""
        cursor = ControladorSolicitante.obtener_cursor()
        consulta = "SELECT nombre, identificacion, fecha_nacimiento, edad FROM solicitantes WHERE identificacion = %s"
        cursor.execute(consulta, (identificacion_solicitante,))
        fila = cursor.fetchone()
        if fila is None:
            return None

        return Solicitante(nombre=fila[0], identificacion=fila[1], fecha_nacimiento=fila[2], edad=fila[3])

    @staticmethod
    def listar_todos() -> list:
        """Retorna la lista de todos los solicitantes registrados en la BD."""
        cursor = ControladorSolicitante.obtener_cursor()
        consulta = "SELECT nombre, identificacion, fecha_nacimiento, edad FROM solicitantes ORDER BY nombre ASC"
        cursor.execute(consulta)
        filas = cursor.fetchall()
        if not filas:
            return []
        return [
            Solicitante(nombre=fila[0], identificacion=fila[1], fecha_nacimiento=fila[2], edad=fila[3])
            for fila in filas
        ]

    @staticmethod
    def modificar_datos(solicitante: Solicitante):
        """Actualiza los datos de un solicitante existente identificado por su cedula."""
        cursor = ControladorSolicitante.obtener_cursor()
        consulta = "UPDATE solicitantes SET nombre = %s, fecha_nacimiento = %s, edad = %s WHERE identificacion = %s"
        cursor.execute(consulta, (solicitante.nombre, solicitante.fecha_nacimiento, solicitante.edad, solicitante.identificacion))
        if cursor.rowcount == 0:
            cursor.connection.rollback()
            raise ValueError(f"No existe solicitante con identificacion {solicitante.identificacion}")
        cursor.connection.commit()

    @staticmethod
    def obtener_cursor():
        """Crea la conexion a la base de datos y retorna un cursor.
        Soporta variables de entorno para Docker y compatibilidad con secret_config.py"""
        host = os.environ.get("DB_HOST", getattr(secret_config, "PGHOST", "localhost"))
        port = int(os.environ.get("DB_PORT", getattr(secret_config, "PGPORT", 5432)))
        database = os.environ.get("DB_NAME", getattr(secret_config, "PGDATABASE", "hipoteca_db"))
        user = os.environ.get("DB_USER", getattr(secret_config, "PGUSER", "postgres"))
        password = os.environ.get("DB_PASSWORD", getattr(secret_config, "PGPASSWORD", "postgres"))

        connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return connection.cursor()