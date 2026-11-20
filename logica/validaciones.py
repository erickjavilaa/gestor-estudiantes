"""Validaciones de los datos del estudiante.

Cada función lanza ValueError con un mensaje claro si el dato es inválido
(la interfaz lo muestra en un messagebox) y devuelve el dato limpio si es válido.
"""

import re

CARRERAS = [
    "Ingeniería en Sistemas",
    "Ingeniería Industrial",
    "Ingeniería Mecatrónica",
    "Ingeniería Civil",
    "Administración",
    "Otra",
]


def validar_nombre(nombre):
    nombre = str(nombre).strip()
    if nombre == "":
        raise ValueError("El nombre no puede estar vacío")
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s.'-]+", nombre):
        raise ValueError("El nombre solo puede contener letras y espacios")
    return nombre


def validar_id(id_iest):
    id_iest = str(id_iest).strip()
    if id_iest == "":
        raise ValueError("El ID IEST no puede estar vacío")
    if not id_iest.isalnum():
        raise ValueError("El ID IEST solo puede contener letras y números")
    return id_iest


def validar_carrera(carrera):
    carrera = str(carrera).strip()
    if carrera == "":
        raise ValueError("La carrera no puede estar vacía")
    return carrera


def validar_semestre(semestre):
    texto = str(semestre).strip()
    if not texto.isdigit():
        raise ValueError("El semestre debe ser un número entero")
    numero = int(texto)
    if not 1 <= numero <= 12:
        raise ValueError("El semestre debe estar entre 1 y 12")
    return numero


def validar_correo(correo):
    correo = str(correo).strip()
    if correo == "":
        raise ValueError("El correo no puede estar vacío")
    if not re.fullmatch(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", correo):
        raise ValueError("El correo no tiene un formato válido (ej. usuario@dominio.com)")
    return correo


def validar_estudiante(nombre, id_iest, carrera, semestre, correo):
    """Valida todos los campos. Devuelve una tupla limpia o lanza ValueError."""
    return (
        validar_nombre(nombre),
        validar_id(id_iest),
        validar_carrera(carrera),
        validar_semestre(semestre),
        validar_correo(correo),
    )
