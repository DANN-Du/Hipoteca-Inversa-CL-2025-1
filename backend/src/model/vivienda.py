class Vivienda  :
    def __init__(self,
        ciudad: str,
        barrio: str,
        direccion: str,
        identificacion_propietario: str,
        valor: float):
        self.ciudad: str = ciudad
        self.barrio: str = barrio
        self.direccion: str = direccion
        self.identificacion_propietario: str = identificacion_propietario
        self.valor: float = valor

    def is_equal(self, otra: 'Vivienda') -> bool:
        """Compara si dos instancias de la clase vivienda son iguales."""
        if otra is None:
            return False

        return (
            self.ciudad == otra.ciudad
            and self.barrio == otra.barrio
            and self.direccion == otra.direccion
            and self.identificacion_propietario == otra.identificacion_propietario
            and float(self.valor) == float(otra.valor)
        )

    def to_dict(self) -> dict:
        """Convierte la instancia a un diccionario serializable a JSON."""
        return {
            "ciudad": self.ciudad,
            "barrio": self.barrio,
            "direccion": self.direccion,
            "identificacion_propietario": self.identificacion_propietario,
            "valor": float(self.valor)
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Vivienda":
        """Crea una instancia a partir de un diccionario."""
        return cls(
            ciudad=data.get("ciudad", ""),
            barrio=data.get("barrio", ""),
            direccion=data.get("direccion", ""),
            identificacion_propietario=str(data.get("identificacion_propietario", "")),
            valor=float(data.get("valor", 0.0))
        )