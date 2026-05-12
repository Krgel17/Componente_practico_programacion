# Componente_practico_programacion
Desarrollo de la actividad Fase 4 del Curso Programación

Integrantes:
Elkin Dario Gelis Blanco,
Jorge Mario Huertas Romero,
Kevin Daniel Argel Bautista,
Leonardo Jose Ruidiaz Oliveros,
Wesmy Jey Chaves Gutierrez

**Sistema Integral de Gestión de Clientes, Servicios y Reservas**

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de un **sistema integral orientado a objetos** para la empresa *Software FJ*, el cual permite la gestión de **clientes, servicios y reservas** sin el uso de bases de datos.

Toda la información es manejada mediante **objetos y estructuras en memoria**, utilizando archivos únicamente para el registro de **logs de eventos y errores**.

El sistema está diseñado para ser **modular, extensible y robusto**, aplicando rigurosamente los principios de la Programación Orientada a Objetos (POO) y técnicas avanzadas de manejo de excepciones.

## Objetivo

Construir una aplicación estable que implemente:

- Abstracción
- Herencia
- Polimorfismo
- Encapsulación
- Manejo avanzado de excepciones

El sistema debe continuar funcionando incluso cuando ocurran errores durante la ejecución.


## Arquitectura del Sistema

El proyecto se basa en una arquitectura orientada a objetos que incluye:

### Clases principales

- **Clase abstracta base**
  - Representa entidades generales del sistema.

- **Clase `Cliente`**
  - Manejo de datos personales.
  - Validaciones estrictas.
  - Encapsulación de atributos.

- **Clase abstracta `Servicio`**
  - Base para todos los servicios.
  - Implementa comportamiento común.

- **Servicios especializados (herencia + polimorfismo)**
  - Al menos 3 tipos de servicios:
    - Reservas de salas
    - Alquiler de equipos
    - Asesorías especializadas
  - Métodos sobrescritos para:
    - Cálculo de costos
    - Descripción del servicio
    - Validación de parámetros

- **Clase `Reserva`**
  - Integra cliente + servicio + duración + estado.
  - Permite:
    - Confirmar reservas
    - Cancelar reservas
    - Procesar reservas con manejo de errores


## Funcionalidades del Sistema

- Gestión de clientes en memoria (sin base de datos)
- Creación y administración de servicios
- Registro de reservas
- Validaciones estrictas de datos
- Operaciones con manejo de errores controlado
- Sistema de logs de eventos y errores

## Manejo de Excepciones

El sistema implementa manejo avanzado de errores:

- `try / except`
- Encadenamiento de excepciones
- Excepciones personalizadas

### Tipos de errores manejados

- Datos inválidos
- Parámetros faltantes
- Operaciones no permitidas
- Reservas incorrectas
- Servicios no disponibles
- Cálculos inconsistentes
- Errores generales del sistema

Todos los errores se registran automáticamente en un archivo:
