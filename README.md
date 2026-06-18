# tpi_organizacion_empresarial
# Sistema de Gestión de Vacaciones Automatizado via Chatbot

## Cátedra: Organización Empresarial
**Tecnicatura Universitaria en Programación (TUP a Distancia)** **Universidad Tecnológica Nacional (UTN)**

##Integrante
* **Kolman, Barbara Stefania**


# Descripción del Proyecto
Este proyecto consiste en el diseño, modelado y simulación de un **asistente virtual (Chatbot) para la gestión automatizada de solicitudes de vacaciones** en el área de Recursos Humanos. 

El objetivo principal es transformar un proceso tradicionalmente manual y burocrático (Flujo As-Is) en un proceso optimizado, inmediato y autónomo (Flujo To-Be), garantizando la disponibilidad del servicio las 24 horas y reduciendo la carga operativa del departamento de RRHH.


## Decisiones Técnicas y Arquitectura

El desarrollo del software se diseñó implementando los siguientes conceptos:

* **Máquina de Estados Finitos:** El chatbot (`VacacionesChatbot`) utiliza variables de control para mantener la "memoria" de la sesión. Sabe en todo momento en qué fase del diálogo se encuentra el empleado (`INICIO`, `ESPERANDO_LEGAJO`, `ESPERANDO_DIAS`, `ESPERANDO_FECHA`, `FINALIZADO`).
* **Persistencia de Datos Simulada:** Se implementó una base de datos en memoria utilizando diccionarios aninados en Python para albergar de forma dinámica una nómina de **50 empleados** (con sus respectivos legajos, nombres y saldos reales de días).
* **Robustez ante el "Camino Infeliz" (Unhappy Path):** El sistema utiliza bloques de control de excepciones (`try/except ValueError`) para evitar caídas ante entradas alfabéticas inválidas en campos numéricos o fechas mal formateadas.

### Reglas de Negocio Dinámicas e Incorporadas:
1. **Validación de Identidad:** El legajo debe existir obligatoriamente en la base de datos.
2. **Validación de Saldo Cuantitativo:** Los días solicitados deben ser mayores a cero y menores o iguales al saldo disponible del empleado.
3. **Restricción Temporal Estricta:** La fecha de inicio elegida por el trabajador debe cargarse con un **mínimo de 15 días de anticipación** respecto a la fecha del día corriente.


## Modelo de Procesos (BPMN 2.0)
El flujo lógico implementado en el código de Python es una traducción exacta del modelo de procesos optimizado (**To-Be**). Las bifurcaciones lógicas del código responden directamente a las compuertas (*gateways*) de decisión diseñadas en los carriles del **Empleado** y del **Chatbot**.



