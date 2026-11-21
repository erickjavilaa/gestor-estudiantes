import os
import ctypes
import tkinter as tk
from tkinter import ttk, messagebox

from logica.estudiante import Estudiante
from logica.gestor import GestorEstudiantes
from logica.validaciones import validar_estudiante, CARRERAS

NARANJA = "#c2570c"
NARANJA_CLARO = "#e8710a"
FONDO = "#fde8d4"
BLANCO = "#ffffff"
ROJO = "#b23b3b"


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        if os.name == "nt":  # solo en Windows
            try:
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    "iest.gestor.estudiantes")
            except Exception:
                pass
        super().__init__()
        self.poner_icono()
        self.title("Gestor de Estudiantes")
        self.geometry("900x600")
        self.minsize(820, 540)
        self.configure(bg=FONDO)

        self.gestor = GestorEstudiantes()

        self.crear_estilos()
        self.crear_encabezado()
        self.crear_formulario()
        # La barra de estado se crea antes que la tabla para que nunca
        # quede recortada al hacer chica la ventana.
        self.crear_barra_estado()
        self.crear_tabla()

        self.actualizar_tabla()

    def poner_icono(self):
        """Cambia el icono de la ventana. Si no encuentra la imagen, usa el de siempre."""
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta = os.path.join(base, "recursos", "logo.png")
        try:
            self.icono = tk.PhotoImage(file=ruta)
            self.iconphoto(True, self.icono)
        except tk.TclError:
            pass

    def crear_estilos(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TFrame", background=FONDO)
        s.configure("Tarjeta.TFrame", background=BLANCO)
        s.configure("Tarjeta.TLabelframe", background=BLANCO)
        s.configure("Tarjeta.TLabelframe.Label", background=BLANCO,
                    foreground=NARANJA, font=("Segoe UI", 11, "bold"))
        s.configure("TLabel", background=BLANCO, font=("Segoe UI", 10))
        s.configure("TEntry", padding=4)
        s.configure("TCombobox", padding=4)
        s.configure("Principal.TButton", background=NARANJA_CLARO, foreground="white",
                    font=("Segoe UI", 10, "bold"), padding=8, borderwidth=0)
        s.map("Principal.TButton", background=[("active", NARANJA)])
        s.configure("Peligro.TButton", background=ROJO, foreground="white",
                    font=("Segoe UI", 10, "bold"), padding=8, borderwidth=0)
        s.map("Peligro.TButton", background=[("active", "#8c2d2d")])
        s.configure("Normal.TButton", font=("Segoe UI", 10), padding=8)
        s.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        s.configure("Treeview.Heading", background=NARANJA, foreground="white",
                    font=("Segoe UI", 10, "bold"))
        s.map("Treeview.Heading", background=[("active", NARANJA_CLARO)])
        s.map("Treeview", background=[("selected", "#e8710a")],
              foreground=[("selected", "white")])

    def crear_encabezado(self):
        barra = tk.Frame(self, bg=NARANJA, height=60)
        barra.pack(fill="x")
        tk.Label(barra, text="Gestor de Estudiantes", bg=NARANJA, fg="white",
                 font=("Segoe UI", 18, "bold")).pack(side="left", padx=20, pady=12)

    def crear_formulario(self):
        marco = ttk.LabelFrame(self, text="Datos del estudiante",
                               style="Tarjeta.TLabelframe", padding=15)
        marco.pack(fill="x", padx=20, pady=(15, 8))
        marco.columnconfigure((1, 3), weight=1)

        self.var_nombre = tk.StringVar()
        self.var_id = tk.StringVar()
        self.var_carrera = tk.StringVar()
        self.var_semestre = tk.StringVar()
        self.var_correo = tk.StringVar()

        def poner_campo(fila, columna, texto, widget):
            ttk.Label(marco, text=texto).grid(row=fila, column=columna,
                                              sticky="e", padx=(0, 8), pady=6)
            widget.grid(row=fila, column=columna + 1, sticky="ew",
                        padx=(0, 20), pady=6)

        self.campo_nombre = ttk.Entry(marco, textvariable=self.var_nombre)
        poner_campo(0, 0, "Nombre:", self.campo_nombre)
        poner_campo(0, 2, "ID IEST:", ttk.Entry(marco, textvariable=self.var_id))
        poner_campo(1, 0, "Carrera:",
                    ttk.Combobox(marco, textvariable=self.var_carrera,
                                 values=CARRERAS, state="readonly"))
        poner_campo(1, 2, "Semestre:",
                    ttk.Spinbox(marco, from_=1, to=12, textvariable=self.var_semestre))
        poner_campo(2, 0, "Correo:", ttk.Entry(marco, textvariable=self.var_correo))

        botones = ttk.Frame(marco, style="Tarjeta.TFrame")
        botones.grid(row=3, column=0, columnspan=4, pady=(12, 0), sticky="e")
        ttk.Button(botones, text="Guardar", style="Principal.TButton",
                   command=self.guardar).pack(side="left", padx=4)
        ttk.Button(botones, text="Buscar por ID", style="Normal.TButton",
                   command=self.buscar).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar", style="Peligro.TButton",
                   command=self.eliminar).pack(side="left", padx=4)
        ttk.Button(botones, text="Limpiar", style="Normal.TButton",
                   command=self.limpiar).pack(side="left", padx=4)
        ttk.Button(botones, text="Imprimir", style="Normal.TButton",
                   command=self.imprimir).pack(side="left", padx=4)

    def crear_tabla(self):
        marco = ttk.Frame(self)
        marco.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        columnas = ("nombre", "id", "carrera", "semestre", "correo")
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings")

        encabezados = [("nombre", "Nombre", 200), ("id", "ID IEST", 100),
                       ("carrera", "Carrera", 200), ("semestre", "Semestre", 80),
                       ("correo", "Correo", 220)]
        for columna, texto, ancho in encabezados:
            self.tabla.heading(columna, text=texto)
            self.tabla.column(columna, width=ancho, anchor="w")

        scroll = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar)

    def crear_barra_estado(self):
        self.var_estado = tk.StringVar(value="Listo")
        tk.Label(self, textvariable=self.var_estado, bg="#e3e8f0", fg=NARANJA,
                 anchor="w", padx=12, font=("Segoe UI", 9)).pack(fill="x", side="bottom")

    def actualizar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for e in self.gestor.listar():
            self.tabla.insert("", "end", iid=e.id_iest,
                              values=(e.nombre, e.id_iest, e.carrera,
                                      e.semestre, e.correo))
        self.var_estado.set(f"{len(self.gestor.estudiantes)} estudiante(s) registrado(s)")

    def limpiar(self):
        for variable in (self.var_nombre, self.var_id, self.var_carrera,
                         self.var_semestre, self.var_correo):
            variable.set("")
        self.tabla.selection_remove(self.tabla.selection())
        self.campo_nombre.focus()

    def llenar_formulario(self, e):
        self.var_nombre.set(e.nombre)
        self.var_id.set(e.id_iest)
        self.var_carrera.set(e.carrera)
        self.var_semestre.set(e.semestre)
        self.var_correo.set(e.correo)

    def al_seleccionar(self, _evento=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        estudiante = self.gestor.buscar(seleccion[0])
        if estudiante:
            self.llenar_formulario(estudiante)

    def guardar(self):
        try:
            nombre, id_iest, carrera, semestre, correo = validar_estudiante(
                self.var_nombre.get(),
                self.var_id.get(),
                self.var_carrera.get(),
                self.var_semestre.get(),
                self.var_correo.get(),
            )
        except ValueError as e:
            messagebox.showwarning("Datos inválidos", str(e))
            return

        estudiante = Estudiante(nombre, id_iest, carrera, semestre, correo)
        try:
            self.gestor.agregar(estudiante)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.actualizar_tabla()
        self.limpiar()
        self.var_estado.set("Estudiante guardado correctamente")
        messagebox.showinfo("Guardar", "Estudiante guardado correctamente")

    def buscar(self):
        id_buscado = self.var_id.get().strip()
        if not id_buscado:
            messagebox.showwarning("Buscar", "Escribe un ID para buscar")
            return

        estudiante = self.gestor.buscar(id_buscado)
        if estudiante is None:
            messagebox.showinfo("Buscar", "No se encontró un estudiante con ese ID")
            return

        self.llenar_formulario(estudiante)
        self.tabla.selection_set(estudiante.id_iest)
        self.tabla.see(estudiante.id_iest)
        self.var_estado.set("Estudiante encontrado")

    def eliminar(self):
        id_eliminar = self.var_id.get().strip()
        if not id_eliminar:
            messagebox.showwarning("Eliminar", "Escribe o selecciona un ID")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar al estudiante {id_eliminar}?"):
            return

        try:
            self.gestor.eliminar(id_eliminar)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.actualizar_tabla()
        self.limpiar()
        self.var_estado.set("Estudiante eliminado")
        messagebox.showinfo("Eliminar", "Estudiante eliminado correctamente")

    def imprimir(self):
        try:
            ruta = self.gestor.exportar_txt()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Imprimir", f"Reporte guardado en:\n{ruta}")
