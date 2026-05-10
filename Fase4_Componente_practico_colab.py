import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import uuid
import json
import os
import logging


#Se configura el logging para registrar eventos importantes y errores
logging.basicConfig(
    filename="Log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_error(error):
    logging.error(error)


# SE CREAN LAS EXCEPCIONES
class ClienteError(Exception):
    pass

class ReservaError(Exception):
    pass

# SE INICIA CON LOS MODELOS
@dataclass
class Cliente:  #Clase cliente con validaciones en el post_init

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


class Servicio(ABC): #Clase abstracta para los servicios

    def __init__(self, nombre: str):

        self.nombre = nombre

    @abstractmethod #Metodo abstracto para calcular el costo total
    def calcular(self, horas: int, costo: float) -> float:
        pass

class Sala(Servicio): #Clase para el servicio de sala, hereda de Servicio

    def calcular(self, horas: int, costo: float) -> float:
        return costo * horas

class Equipo(Servicio): #Clase para el servicio de equipo, hereda de Servicio

    def calcular(self, horas: int, costo: float) -> float:
        return (costo * horas) + 10

class Asesoria(Servicio): #Clase para el servicio de asesoria, hereda de Servicio

    def calcular(self, horas: int, costo: float) -> float:
        return (costo * horas) * 1.2

class Reserva: #Clase para las reservas, contiene validaciones en el init y un metodo para procesar la reserva

    def __init__(
        self,
        cliente: Cliente,
        servicio: Servicio,
        horas: int,
        costo_servicio: float
    ):

        if horas <= 0:
            raise ReservaError("Las horas deben ser mayores que cero.")

        if costo_servicio <= 0:
            raise ReservaError("El costo debe ser mayor que cero.")

        self.id = str(uuid.uuid4())[:8].upper()
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.costo_servicio = costo_servicio
        self.total = 0.0

    def procesar(self): #Metodo para procesar la reserva, calcula el costo total utilizando el metodo calcular del servicio

        self.total = self.servicio.calcular(
            self.horas,
            self.costo_servicio
        )
        return self.total

# PERSISTENCIA, SE GUARDAN LOS CLIENTES Y RESERVAS EN ARCHIVOS JSON
ARCHIVO_CLIENTES = "clientes.json"
ARCHIVO_RESERVAS = "reservas.json"

def guardar_clientes(clientes: List[Cliente]): #Funcion para guardar los clientes en un archivo JSON, convierte los objetos Cliente a diccionarios antes de guardarlos

    datos = []

    for cliente in clientes:
        datos.append({
            "nombre": cliente.nombre,
            "edad": cliente.edad
        })

    with open(ARCHIVO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)


def cargar_clientes(): #Funcion para cargar los clientes desde un archivo JSON

    clientes = []

    if not os.path.exists(ARCHIVO_CLIENTES):
        return clientes

    with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as f:
        datos = json.load(f)

        for item in datos:
            clientes.append(
                Cliente(
                    item["nombre"],
                    item["edad"]
                )
            )
    return clientes

# INTERFAZ GRÁFICA CON TKINTER
class App:

    def __init__(self, root):

        self.root = root

        self.root.title("Sistema de Reservas")
        self.root.geometry("950x700")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.grid(sticky="nsew")

        self.frame.grid_columnconfigure(1, weight=1)

        self.clientes: List[Cliente] = []
        self.reservas = []

        self.servicios = {
            "Sala": Sala("Sala"),
            "Equipo": Equipo("Equipo"),
            "Asesoria": Asesoria("Asesoria")
        }

        # ESPACIO PARA INFORMACION DEL CLIENTE 
        tk.Label(
            self.frame,
            text="Nombre"
        ).grid(row=0, column=0, sticky="w")

        self.nombre = tk.Entry(self.frame)

        self.nombre.grid(
            row=0,
            column=1,
            sticky="ew",
            pady=5
        )

        tk.Label(
            self.frame,
            text="Edad"
        ).grid(row=1, column=0, sticky="w")

        self.edad = tk.Entry(self.frame)

        self.edad.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=5
        )

        tk.Button(
            self.frame,
            text="Crear Cliente",
            command=self.crear_cliente
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=10
        )

        # ESPACIO PARA SELECCIONAR CLIENTE
        tk.Label(
            self.frame,
            text="Seleccionar Cliente"
        ).grid(row=3, column=0, sticky="w")

        self.cliente_var = tk.StringVar()

        self.combo_clientes = ttk.Combobox(
            self.frame,
            textvariable=self.cliente_var,
            state="readonly"
        )

        self.combo_clientes.grid(
            row=3,
            column=1,
            sticky="ew",
            pady=5
        )

        # ESPACIO PARA INGRESAR HORAS
        tk.Label(
            self.frame,
            text="Horas"
        ).grid(row=4, column=0, sticky="w")

        self.horas = tk.Entry(self.frame)

        self.horas.grid(
            row=4,
            column=1,
            sticky="ew",
            pady=5
        )

        # COSTO POR HORA
        tk.Label(
            self.frame,
            text="Costo por Hora"
        ).grid(row=5, column=0, sticky="w")

        self.costo = tk.Entry(self.frame)

        self.costo.grid(
            row=5,
            column=1,
            sticky="ew",
            pady=5
        )

        # SERVICIO A SELECCIONAR
        tk.Label(
            self.frame,
            text="Servicio"
        ).grid(row=6, column=0, sticky="w")

        self.servicio_var = tk.StringVar(
            value="Sala"
        )

        self.combo_servicios = ttk.Combobox(
            self.frame,
            textvariable=self.servicio_var,
            values=list(self.servicios.keys()),
            state="readonly"
        )

        self.combo_servicios.grid(
            row=6,
            column=1,
            sticky="ew",
            pady=5
        )

        # BOTON PARA CREAR RESERVA
        tk.Button(
            self.frame,
            text="Crear Reserva",
            command=self.crear_reserva
        ).grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=10
        )

        # BOTON PARA CANCELAR RESERVA
        tk.Label(
            self.frame,
            text="ID Reserva"
        ).grid(row=8, column=0, sticky="w")

        self.id_reserva = tk.Entry(self.frame)

        self.id_reserva.grid(
            row=8,
            column=1,
            sticky="ew",
            pady=5
        )

        tk.Button(
            self.frame,
            text="Cancelar Reserva",
            command=self.cancelar_reserva
        ).grid(
            row=9,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=5
        )

        # ESPACIO PARA MODIFICAR RESERVA
        tk.Button(
            self.frame,
            text="Modificar Reserva",
            command=self.modificar_reserva
        ).grid(
            row=10,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=5
        )

        # TREEVIEW PARA MOSTRAR Y  MODIFICAR RESERVAS
        columnas = ("ID","Cliente","Servicio","Horas","Costo Hora","Total")

        self.tabla = ttk.Treeview(
            self.frame,
            columns=columnas,
            show="headings",
            height=12
        )

        for col in columnas:

            self.tabla.heading(col, text=col)

            self.tabla.column(
                col,
                anchor="center",
                width=120
            )

        self.tabla.grid(
            row=11,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=10
        )

        self.frame.grid_rowconfigure(11, weight=1)
        self.actualizar_lista_clientes()

    # SE REALIZAN LAS VALIDACIONES DE LOS CAMPOS DE ENTRADA
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

    # SE ACTUALIZA LA LISTA DE CLIENTES
    def actualizar_lista_clientes(self):

        valores = [
            f"{i+1}. {cliente}"
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
            guardar_clientes(self.clientes)
            self.actualizar_lista_clientes()

            self.nombre.delete(0, tk.END)
            self.edad.delete(0, tk.END)

            messagebox.showinfo("OK","Cliente creado.")

        except Exception as e: 
            log_error(str(e))
            messagebox.showerror("Error",str(e))

    # SE CREA UNA NUEVA RESERVA
    def crear_reserva(self):

        try:
            if not self.clientes:
                raise ReservaError("No existen clientes.")

            cliente = self.clientes[self.combo_clientes.current()]
            servicio = self.servicios[self.servicio_var.get()]
            horas = self.obtener_entero(self.horas.get(),"Horas")

            costo = self.obtener_float(
                self.costo.get(),
                "Costo"
            )

            reserva = Reserva(
                cliente,
                servicio,
                horas,
                costo
            )

            total = reserva.procesar()
            self.reservas.append(reserva)

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    reserva.id,
                    cliente.nombre,
                    servicio.nombre,
                    horas,
                    f"${costo:.2f}",
                    f"${total:.2f}"
                )
            )

            messagebox.showinfo("OK",f"Reserva creada.\nID: {reserva.id}")

        except Exception as e:
            log_error(str(e))
            messagebox.showerror("Error",str(e))

    # CANCELAR RESERVA
    def cancelar_reserva(self):

        reserva_id = self.id_reserva.get().strip()

        for item in self.tabla.get_children():
            valores = self.tabla.item(item)["values"]
            if valores[0] == reserva_id:
                self.tabla.delete(item)
                self.reservas = [
                    r for r in self.reservas
                    if r.id != reserva_id
                ]

                messagebox.showinfo("OK","Reserva cancelada.")
                return

        messagebox.showerror("Error","Reserva no encontrada.")

# MODIFICAR RESERVA
    def modificar_reserva(self):
        reserva_id = self.id_reserva.get().strip()
        reserva_encontrada = None

        for reserva in self.reservas:
            if reserva.id == reserva_id:
                reserva_encontrada = reserva
                break

        if reserva_encontrada is None:
            messagebox.showerror("Error","Reserva no encontrada.")
            return

        # VENTANA EMERGENTE PARA MODIFICAR RESERVA
        ventana = tk.Toplevel(self.root)

        ventana.title("Modificar Reserva")
        ventana.geometry("400x350")
        
        ventana.grab_set()
        ventana.grid_columnconfigure(1, weight=1)

        # ESPACIO PARA CLIENTE
        tk.Label(
            ventana,
            text="Cliente"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        cliente_var = tk.StringVar()

        combo_cliente = ttk.Combobox(
            ventana,
            textvariable=cliente_var,
            state="readonly",
            values=[
                str(cliente)
                for cliente in self.clientes
            ]
        )

        combo_cliente.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        # Cliente actual
        indice_cliente = self.clientes.index(reserva_encontrada.cliente)
        combo_cliente.current(indice_cliente)

        # ESPACIO PARA SERVICIO
        tk.Label(
            ventana,
            text="Servicio"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        servicio_var = tk.StringVar(value=reserva_encontrada.servicio.nombre)

        combo_servicio = ttk.Combobox(
            ventana,
            textvariable=servicio_var,
            state="readonly",
            values=list(self.servicios.keys())
        )

        combo_servicio.grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        # ESPACIO PARA HORAS
        tk.Label(
            ventana,
            text="Horas"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        entry_horas = tk.Entry(ventana)

        entry_horas.grid(
            row=2,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        entry_horas.insert(0,str(reserva_encontrada.horas))

        # ESPACIO PARA COSTO
        tk.Label(
            ventana,
            text="Costo por Hora"
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        entry_costo = tk.Entry(ventana)

        entry_costo.grid(
            row=3,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        entry_costo.insert(0,str(reserva_encontrada.costo_servicio))

        # GUARDAR CAMBIOS
        def guardar_cambios():

            try:
                nuevo_cliente = self.clientes[combo_cliente.current()]
                nuevo_servicio = self.servicios[servicio_var.get()]
                nuevas_horas = self.obtener_entero(entry_horas.get(),"Horas")
                nuevo_costo = self.obtener_float(entry_costo.get(),"Costo")
                nuevo_total = nuevo_servicio.calcular(nuevas_horas,nuevo_costo)

                # SE ACTUALIZA EL OBJETO
                reserva_encontrada.cliente = nuevo_cliente
                reserva_encontrada.servicio = nuevo_servicio
                reserva_encontrada.horas = nuevas_horas
                reserva_encontrada.costo_servicio = nuevo_costo
                reserva_encontrada.total = nuevo_total

                # ACTUALIZAR TREEVIEW
                for item in self.tabla.get_children():
                    valores = self.tabla.item(item)["values"]
                    if valores[0] == reserva_id:

                        self.tabla.item(
                            item,
                            values=(
                                reserva_id,
                                nuevo_cliente.nombre,
                                nuevo_servicio.nombre,
                                nuevas_horas,
                                f"${nuevo_costo:.2f}",
                                f"${nuevo_total:.2f}"
                            )
                        )
                        break

                messagebox.showinfo("OK","Reserva modificada correctamente.")
                ventana.destroy()

            except Exception as e:
                log_error(str(e))
                messagebox.showerror("Error",str(e))

        # BOTON PARA GUARDAR CAMBIOS
        tk.Button(
            ventana,
            text="Guardar Cambios",
            command=guardar_cambios
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            padx=10,
            pady=20,
            sticky="ew"
        )

# FUNCION PARA EL MAIN E INICIAR LA APLICACION

def main():

    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()