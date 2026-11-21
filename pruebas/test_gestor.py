"""Pruebas automáticas de la capa lógica (GestorEstudiantes).

Cada prueba usa una carpeta temporal, así que NO toca datos/estudiantes.json.
Ejecutar desde la raíz del proyecto:
    python -m unittest discover -s pruebas -v
"""

import json
import os
import sys
import tempfile
import unittest

# Permite importar el paquete `logica` sin importar desde dónde se ejecute
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logica.estudiante import Estudiante
from logica.gestor import GestorEstudiantes


def crear_estudiante(id_iest="123", nombre="Ana Pérez"):
    return Estudiante(nombre, id_iest, "Ingeniería en Sistemas", 3, "ana@correo.com")


class PruebasGestor(unittest.TestCase):
    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        self.ruta = os.path.join(self.carpeta.name, "datos", "estudiantes.json")
        self.gestor = GestorEstudiantes(self.ruta)

    def tearDown(self):
        self.carpeta.cleanup()

    # ---------- Agregar ----------
    def test_agregar_estudiante_nuevo(self):
        self.gestor.agregar(crear_estudiante())
        self.assertEqual(len(self.gestor.listar()), 1)
        self.assertIsNotNone(self.gestor.buscar("123"))

    def test_agregar_id_repetido_lanza_error(self):
        self.gestor.agregar(crear_estudiante())
        with self.assertRaises(ValueError):
            self.gestor.agregar(crear_estudiante(nombre="Otra Persona"))
        self.assertEqual(len(self.gestor.listar()), 1)

    def test_id_con_espacios_se_normaliza(self):
        self.gestor.agregar(crear_estudiante(id_iest=" 123 "))
        self.assertIsNotNone(self.gestor.buscar("123"))
        # y también después de cerrar y reabrir
        otro = GestorEstudiantes(self.ruta)
        self.assertIsNotNone(otro.buscar("123"))

    # ---------- Buscar ----------
    def test_buscar_existente_devuelve_sus_datos(self):
        self.gestor.agregar(crear_estudiante())
        e = self.gestor.buscar("123")
        self.assertEqual(e.nombre, "Ana Pérez")
        self.assertEqual(e.correo, "ana@correo.com")

    def test_buscar_inexistente_devuelve_none(self):
        self.assertIsNone(self.gestor.buscar("999"))

    # ---------- Eliminar ----------
    def test_eliminar_existente(self):
        self.gestor.agregar(crear_estudiante())
        self.gestor.eliminar("123")
        self.assertIsNone(self.gestor.buscar("123"))
        self.assertEqual(self.gestor.listar(), [])

    def test_eliminar_inexistente_lanza_error(self):
        with self.assertRaises(ValueError):
            self.gestor.eliminar("999")

    # ---------- Persistencia ----------
    def test_los_datos_persisten_al_reabrir(self):
        self.gestor.agregar(crear_estudiante("111", "Ana"))
        self.gestor.agregar(crear_estudiante("222", "Luis"))
        reabierto = GestorEstudiantes(self.ruta)  # simula cerrar y abrir el programa
        self.assertEqual(sorted(e.id_iest for e in reabierto.listar()), ["111", "222"])

    def test_eliminar_tambien_persiste(self):
        self.gestor.agregar(crear_estudiante())
        self.gestor.eliminar("123")
        self.assertIsNone(GestorEstudiantes(self.ruta).buscar("123"))

    def test_acentos_y_enie_se_guardan_legibles(self):
        self.gestor.agregar(crear_estudiante(nombre="Ñandú Pérez"))
        with open(self.ruta, encoding="utf-8") as archivo:
            texto = archivo.read()
        self.assertIn("Ñandú Pérez", texto)  # no como \u00d1...
        self.assertEqual(GestorEstudiantes(self.ruta).buscar("123").nombre, "Ñandú Pérez")

    def test_json_creado_con_los_cinco_campos(self):
        self.gestor.agregar(crear_estudiante())
        with open(self.ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)
        self.assertEqual(set(datos[0]),
                         {"nombre", "id_iest", "carrera", "semestre", "correo"})

    # ---------- Archivos problemáticos ----------
    def test_archivo_inexistente_empieza_vacio(self):
        self.assertEqual(self.gestor.listar(), [])

    def test_archivo_vacio_empieza_vacio(self):
        os.makedirs(os.path.dirname(self.ruta), exist_ok=True)
        open(self.ruta, "w", encoding="utf-8").close()
        self.assertEqual(GestorEstudiantes(self.ruta).listar(), [])

    def test_json_danado_no_rompe_y_deja_respaldo(self):
        os.makedirs(os.path.dirname(self.ruta), exist_ok=True)
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            archivo.write("{esto no es json")
        gestor = GestorEstudiantes(self.ruta)
        self.assertEqual(gestor.listar(), [])
        self.assertTrue(os.path.exists(self.ruta + ".bak"))

    # ---------- Reporte de texto ----------
    def test_exportar_txt_genera_el_reporte(self):
        self.gestor.agregar(crear_estudiante("111", "Ana Pérez"))
        self.gestor.agregar(crear_estudiante("222", "Luis Gómez"))
        ruta_txt = os.path.join(self.carpeta.name, "salidas", "reporte.txt")
        self.assertEqual(self.gestor.exportar_txt(ruta_txt), ruta_txt)
        with open(ruta_txt, encoding="utf-8") as archivo:
            contenido = archivo.read()
        self.assertIn("Ana Pérez", contenido)
        self.assertIn("Luis Gómez", contenido)
        self.assertIn("Total: 2", contenido)


if __name__ == "__main__":
    unittest.main()
