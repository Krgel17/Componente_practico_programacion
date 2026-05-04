# IMPORTACIONES


from abc import ABC, abstractmethod
import datetime



# LOGS


def registrar_log(mensaje):
    # Guarda errores en un archivo
    with open("logs.txt", "a") as archivo:
        fecha = datetime.datetime.now()
        archivo.write(f"{fecha} - {mensaje}\n")



# EXCEPCIONES


class ErrorSistema(Exception):
    pass

class ErrorDatoInvalido(ErrorSistema):
    pass

class ErrorOperacion(ErrorSistema):
    pass



# CLASE ABSTRACTA BASE


class EntidadBase(ABC):

    def __init__(self, id):
        self._id = id

    def obtener_id(self):
        return self._id

    @abstractmethod
    def mostrar_info(self):
        pass



# CLASE CLIENTE


class Cliente(EntidadBase):

    def __init__(self, id, nombre, email):
        super().__init__(id)

        # Validaciones básicas
        if not nombre:
            raise ErrorDatoInvalido("Nombre vacío")

        if "@" not in email or "." not in email:
            raise ErrorDatoInvalido("Email inválido")

        self.__nombre = nombre   # encapsulado
        self.__email = email

    def mostrar_nombre(self):
        return self._nombre 
        
    def mostrar_email(
        return self.__nombre
     
    def f"cliente:{self.__nombre} - {self._email}"



# CLASE ABSTRACTA SERVICIO


class Servicio(ABC):

    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def calcular_costo(self, horas):
        pass

    @abstractmethod
    def descripcion(self):
        pass



# SERVICIOS CONCRETOS


class ReservaSala(Servicio):

    def calcular_costo(self, horas, precio=50):
        return horas * precio

    def descripcion(self):
        return "Reserva de sala"


class AlquilerEquipo(Servicio):

    def calcular_costo(self, horas, precio=30):
        return horas * precio

    def descripcion(self):
        return "Alquiler de equipo"


class Asesoria(Servicio):

    def calcular_costo(self, horas, precio=100):
        return horas * precio

    def descripcion(self):
        return "Asesoría especializada"



# CLASE RESERVA


class Reserva:

    def __init__(self, cliente, servicio, horas):
        if horas <= 0:
            raise ErrorDatoInvalido("Horas inválidas")

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
            return costo

        except Exception as e:
            registrar_log(str(e))
            raise ErrorOperacion("Error al procesar reserva") from e



# SIMULACIÓN DEL SISTEMA


if __name__ == "__main__":

    print("=== SISTEMA SOFTWARE FJ ===")

    clientes = []
    reservas = []

    try:
        # Cliente válido
        c1 = Cliente(1, "Juan", "juan@email.com")
        clientes.append(c1)

        # Cliente inválido
        try:
            c2 = Cliente(2, "", "malcorreo")
        except ErrorSistema as e:
            print("Error cliente:", e)
            registrar_log(str(e))

        # Servicios
        s1 = ReservaSala("Sala 1")
        s2 = AlquilerEquipo("Proyector")
        s3 = Asesoria("Consultoría")

        # Reserva válida
        r1 = Reserva(c1, s1, 2)
        r1.confirmar()
        costo = r1.procesar()
        print("Reserva exitosa - Costo:", costo)
        reservas.append(r1)

        # Reserva inválida
        try:
            r2 = Reserva(c1, s2, -5)
        except ErrorSistema as e:
            print("Error reserva:", e)
            registrar_log(str(e))

        # Otra reserva
        r3 = Reserva(c1, s3, 1)
        print("Costo asesoría:", r3.procesar())
        reservas.append(r3)

        # Mostrar estados
        print("\nEstado de reservas:")
        for r in reservas:
            print(r.cliente.mostrar_info(), "|", r.estado)

    except Exception as e:
        registrar_log("Error crítico: " + str(e))

    finally:
        print("\nSistema sigue funcionando correctamente ")
