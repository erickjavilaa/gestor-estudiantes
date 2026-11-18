"""Gestor de estudiantes: lectura/escritura en JSON y operaciones CRUD.

"""

import json
import os

from logica.estudiante import Estudiante


class GestorEstudiantes:
    """Administra los estudiantes y los guarda en un archivo JSON."""

    def __init__(self, ruta_json="datos/estudiantes.json"):
        self.ruta_json = ruta_json
        self.estudiantes = {}  # clave: id_iest, valor: Estudiante
        self.cargar()

    # ---------- Persistencia ----------
    def cargar(self):
        """Lee el JSON. Si no existe, está vacío o dañado, empieza vacío."""
        self.estudiantes = {}
        if not os.path.exists(self.ruta_json):
            return

        try:
            with open(self.ruta_json, "r", encoding="utf-8") as archivo:
                contenido = archivo.read().strip()
            if contenido == "":
                return
            datos = json.loads(contenido)
        except json.JSONDecodeError:
            # JSON dañado: se conserva una copia para no perder lo que había
            os.replace(self.ruta_json, self.ruta_json + ".bak")
            return
        except OSError as error:
            raise ValueError(f"No se pudo leer el archivo de datos: {error}")

        if not isinstance(datos, list):
            os.replace(self.ruta_json, self.ruta_json + ".bak")
            return

        for item in datos:
            if isinstance(item, dict):
                estudiante = Estudiante.desde_dict(item)
                # Quitar espacios al ID (también protege ante JSON editado a mano)
                estudiante.id_iest = str(estudiante.id_iest).strip()
                self.estudiantes[estudiante.id_iest] = estudiante

    def guardar_archivo(self):
        """Escribe todos los estudiantes en el JSON."""
        carpeta = os.path.dirname(self.ruta_json)
        try:
            if carpeta:
                os.makedirs(carpeta, exist_ok=True)
            lista = [e.a_dict() for e in self.estudiantes.values()]
            with open(self.ruta_json, "w", encoding="utf-8") as archivo:
                json.dump(lista, archivo, indent=4, ensure_ascii=False)
        except OSError as error:
            raise ValueError(f"No se pudo guardar el archivo de datos: {error}")

    # ---------- CRUD ----------
    def agregar(self, estudiante):
        """Agrega un estudiante. ValueError si el ID ya existe."""
        estudiante.id_iest = str(estudiante.id_iest).strip()
        if estudiante.id_iest in self.estudiantes:
            raise ValueError("El ID ya existe")
        self.estudiantes[estudiante.id_iest] = estudiante
        self.guardar_archivo()

    def buscar(self, id_iest):
        """Devuelve el Estudiante con ese ID, o None si no existe."""
        return self.estudiantes.get(str(id_iest).strip())

    def eliminar(self, id_iest):
        """Elimina un estudiante. ValueError si el ID no existe."""
        id_iest = str(id_iest).strip()
        if id_iest not in self.estudiantes:
            raise ValueError("El ID no existe")
        del self.estudiantes[id_iest]
        self.guardar_archivo()

    def listar(self):
        """Devuelve la lista de todos los estudiantes."""
        return list(self.estudiantes.values())

    # ---------- Reporte ----------
    def exportar_txt(self, ruta="salidas/reporte_estudiantes.txt"):
        """Escribe todos los estudiantes en un archivo de texto legible."""
        carpeta = os.path.dirname(ruta)
        try:
            if carpeta:
                os.makedirs(carpeta, exist_ok=True)
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("REPORTE DE ESTUDIANTES\n")
                archivo.write("=" * 40 + "\n\n")
                if not self.estudiantes:
                    archivo.write("No hay estudiantes registrados.\n")
                for i, e in enumerate(self.listar(), start=1):
                    archivo.write(f"Estudiante {i}\n")
                    archivo.write(f"  Nombre:   {e.nombre}\n")
                    archivo.write(f"  ID IEST:  {e.id_iest}\n")
                    archivo.write(f"  Carrera:  {e.carrera}\n")
                    archivo.write(f"  Semestre: {e.semestre}\n")
                    archivo.write(f"  Correo:   {e.correo}\n")
                    archivo.write("-" * 40 + "\n")
                archivo.write(f"\nTotal: {len(self.estudiantes)}\n")
        except OSError as error:
            raise ValueError(f"No se pudo escribir el reporte: {error}")
        return ruta
