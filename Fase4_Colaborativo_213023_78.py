# =========================
# IMPORTACIONES
# =========================

from abc import ABC, abstractmethod
import datetime


# =========================
# FUNCIÓN PARA GUARDAR LOGS
# =========================

def registrar_log(mensaje):

    with open("logs.txt", "a") as archivo:
        fecha = datetime.datetime.now()
        archivo.write(f"{fecha} - {mensaje}\n")


# =========================
# EXCEPCIONES
# =========================

class ErrorSistema(Exception):
    pass


class ErrorDatoInvalido(ErrorSistema):
    pass


# =========================
# CLASE ABSTRACTA BASE
# =========================

class EntidadBase(ABC):

    def __init__(self, id):
        self._id = id

    @abstractmethod
    def mostrar_info(self):
        pass


# =========================
# CLASE CLIENTE
# =========================

class Cliente(EntidadBase):

    def __init__(self, id, nombre, email):

        super().__init__(id)

        # Validaciones
        if not nombre.strip():
            raise ErrorDatoInvalido("Nombre vacío")

        if "@" not in email:
            raise ErrorDatoInvalido("Correo inválido")

        self.__nombre = nombre
        self.__email = email

    def mostrar_info(self):

        return f"Cliente: {self.__nombre} - {self.__email}"


# =========================
# CLASE ABSTRACTA SERVICIO
# =========================

class Servicio(ABC):

    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def calcular_costo(self, horas):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# =========================
# SERVICIOS
# =========================

class ReservaSala(Servicio):

    def calcular_costo(self, horas):

        if horas <= 0:
            raise ErrorDatoInvalido("Horas inválidas")

        return horas * 50

    def descripcion(self):
        return "Reserva de sala"


class AlquilerEquipo(Servicio):

    def calcular_costo(self, horas):

        if horas <= 0:
            raise ErrorDatoInvalido("Horas inválidas")

        return horas * 30

    def descripcion(self):
        return "Alquiler de equipo"


class Asesoria(Servicio):

    def calcular_costo(self, horas):

        if horas <= 0:
            raise ErrorDatoInvalido("Horas inválidas")

        return horas * 100

    def descripcion(self):
        return "Asesoría especializada"


# =========================
# CLASE RESERVA
# =========================

class Reserva:

    def __init__(self, cliente, servicio, horas):

        if horas <= 0:
            raise ErrorDatoInvalido("Las horas deben ser mayores a 0")

        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "Pendiente"

    def confirmar(self):
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"

    def procesar(self):

        try:
            costo = self.servicio.calcular_costo(self.horas)

        except Exception as e:

            registrar_log(str(e))
            print("Ocurrió un error")

        else:

            return costo

        finally:

            registrar_log("Proceso terminado")


# =========================
# PROGRAMA PRINCIPAL
# =========================

if __name__ == "__main__":

    print("===== SISTEMA SOFTWARE FJ =====\n")

    clientes = []
    reservas = []

    try:

        # Cliente válido
        c1 = Cliente(1, "Juan", "juan@gmail.com")
        clientes.append(c1)

        print(c1.mostrar_info())

        # Cliente inválido
        try:

            c2 = Cliente(2, "", "correo malo")

        except ErrorSistema as e:

            print("Error cliente:", e)

            registrar_log(str(e))

        # Servicios
        s1 = ReservaSala("Sala 1")
        s2 = AlquilerEquipo("Proyector")
        s3 = Asesoria("Consultoría")

        print("\nServicios disponibles:")

        servicios = [s1, s2, s3]

        for s in servicios:
            print("-", s.descripcion())

        # Reserva válida
        r1 = Reserva(c1, s1, 2)

        r1.confirmar()

        print("\nCosto reserva sala:", r1.procesar())

        reservas.append(r1)

        # Reserva inválida
        try:

            r2 = Reserva(c1, s2, -5)

        except ErrorSistema as e:

            print("Error reserva:", e)

            registrar_log(str(e))

        # Otra reserva válida
        r3 = Reserva(c1, s3, 1)

        r3.confirmar()

        print("Costo asesoría:", r3.procesar())

        reservas.append(r3)

        # Cancelar reserva
        r3.cancelar()

    except Exception as e:

        registrar_log("Error crítico: " + str(e))

    finally:

        print("\n===== ESTADO DE RESERVAS =====")

        for r in reservas:
            print(r.cliente.mostrar_info(), "| Estado:", r.estado)

        print("\nEl sistema sigue funcionando correctamente.")
