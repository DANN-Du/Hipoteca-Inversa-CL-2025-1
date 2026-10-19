import os
import sys
sys.path.append("src")
sys.path.append(".")

from model.vivienda import Vivienda
import psycopg2

try:
    import secret_config
except ImportError:
    secret_config = None


class ControladorVivienda:

    @staticmethod
    def crear_tabla():
        cursor = ControladorVivienda.obtener_cursor()
        posibles_rutas = [
            "sql/crear_tabla_viviendas.sql",
            "../sql/crear_tabla_viviendas.sql",
            "backend/sql/crear_tabla_viviendas.sql"
        ]
        sql = None
        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                with open(ruta, "r", encoding="utf-8") as archivo_sql:
                    sql = archivo_sql.read()
                break

        if not sql:
            sql = """
            CREATE TABLE IF NOT EXISTS viviendas (
                ciudad VARCHAR(100) NOT NULL,
                barrio VARCHAR(100) NOT NULL,
                direccion VARCHAR(200) NOT NULL,
                identificacion_propietario VARCHAR(20) NOT NULL,
                valor DECIMAL(15,2) NOT NULL,
                PRIMARY KEY (direccion),
                FOREIGN KEY (identificacion_propietario) REFERENCES solicitantes(identificacion)
            );
            """
        cursor.execute(sql)
        cursor.connection.commit()

    @staticmethod
    def eliminar_tabla():
        cursor = ControladorVivienda.obtener_cursor()
        sql = "DROP TABLE IF EXISTS viviendas CASCADE;"
        cursor.execute(sql)
        cursor.connection.commit()

    @staticmethod
    def borrar_datos_tabla():
        cursor = ControladorVivienda.obtener_cursor()
        sql = "DELETE FROM viviendas;"
        cursor.execute(sql)
        cursor.connection.commit()

    @staticmethod
    def insertar(vivienda: Vivienda):
        """Recibe una instancia de la clase Vivienda y la inserta en la tabla respectiva."""
        cursor = ControladorVivienda.obtener_cursor()
        consulta = "INSERT INTO viviendas (ciudad, barrio, direccion, identificacion_propietario, valor) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(consulta, (vivienda.ciudad, vivienda.barrio, vivienda.direccion, vivienda.identificacion_propietario, vivienda.valor))
        cursor.connection.commit()

    @staticmethod
    def buscar_por_direccion(direccion_vivienda: str) -> Vivienda:
        """Retorna una instancia de la clase Vivienda con los datos obtenidos de la BD
        a partir de la direccion de forma parametrizada y segura."""
        cursor = ControladorVivienda.obtener_cursor()
        consulta = "SELECT ciudad, barrio, direccion, identificacion_propietario, valor FROM viviendas WHERE direccion = %s"
        cursor.execute(consulta, (direccion_vivienda,))
        fila = cursor.fetchone()
        if fila is None:
            return None

        return Vivienda(ciudad=fila[0], barrio=fila[1], direccion=fila[2], identificacion_propietario=fila[3], valor=float(fila[4]))

    @staticmethod
    def buscar_por_propietario(identificacion_propietario: str) -> list:
        """Retorna una lista de instancias de la clase Vivienda a partir de la identificacion
        del propietario de forma parametrizada y segura."""
        cursor = ControladorVivienda.obtener_cursor()
        consulta = "SELECT ciudad, barrio, direccion, identificacion_propietario, valor FROM viviendas WHERE identificacion_propietario = %s"
        cursor.execute(consulta, (identificacion_propietario,))
        filas = cursor.fetchall()
        if not filas:
            return []
        resultados = []
        for fila in filas:
            vivienda = Vivienda(ciudad=fila[0], barrio=fila[1], direccion=fila[2], identificacion_propietario=fila[3], valor=float(fila[4]))
            resultados.append(vivienda)
        return resultados

    @staticmethod
    def listar_todas() -> list:
        """Retorna una lista con todas las viviendas registradas en la base de datos."""
        cursor = ControladorVivienda.obtener_cursor()
        consulta = "SELECT ciudad, barrio, direccion, identificacion_propietario, valor FROM viviendas ORDER BY direccion ASC"
        cursor.execute(consulta)
        filas = cursor.fetchall()
        if not filas:
            return []
        return [
            Vivienda(ciudad=fila[0], barrio=fila[1], direccion=fila[2], identificacion_propietario=fila[3], valor=float(fila[4]))
            for fila in filas
        ]

    @staticmethod
    def modificar_datos(vivienda: Vivienda):
        """Actualiza los datos de una vivienda existente identificada por su direccion."""
        cursor = ControladorVivienda.obtener_cursor()
        consulta = "UPDATE viviendas SET ciudad = %s, barrio = %s, identificacion_propietario = %s, valor = %s WHERE direccion = %s"
        cursor.execute(consulta, (vivienda.ciudad, vivienda.barrio, vivienda.identificacion_propietario, vivienda.valor, vivienda.direccion))
        if cursor.rowcount == 0:
            cursor.connection.rollback()
            raise ValueError(f"No existe vivienda con direccion {vivienda.direccion}")
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
