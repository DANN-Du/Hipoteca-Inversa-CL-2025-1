import datetime


class Solicitante  :
    def __init__(self,nombre: str,
        identificacion: str,
        fecha_nacimiento: datetime.date,
        edad: int):
        self.nombre: str = nombre
        self.identificacion: str = identificacion
        self.fecha_nacimiento: datetime.date = fecha_nacimiento
        self.edad: int = edad

    def is_equal(self, otra: "Solicitante") -> bool:
        """Compara si dos instancias de la clase solicitante son iguales."""
        if otra is None:
            return False

        return (
            self.nombre == otra.nombre
            and self.identificacion
            == otra.identificacion
            and str(self.fecha_nacimiento)
            == str(otra.fecha_nacimiento)
            and int(self.edad) == int(otra.edad)
        )

    def to_dict(self) -> dict:
        """Convierte la instancia a un diccionario serializable a JSON."""
        return {
            "nombre": self.nombre,
            "identificacion": self.identificacion,
            "fecha_nacimiento": str(self.fecha_nacimiento),
            "edad": int(self.edad)
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Solicitante":
        """Crea una instancia a partir de un diccionario."""
        fecha = data.get("fecha_nacimiento")
        if isinstance(fecha, str):
            try:
                fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
            except ValueError:
                pass
        return cls(
            nombre=data.get("nombre", ""),
            identificacion=str(data.get("identificacion", "")),
            fecha_nacimiento=fecha,
            edad=int(data.get("edad", 0))
        )