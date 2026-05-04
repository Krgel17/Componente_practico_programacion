import tkinter as tk
from tkinter import messagebox, ttk
from abc import ABC, abstractmethod
import datetime


def log_error(msg):
    with open("logs.txt", "a", encoding="utf-8") as f:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{fecha} - {msg}\n")


class ClienteError(Exception):
    pass


class ReservaError(Exception):
    pass


class Cliente:
    def __init__(self, nombre, edad):
        nombre = nombre.strip()

        if not nombre:
            raise ClienteError("El nombre no puede estar vacio.")

        if edad <= 0:
            raise ClienteError("La edad debe ser mayor que cero.")

        self.nombre = nombre
        self.edad = edad

    def __str__(self):
        return f"{self.nombre} ({self.edad} anos)"


class Servicio(ABC):
    def __init__(self, nombre, precio):
        if precio <= 0:
            raise ValueError("El precio del servicio debe ser mayor que cero.")

        self.nombre = nombre
        self.precio = precio

    @abstractmethod
    def calcular(self, horas):
        pass


class Sala(Servicio):
    def calcular(self, horas):
        return self.precio * horas


class Equipo(Servicio):
    def calcular(self, horas):
        return (self.precio * horas) + 10


class Asesoria(Servicio):
    def calcular(self, horas):
        return (self.precio * horas) * 1.2


class Reserva:
    def __init__(self, cliente, servicio, horas):
        if not isinstance(cliente, Cliente):
            raise ReservaError("Cliente no valido.")

        if not isinstance(servicio, Servicio):
            raise ReservaError("Servicio no valido.")

        if horas <= 0:
            raise ReservaError("Las horas deben ser mayores que cero.")

        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas

    def procesar(self):
        return self.servicio.calcular(self.horas)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Software FJ")
        self.root.geometry("450x500")
        self.root.resizable(False, False)

        self.clientes = []
        self.servicios = {
            "Sala": Sala("Sala", 50),
            "Equipo": Equipo("Equipo", 30),
            "Asesoria": Asesoria("Asesoria", 100),
        }

        tk.Label(root, text="Nombre").pack(pady=(15, 0))
        self.nombre = tk.Entry(root, width=35)
        self.nombre.pack()

        tk.Label(root, text="Edad").pack(pady=(10, 0))
        self.edad = tk.Entry(root, width=35)
        self.edad.pack()

        tk.Button(root, text="Crear Cliente", command=self.crear_cliente).pack(pady=8)

        tk.Label(root, text="Seleccionar Cliente").pack(pady=(10, 0))
        self.cliente_var = tk.StringVar()
        self.combo_clientes = ttk.Combobox(
            root,
            textvariable=self.cliente_var,
            state="readonly",
            width=32
        )
        self.combo_clientes.pack()

        tk.Label(root, text="Horas").pack(pady=(15, 0))
        self.horas = tk.Entry(root, width=35)
        self.horas.pack()

        tk.Label(root, text="Servicio").pack(pady=(10, 0))
        self.servicio_var = tk.StringVar(value="Sala")
        self.combo_servicios = ttk.Combobox(
            root,
            textvariable=self.servicio_var,
            values=list(self.servicios.keys()),
            state="readonly",
            width=32
        )
        self.combo_servicios.pack()
        self.combo_servicios.current(0)

        tk.Button(root, text="Crear Reserva", command=self.crear_reserva).pack(pady=10)

        self.resultado = tk.Label(root, text="", justify="left")
        self.resultado.pack(pady=10)

        tk.Label(root, text="Historial de reservas").pack(pady=(10, 0))
        self.lista_reservas = tk.Listbox(root, width=55, height=8)
        self.lista_reservas.pack(pady=(5, 10))

    def obtener_entero(self, valor, nombre_campo):
        valor = valor.strip()

        if not valor:
            raise ValueError(f"El campo '{nombre_campo}' es obligatorio.")

        try:
            return int(valor)
        except ValueError as exc:
            raise ValueError(f"El campo '{nombre_campo}' debe ser un numero entero.") from exc

    def actualizar_lista_clientes(self):
        valores = [f"{i + 1}. {cliente}" for i, cliente in enumerate(self.clientes)]
        self.combo_clientes["values"] = valores

        if valores:
            self.combo_clientes.current(len(valores) - 1)

    def obtener_cliente_seleccionado(self):
        indice = self.combo_clientes.current()

        if indice == -1:
            raise ReservaError("Debes seleccionar un cliente.")

        return self.clientes[indice]

    def limpiar_campos_cliente(self):
        self.nombre.delete(0, tk.END)
        self.edad.delete(0, tk.END)

    def limpiar_campos_reserva(self):
        self.horas.delete(0, tk.END)
        self.combo_servicios.current(0)

    def crear_cliente(self):
        try:
            nombre = self.nombre.get().strip()
            edad = self.obtener_entero(self.edad.get(), "Edad")

            cliente = Cliente(nombre, edad)
            self.clientes.append(cliente)
            self.actualizar_lista_clientes()
            self.limpiar_campos_cliente()

            messagebox.showinfo("OK", "Cliente creado correctamente.")

        except (ClienteError, ValueError) as e:
            log_error(str(e))
            messagebox.showerror("Error", str(e))

        except Exception as e:
            log_error(f"Error inesperado al crear cliente: {e}")
            messagebox.showerror("Error", "Ocurrio un error inesperado al crear el cliente.")

    def crear_reserva(self):
        try:
            if not self.clientes:
                raise ReservaError("Primero debes crear al menos un cliente.")

            cliente = self.obtener_cliente_seleccionado()
            horas = self.obtener_entero(self.horas.get(), "Horas")
            servicio_nombre = self.servicio_var.get()

            servicio = self.servicios.get(servicio_nombre)
            if servicio is None:
                raise ReservaError("Servicio no valido.")

            reserva = Reserva(cliente, servicio, horas)
            costo = reserva.procesar()

            self.resultado.config(
                text=(
                    f"Cliente: {cliente.nombre}\n"
                    f"Servicio: {servicio.nombre}\n"
                    f"Horas: {horas}\n"
                    f"Costo: {costo:.2f}"
                )
            )

            self.lista_reservas.insert(
                tk.END,
                f"{cliente.nombre} | {servicio.nombre} | {horas} hora(s) | ${costo:.2f}"
            )

            self.limpiar_campos_reserva()
            messagebox.showinfo("OK", "Reserva creada correctamente.")

        except (ReservaError, ValueError) as e:
            log_error(str(e))
            messagebox.showerror("Error", str(e))

        except Exception as e:
            log_error(f"Error inesperado al crear reserva: {e}")
            messagebox.showerror("Error", "Ocurrio un error inesperado al crear la reserva.")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
