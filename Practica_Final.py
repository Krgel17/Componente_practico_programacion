import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import uuid
import logging

# CONFIGURACION DEL LOG
logging.basicConfig(
    filename="Log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_error(error):
    logging.error(error)


# EXCEPCIONES
class ClienteError(Exception):
    pass


class ReservaError(Exception):
    pass


# MODELOS
@dataclass
class Cliente:

    nombre: str
    edad: int

    def __post_init__(self):

        self.nombre = self.nombre.strip()

        if not self.nombre:
            raise ClienteError("El nombre no puede estar vacio.")

        if not self.nombre.replace(" ", "").isalpha():
            raise ClienteError("El nombre solo debe contener letras.")

        if self.edad <= 0:
            raise ClienteError("La edad debe ser mayor que cero.")

    def __str__(self):
        return f"{self.nombre} ({self.edad} anos)"


class Servicio(ABC):

    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def calcular(
        self,
        duracion: int,
        costo: float,
        impuesto: float = 0,
        descuento: float = 0
    ) -> float:
        pass

    def calcular_total(
        self,
        subtotal: float,
        impuesto: float = 0,
        descuento: float = 0
    ) -> float:

        total = subtotal

        # IMPUESTO
        if impuesto > 0:

            total = total * (
                1 + (impuesto / 100)
            )

        # DESCUENTO
        if descuento > 0:

            if descuento > total:

                raise ReservaError(
                    "El descuento no puede ser mayor al total."
                )

            total -= descuento

        return total


class Sala(Servicio):

    def calcular(
        self,
        duracion: int,
        costo: float,
        impuesto: float = 0,
        descuento: float = 0
    ) -> float:

        subtotal = costo * duracion

        return self.calcular_total(
            subtotal,
            impuesto,
            descuento
        )


class Equipo(Servicio):

    def calcular(
        self,
        duracion: int,
        costo: float,
        impuesto: float = 0,
        descuento: float = 0
    ) -> float:

        subtotal = costo * duracion

        return self.calcular_total(
            subtotal,
            impuesto,
            descuento
        )


class Asesoria(Servicio):

    def calcular(
        self,
        duracion: int,
        costo: float,
        impuesto: float = 0,
        descuento: float = 0
    ) -> float:

        subtotal = costo * duracion

        return self.calcular_total(
            subtotal,
            impuesto,
            descuento
        )


class Reserva:

    def __init__(
        self,
        cliente: Cliente,
        servicio: Servicio,
        duracion: int,
        costo_servicio: float
    ):

        if duracion <= 0:
            raise ReservaError(
                "La duracion debe ser mayor que cero."
            )

        if costo_servicio <= 0:
            raise ReservaError(
                "El costo debe ser mayor que cero."
            )

        self.id = str(uuid.uuid4())[:8].upper()

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.costo_servicio = costo_servicio

        self.estado = "Pendiente"

        self.total = 0.0
        self.impuesto = 0
        self.descuento = 0
        self.tipo_descuento = "%"
        self.descuento_original = 0

    def procesar(
        self,
        impuesto: float = 0,
        descuento: float = 0
    ):

        self.impuesto = impuesto
        self.descuento = descuento

        self.total = self.servicio.calcular(
            self.duracion,
            self.costo_servicio,
            impuesto,
            descuento
        )

        self.estado = "Procesada"

        return self.total

    def confirmar(self):
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"
    
    def modificar(self):
        self.estado = "Modificada"

    @property
    def descuento_original(self):
        raise NotImplementedError

    @descuento_original.setter
    def descuento_original(self, value):
        raise NotImplementedError


clientes_temporales = []


# INTERFAZ
class App:

    def __init__(self, root):

        self.root = root

        self.root.title("Software FJ")
        self.root.geometry("1200x750")
        self.root.minsize(900, 600)
        self.root.state("zoomed")

    # ESTILOS
        # COLORES
        COLOR_FONDO = "#121212"
        COLOR_PANEL = "#1e1e1e"
        COLOR_DORADO = "#c9a227"
        COLOR_HOVER = "#dbb83a"
        COLOR_TEXTO = "#e0e0e0"
        COLOR_BORDE = "#2a2a2a"

        # CONFIGURAR VENTANA
        self.root.configure(
            bg=COLOR_FONDO
        )

        # ESTILOS
        self.style = ttk.Style()

        self.style.theme_use("clam")

        # FRAME
        self.style.configure(
            "TFrame",
            background=COLOR_FONDO
        )

        # LABEL
        self.style.configure(
            "TLabel",
            background=COLOR_FONDO,
            foreground=COLOR_TEXTO,
            font=("Segoe UI", 11)
        )

        # ENTRY
        self.style.configure(
            "TEntry",
            fieldbackground=COLOR_TEXTO,
            foreground=COLOR_FONDO,
            bordercolor=COLOR_TEXTO,
            lightcolor=COLOR_TEXTO,
            darkcolor=COLOR_TEXTO,
            insertcolor=COLOR_TEXTO,
            padding=8
        )

        # COMBOBOX
        self.style.configure(
            "TCombobox",
            fieldbackground=COLOR_FONDO,
            background=COLOR_FONDO,
            foreground=COLOR_FONDO,
            bordercolor=COLOR_BORDE,
            lightcolor=COLOR_BORDE,
            darkcolor=COLOR_FONDO,
            arrowcolor=COLOR_FONDO,
            padding=8
        )

        # BOTONES
        self.style.configure(
            "TButton",
            background=COLOR_DORADO,
            foreground="#000000",
            borderwidth=0,
            focusthickness=0,
            focuscolor="none",
            padding=10,
            font=("Segoe UI", 11, "bold")
        )

        self.style.map(
            "TButton",
            background=[
                ("active", COLOR_HOVER)
            ]
        )

        # CHECKBUTTON
        self.style.configure(
            "TCheckbutton",
            background=COLOR_FONDO,
            foreground=COLOR_TEXTO,
            font=("Segoe UI", 10)
        )

        self.style.map(
            "TCheckbutton",
            background=[("active", COLOR_PANEL)],
            foreground=[("active", COLOR_DORADO)]
        )

        # TREEVIEW
        self.style.configure(
            "Treeview",
            background=COLOR_FONDO,
            foreground=COLOR_TEXTO,
            fieldbackground=COLOR_PANEL,
            bordercolor=COLOR_BORDE,
            rowheight=35,
            font=("Segoe UI", 10)
        )

        # SELECCION DE FILA
        self.style.map(
            "Treeview",
            background=[
                ("selected", COLOR_DORADO)
            ],
            foreground=[
                ("selected", "#000000")
            ]
        )

        # HEADERS
        self.style.configure(
            "Treeview.Heading",
            background=COLOR_DORADO,
            foreground="#000000",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0
        )

        self.style.map(
            "Treeview.Heading",
            background=[
                ("active", COLOR_HOVER)
            ]
        )

        # SCROLLBAR
        self.style.configure(
            "Vertical.TScrollbar",
            background=COLOR_PANEL,
            troughcolor=COLOR_FONDO,
            bordercolor=COLOR_BORDE,
            arrowcolor=COLOR_DORADO
        )

        self.style.configure(
            "Horizontal.TScrollbar",
            background=COLOR_PANEL,
            troughcolor=COLOR_FONDO,
            bordercolor=COLOR_BORDE,
            arrowcolor=COLOR_DORADO
        )

        # SEPARADOR
        self.style.configure(
            "TSeparator",
            background=COLOR_FONDO
        )

        self.clientes: List[Cliente] = clientes_temporales
        self.reservas = []

        self.servicios = {
            "Sala": Sala("Sala"),
            "Equipo": Equipo("Equipo"),
            "Asesoria": Asesoria("Asesoria")
        }

        # VARIABLES
        self.aplica_impuesto = tk.BooleanVar()
        self.aplica_descuento = tk.BooleanVar()
        self.tipo_descuento = tk.StringVar(value="%")

        # CONTENEDOR PRINCIPAL
        contenedor = ttk.Frame(root)

        contenedor.pack(
            fill="both",
            expand=True
        )

        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            contenedor,
            bg=COLOR_FONDO,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            contenedor,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )
        
        self.canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.frame = ttk.Frame(self.canvas, padding=25)

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.frame,
            anchor="n"
        )

        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self._on_mousewheel
        )

        for i in range(4):
            self.frame.columnconfigure(i, weight=1)
        

        for i in range(25):
            self.frame.rowconfigure(i, weight=1)
        
        self.frame.rowconfigure(20, weight=1)

        # TITULO
        titulo = tk.Label(
            self.frame,
            text="SISTEMA DE RESERVAS",
            font=("Segoe UI", 24, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        )

        titulo.grid(
            row=0,
            column=0,
            columnspan=4,
            pady=(20, 30),
            sticky="n"
        )

        # CONTENEDOR CENTRAL
        formulario = ttk.Frame(
            self.frame,
            padding=30
        )

        formulario.grid(
            row=1,
            column=0,
            columnspan=4,
            pady=10
        )

        # CENTRAR
        for i in range(4):
            formulario.columnconfigure(i, weight=1)

        # =========================
        # CLIENTES
        # =========================

        ttk.Label(
            formulario,
            text="Nombre"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        self.nombre = ttk.Entry(formulario)

        self.nombre.grid(
            row=0,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=10
        )

        ttk.Label(
            formulario,
            text="Edad"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        self.edad = ttk.Entry(formulario)

        self.edad.grid(
            row=1,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=10
        )

        ttk.Button(
            formulario,
            text="Crear Cliente",
            command=self.crear_cliente
        ).grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=10,
            pady=(15, 25)
        )

        # SEPARADOR
        ttk.Separator(
            formulario,
            orient="horizontal"
        ).grid(
            row=3,
            column=0,
            columnspan=4,
            sticky="ew",
            pady=10
        )

        # =========================
        # RESERVAS
        # =========================

        ttk.Label(
            formulario,
            text="Seleccionar Cliente"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        self.cliente_var = tk.StringVar()

        self.combo_clientes = ttk.Combobox(
            formulario,
            textvariable=self.cliente_var,
            state="readonly"
        )

        self.combo_clientes.grid(
            row=4,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=10
        )

        # HORAS
        ttk.Label(
            formulario,
            text="Horas"
        ).grid(
            row=5,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        self.duracion = ttk.Entry(formulario)

        self.duracion.grid(
            row=5,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=10
        )

        # COSTO
        ttk.Label(
            formulario,
            text="Costo por Hora"
        ).grid(
            row=6,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        self.costo = ttk.Entry(formulario)

        self.costo.grid(
            row=6,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=10
        )

        # SERVICIO
        ttk.Label(
            formulario,
            text="Servicio"
        ).grid(
            row=7,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        self.servicio_var = tk.StringVar(
            value="Sala"
        )

        self.combo_servicios = ttk.Combobox(
            formulario,
            textvariable=self.servicio_var,
            values=list(self.servicios.keys()),
            state="readonly"
        )

        self.combo_servicios.grid(
            row=7,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=10
        )

        # IMPUESTO
        ttk.Checkbutton(
            formulario,
            text="Aplicar Impuesto (19%)",
            variable=self.aplica_impuesto
        ).grid(
            row=8,
            column=0,
            columnspan=3,
            sticky="w",
            padx=10,
            pady=10
        )

        # DESCUENTO
        ttk.Checkbutton(
            formulario,
            text="Aplicar Descuento",
            variable=self.aplica_descuento,
            command=self.toggle_descuento
        ).grid(
            row=9,
            column=0,
            columnspan=3,
            sticky="w",
            padx=10,
            pady=10
        )

        # VALOR DESCUENTO
        ttk.Label(
            formulario,
            text="Valor Descuento"
        ).grid(
            row=10,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        self.entry_descuento = ttk.Entry(formulario)
        self.entry_descuento.configure(
            state="disabled"
        )

        self.entry_descuento.grid(
            row=10,
            column=1,
            sticky="ew",
            padx=(10, 5),
            pady=10
        )

        combo_tipo_descuento = ttk.Combobox(
            formulario,
            textvariable=self.tipo_descuento,
            values=["%", "$"],
            state="readonly",
            width=5
        )

        combo_tipo_descuento.grid(
            row=10,
            column=2,
            sticky="w",
            padx=(5, 10),
            pady=10
        )

        # BOTON
        ttk.Button(
            formulario,
            text="Crear Reserva",
            command=self.crear_reserva
        ).grid(
            row=11,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=10,
            pady=(20, 10)
        )
        # BOTONES
        botones_frame = ttk.Frame(self.frame)

        botones_frame.grid(
            row=12,
            column=0,
            columnspan=4,
            sticky="ew",
            pady=10
        )

        botones_frame.columnconfigure((0, 1, 2), weight=1)

        ttk.Button(
            botones_frame,
            text="Modificar Reserva",
            command=self.modificar_reserva
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5
        )

        ttk.Button(
            botones_frame,
            text="Confirmar Reserva",
            command=self.confirmar_reserva
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5
        )

        ttk.Button(
            botones_frame,
            text="Cancelar Reserva",
            command=self.cancelar_reserva
        ).grid(
            row=0,
            column=2,
            sticky="ew",
            padx=5
        )

        # TABLA
        tabla_frame = ttk.Frame(self.frame)

        tabla_frame.grid(
            row=20,
            column=0,
            columnspan=4,
            sticky="nsew",
            pady=20
        )

        # RESPONSIVE
        self.frame.rowconfigure(20, weight=1)

        tabla_frame.rowconfigure(0, weight=1)
        tabla_frame.columnconfigure(0, weight=1)

        columnas = (
            "ID",
            "Cliente",
            "Servicio",
            "Horas",
            "Costo/Hora",
            "Subtotal",
            "Estado",
            "Impuesto",
            "Descuento",
            "Total"
        )

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings"
        )

        # CONFIGURAR COLUMNAS RESPONSIVE
        for col in columnas:

            self.tabla.heading(
                col,
                text=col
            )

            self.tabla.column(
                col,
                anchor="center",
                stretch=True,
                width=100,
                minwidth=80
            )

        # SCROLLS
        scrollbar_y = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla.yview
        )

        scrollbar_x = ttk.Scrollbar(
            tabla_frame,
            orient="horizontal",
            command=self.tabla.xview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        # POSICIONAMIENTO RESPONSIVE
        self.tabla.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar_y.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        scrollbar_x.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        # AJUSTAR AUTOMATICAMENTE EL TAMANO DE COLUMNAS
        def ajustar_columnas(event=None):

            ancho_total = self.tabla.winfo_width()

            if ancho_total <= 1:
                return

            cantidad_columnas = len(columnas)

            ancho_columna = int(
                ancho_total / cantidad_columnas
            )

            for col in columnas:

                self.tabla.column(
                    col,
                    width=ancho_columna
                )

        # EVENTO RESPONSIVE
        self.tabla.bind(
            "<Configure>",
            ajustar_columnas
        )

        self.canvas.bind(
            "<Configure>",
            self.centrar_contenido
        )

    def centrar_contenido(self, event=None):

        ancho_canvas = self.canvas.winfo_width()

        ancho_frame = self.frame.winfo_reqwidth()

        x = max((ancho_canvas - ancho_frame) // 2, 0)

        self.canvas.coords(
            self.canvas_window,
            x,
            0
        )

    # SCROLL
    def _on_mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # VALIDACIONES
    def obtener_entero(self, valor, campo):

        valor = valor.strip()

        if not valor:
            raise ValueError(f"El campo '{campo}' es obligatorio.")

        numero = int(valor)

        if numero <= 0:
            raise ValueError(f"El campo '{campo}' debe ser positivo.")

        return numero

    def obtener_float(self, valor, campo):

        valor = valor.strip()

        if not valor:
            raise ValueError(f"El campo '{campo}' es obligatorio.")

        numero = float(valor)

        if numero <= 0:
            raise ValueError(f"El campo '{campo}' debe ser positivo.")

        return numero
    
    def toggle_descuento(self):

        if self.aplica_descuento.get():

            self.entry_descuento.configure(
                state="normal"
            )

        else:

            self.entry_descuento.delete(0, tk.END)

            self.entry_descuento.configure(
                state="disabled"
            )
    
    def formatear_moneda(self, valor):
        return (
            f"${valor:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )


    # CLIENTES
    def actualizar_lista_clientes(self):

        valores = [
            f"{i + 1}. {cliente}"
            for i, cliente in enumerate(self.clientes)
        ]

        self.combo_clientes["values"] = valores

        if valores:
            self.combo_clientes.current(0)

    def crear_cliente(self):

        try:

            cliente = Cliente(
                self.nombre.get(),
                self.obtener_entero(
                    self.edad.get(),
                    "Edad"
                )
            )

            self.clientes.append(cliente)

            self.actualizar_lista_clientes()

            self.nombre.delete(0, tk.END)
            self.edad.delete(0, tk.END)

            messagebox.showinfo(
                "OK",
                "Cliente creado."
            )

        except Exception as e:

            log_error(e)

            messagebox.showerror(
                "Error",
                str(e)
            )

    # CREAR RESERVA
    def crear_reserva(self):

        try:

            if not self.clientes:
                raise ReservaError("No existen clientes.")

            cliente = self.clientes[
                self.combo_clientes.current()
            ]

            servicio = self.servicios[
                self.servicio_var.get()
            ]

            duracion = self.obtener_entero(
                self.duracion.get(),
                "Duracion"
            )

            costo = self.obtener_float(
                self.costo.get(),
                "Costo"
            )

            reserva = Reserva(
                cliente,
                servicio,
                duracion,
                costo
            )

            subtotal = costo * duracion

            impuesto = 19 if self.aplica_impuesto.get() else 0

            total_con_impuesto = subtotal

            if impuesto > 0:

                total_con_impuesto = (
                    subtotal * (1 + impuesto / 100)
                )

            descuento = 0
            descuento_mostrar = "$0.00"


            if self.aplica_descuento.get():

                descuento_valor = self.obtener_float(
                    self.entry_descuento.get(),
                    "Descuento"
                )

                reserva.tipo_descuento = (
                    self.tipo_descuento.get()
                )

                reserva.descuento_original = (
                    descuento_valor
                )

                # PORCENTAJE
                if self.tipo_descuento.get() == "%":

                    descuento = (
                        total_con_impuesto *
                        (descuento_valor / 100)
                    )

                # DINERO
                else:

                    descuento = descuento_valor

                if descuento > total_con_impuesto:

                    raise ReservaError(
                        "El descuento no puede ser mayor al total."
                    )

                descuento_mostrar = (
                    self.formatear_moneda(descuento)
                )

            total = reserva.procesar(
                impuesto=impuesto,
                descuento=descuento
            )

            self.reservas.append(reserva)

            subtotal = costo * duracion

            if servicio.nombre == "Equipo":
                subtotal += 10

            elif servicio.nombre == "Asesoria":
                subtotal *= 1.2

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    reserva.id,
                    cliente.nombre,
                    servicio.nombre,
                    duracion,
                    self.formatear_moneda(costo),
                    self.formatear_moneda(subtotal),
                    reserva.estado,
                    f"{impuesto}%",
                    descuento_mostrar,
                    self.formatear_moneda(total)
                )
            )


            self.duracion.delete(0, tk.END)
            self.costo.delete(0, tk.END)
            self.entry_descuento.delete(0, tk.END)
            self.aplica_impuesto.set(False)
            self.aplica_descuento.set(False)
            self.tipo_descuento.set("%")
            if self.combo_clientes["values"]:
                self.combo_clientes.current(0)
            self.combo_servicios.current(0)

            messagebox.showinfo(
                "OK",
                f"Reserva creada.\nID: {reserva.id}"
            )

        except Exception as e:

            log_error(e)

            messagebox.showerror(
                "Error",
                str(e)
            )

    def confirmar_reserva(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showerror(
                "Error",
                "Seleccione una reserva."
            )

            return

        item = seleccion[0]

        valores = self.tabla.item(item)["values"]

        reserva_id = valores[0]

        for reserva in self.reservas:

            if reserva.id == reserva_id:

                reserva.confirmar()

                self.tabla.item(
                    item,
                    values=(
                        reserva.id,
                        reserva.cliente.nombre,
                        reserva.servicio.nombre,
                        reserva.duracion,
                        valores[4],
                        valores[5],
                        reserva.estado,
                        valores[7],
                        valores[8],
                        valores[9]
                    )
                )

                break

        messagebox.showinfo(
            "OK",
            "Reserva confirmada correctamente."
        )


    # CANCELAR RESERVA
    def cancelar_reserva(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showerror(
                "Error",
                "Seleccione una reserva."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmacion",
            "Desea cancelar la reserva seleccionada?"
        )

        if not confirmar:
            return

        item = seleccion[0]

        valores = self.tabla.item(item)["values"]

        reserva_id = valores[0]

        for reserva in self.reservas:

            if reserva.id == reserva_id:
                reserva.cancelar()
                break

        self.tabla.delete(item)

        self.reservas = [
            r for r in self.reservas
            if r.id != reserva_id
        ]

        messagebox.showinfo(
            "OK",
            "Reserva cancelada."
        )

    # MODIFICAR RESERVA
    def modificar_reserva(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showerror(
                "Error",
                "Seleccione una reserva."
            )

            return

        item = seleccion[0]

        valores = self.tabla.item(item)["values"]

        reserva_id = valores[0]

        reserva_encontrada = None

        for reserva in self.reservas:

            if reserva.id == reserva_id:
                reserva_encontrada = reserva
                break

        if reserva_encontrada is None:

            messagebox.showerror(
                "Error",
                "Reserva no encontrada."
            )

            return
        # COLORES
        COLOR_FONDO = "#121212"
        COLOR_PANEL = "#1e1e1e"
        COLOR_DORADO = "#c9a227"
        COLOR_HOVER = "#dbb83a"
        COLOR_TEXTO = "#e0e0e0"
        COLOR_BORDE = "#2a2a2a"


        # VENTANA
        ventana = tk.Toplevel(self.root)
        ventana.configure(
            bg=COLOR_FONDO
        )

        ventana.title("Modificar Reserva")

        ventana.geometry("600x500")

        ventana.minsize(500, 450)

        ventana.grab_set()

        ventana.columnconfigure(1, weight=1)

        # CLIENTE
        ttk.Label(
            ventana,
            text="Seleccionar Cliente"
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        cliente_var = tk.StringVar()

        combo_clientes = ttk.Combobox(
            ventana,
            textvariable=cliente_var,
            state="readonly",
            values=[
                f"{i+1}. {cliente}"
                for i, cliente in enumerate(self.clientes)
            ]
        )

        combo_clientes.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=10,
            pady=10
        )

        indice_cliente = self.clientes.index(
            reserva_encontrada.cliente
        )

        combo_clientes.current(indice_cliente)

        # HORAS
        ttk.Label(
            ventana,
            text="Horas"
        ).grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        entry_duracion = ttk.Entry(ventana)

        entry_duracion.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=10,
            pady=10
        )

        entry_duracion.insert(
            0,
            str(reserva_encontrada.duracion)
        )

        # COSTO
        ttk.Label(
            ventana,
            text="Costo por Hora"
        ).grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        entry_costo = ttk.Entry(ventana)

        entry_costo.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=10,
            pady=10
        )

        entry_costo.insert(
            0,
            str(reserva_encontrada.costo_servicio)
        )

        # SERVICIO
        ttk.Label(
            ventana,
            text="Servicio"
        ).grid(
            row=3,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        servicio_var = tk.StringVar(
            value=reserva_encontrada.servicio.nombre
        )

        combo_servicios = ttk.Combobox(
            ventana,
            textvariable=servicio_var,
            values=list(self.servicios.keys()),
            state="readonly"
        )

        combo_servicios.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=10,
            pady=10
        )

        # IMPUESTO
        aplica_impuesto = tk.BooleanVar(
            value=reserva_encontrada.impuesto > 0
        )

        ttk.Checkbutton(
            ventana,
            text="Aplicar Impuesto (19%)",
            variable=aplica_impuesto
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=10
        )

        # DESCUENTO
        aplica_descuento = tk.BooleanVar(
            value=reserva_encontrada.descuento > 0
        )

        def toggle_descuento_modal():

            if aplica_descuento.get():
                entry_descuento.configure(
                    state="normal"
                )

            else:
                entry_descuento.delete(0, tk.END)
                entry_descuento.configure(
                    state="disabled"
                )


        ttk.Checkbutton(
            ventana,
            text="Aplicar Descuento",
            variable=aplica_descuento,
            command=toggle_descuento_modal
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="w",
            padx=10,
            pady=10
        )

        # VALOR DESCUENTO
        ttk.Label(
            ventana,
            text="Valor Descuento"
        ).grid(
            row=6,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        entry_descuento = ttk.Entry(ventana)
        if not aplica_descuento.get():
            entry_descuento.configure(
                state="disabled"
            )

        entry_descuento.grid(
            row=6,
            column=1,
            sticky="ew",
            padx=10,
            pady=10
        )

        if reserva_encontrada.descuento > 0:

            entry_descuento.insert(
                0,
                str(reserva_encontrada.descuento_original)
            )

        # TIPO DESCUENTO
        tipo_descuento = tk.StringVar(
            value=reserva_encontrada.tipo_descuento
        )

        combo_tipo_descuento = ttk.Combobox(
            ventana,
            textvariable=tipo_descuento,
            values=["%", "$"],
            state="readonly",
            width=5
        )

        combo_tipo_descuento.grid(
            row=6,
            column=2,
            padx=5
        )

        # GUARDAR CAMBIOS
        def guardar_cambios():

            try:

                nuevo_cliente = self.clientes[
                    combo_clientes.current()
                ]

                nuevo_servicio = self.servicios[
                    servicio_var.get()
                ]

                nueva_duracion = self.obtener_entero(
                    entry_duracion.get(),
                    "Duracion"
                )

                nuevo_costo = self.obtener_float(
                    entry_costo.get(),
                    "Costo"
                )

                subtotal = (
                    nuevo_costo *
                    nueva_duracion
                )

                impuesto = 19 if aplica_impuesto.get() else 0

                total_con_impuesto = subtotal

                if impuesto > 0:

                    total_con_impuesto = (
                        subtotal * (1 + impuesto / 100)
                    )

                descuento = 0
                descuento_mostrar = "$0.00"

                if aplica_descuento.get():

                    descuento_valor = self.obtener_float(
                        entry_descuento.get(),
                        "Descuento"
                    )

                    # PORCENTAJE
                    if tipo_descuento.get() == "%":

                        descuento = (
                            total_con_impuesto *
                            (descuento_valor / 100)
                        )

                    # DINERO
                    else:

                        descuento = descuento_valor

                    if descuento > total_con_impuesto:

                        raise ReservaError(
                            "El descuento no puede ser mayor al total."
                        )

                    descuento_mostrar = (
                        self.formatear_moneda(descuento)
                    )

                
                total = nuevo_servicio.calcular(
                    nueva_duracion,
                    nuevo_costo,
                    impuesto,
                    descuento
                )

                # ACTUALIZAR OBJETO
                reserva_encontrada.cliente = nuevo_cliente
                reserva_encontrada.servicio = nuevo_servicio
                reserva_encontrada.duracion = nueva_duracion
                reserva_encontrada.costo_servicio = nuevo_costo
                reserva_encontrada.impuesto = impuesto
                reserva_encontrada.descuento = descuento
                reserva_encontrada.total = total

                reserva_encontrada.modificar()

                # ACTUALIZAR TABLA
                subtotal = nuevo_costo * nueva_duracion

                if nuevo_servicio.nombre == "Equipo":
                    subtotal += 10

                elif nuevo_servicio.nombre == "Asesoria":
                    subtotal *= 1.2

                self.tabla.item(
                    item,
                    values=(
                        reserva_encontrada.id,
                        nuevo_cliente.nombre,
                        nuevo_servicio.nombre,
                        nueva_duracion,
                        self.formatear_moneda(nuevo_costo),
                        self.formatear_moneda(subtotal),
                        reserva_encontrada.estado,
                        f"{impuesto}%",
                        descuento_mostrar,
                        self.formatear_moneda(total)
                    )
                )

                messagebox.showinfo(
                    "OK",
                    "Reserva modificada correctamente."
                )

                ventana.destroy()

            except Exception as e:

                log_error(e)

                messagebox.showerror(
                    "Error",
                    str(e)
                )

        ttk.Button(
            ventana,
            text="Guardar Cambios",
            command=guardar_cambios
        ).grid(
            row=7,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=10,
            pady=20
        )


# MAIN
def main():

    root = tk.Tk()

    App(root)

    root.mainloop()


if __name__ == "__main__":
    main()