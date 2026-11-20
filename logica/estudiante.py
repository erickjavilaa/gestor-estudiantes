"""Clase Estudiante: representa a un estudiante del IEST."""


class Estudiante:
    """Guarda los datos de un estudiante."""

    def __init__(self, nombre, id_iest, carrera, semestre, correo):
        self.nombre = nombre
        self.id_iest = id_iest
        self.carrera = carrera
        self.semestre = semestre
        self.correo = correo

    def a_dict(self):
        """Convierte el estudiante a diccionario (para guardarlo en JSON)."""
        return {
            "nombre": self.nombre,
            "id_iest": self.id_iest,
            "carrera": self.carrera,
            "semestre": self.semestre,
            "correo": self.correo,
        }

    @classmethod
    def desde_dict(cls, datos):
        """Crea un Estudiante a partir de un diccionario."""
        return cls(
            datos.get("nombre", ""),
            datos.get("id_iest", ""),
            datos.get("carrera", ""),
            datos.get("semestre", ""),
            datos.get("correo", ""),
        )

    def __str__(self):
        return f"{self.nombre} ({self.id_iest})"
