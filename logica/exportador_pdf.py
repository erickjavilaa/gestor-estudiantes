"""Exportación de la lista de estudiantes a un archivo PDF."""

import os
from datetime import datetime
from xml.sax.saxutils import escape


def exportar_pdf(estudiantes, ruta="salidas/lista_estudiantes.pdf"):
    """Genera un PDF con una tabla de estudiantes y devuelve la ruta.

    Lanza ValueError si no hay estudiantes, si falta reportlab
    o si no se puede escribir el archivo.
    """
    if not estudiantes:
        raise ValueError("No hay estudiantes para exportar.")

    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import (Paragraph, SimpleDocTemplate,
                                        Spacer, Table, TableStyle)
    except ImportError:
        raise ValueError("Falta instalar reportlab. Ejecuta: pip install reportlab")

    estilos = getSampleStyleSheet()
    celda = estilos["Normal"]
    celda.fontSize = 9

    def texto(valor):
        return Paragraph(escape(str(valor)), celda)

    elementos = [
        Paragraph("Lista de estudiantes", estilos["Title"]),
        Paragraph(f"Generado el {datetime.now():%d/%m/%Y %H:%M}", estilos["Normal"]),
        Spacer(1, 16),
    ]

    datos = [["Nombre", "ID IEST", "Carrera", "Semestre", "Correo"]]
    for e in estudiantes:
        datos.append([texto(e.nombre), texto(e.id_iest), texto(e.carrera),
                      texto(e.semestre), texto(e.correo)])

    tabla = Table(datos, colWidths=[110, 60, 120, 45, 133], repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F5597")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#EEF2F9")]),
    ]))
    elementos.append(tabla)
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"Total de estudiantes: {len(estudiantes)}",
                               estilos["Normal"]))

    try:
        carpeta = os.path.dirname(ruta)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)
        SimpleDocTemplate(ruta, pagesize=letter).build(elementos)
    except OSError as error:
        raise ValueError(f"No se pudo guardar el PDF: {error}")

    return ruta