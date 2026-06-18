# =====================================================================
# TRABAJO PRÁCTICO INTEGRADOR - ORGANIZACIÓN EMPRESARIAL (UTN)
# Simulación de Chatbot: Gestión de Solicitud de Vacaciones (Con Restricción Temporal)
# =====================================================================

from datetime import datetime, timedelta

# Persistencia de Datos
BASE_DE_DATOS = {
    "1001": {"nombre": "Bárbara", "dias_disponibles": 14},
    "1002": {"nombre": "Juan Pérez", "dias_disponibles": 7},
    "1003": {"nombre": "Ana Gómez", "dias_disponibles": 21},
    "1004": {"nombre": "Nicolás Ghersinich", "dias_disponibles": 10},
}
for i in range(1005, 1051):
    BASE_DE_DATOS[str(i)] = {"nombre": f"Empleado Simulado {i-1000}", "dias_disponibles": 14}


class VacacionesChatbot:
    def __init__(self):
        self.estado_actual = "INICIO"
        self.usuario_legajo = None
        self.usuario_nombre = None
        self.dias_solicitados = None

    def procesar_mensaje(self, mensaje_usuario):
        mensaje = mensaje_usuario.strip()

        # 1. ESTADO: INICIO
        if self.estado_actual == "INICIO":
            if mensaje.lower() in ["/start", "hola", "buen día", "buenas"]:
                self.estado_actual = "ESPERANDO_LEGAJO"
                return (
                    "Bot: ¡Hola! Bienvenido al asistente virtual de RRHH.\n"
                    "Por favor, ingresá tu Número de Legajo:"
                )
            else:
                return "Bot: Por favor, enviá 'Hola' o '/start' para iniciar el proceso."

        # 2. ESTADO: ESPERANDO_LEGAJO
        elif self.estado_actual == "ESPERANDO_LEGAJO":
            if mensaje in BASE_DE_DATOS:
                self.usuario_legajo = mensaje
                self.usuario_nombre = BASE_DE_DATOS[mensaje]["nombre"]
                self.estado_actual = "ESPERANDO_DIAS"
                saldo = BASE_DE_DATOS[mensaje]["dias_disponibles"]
                return (
                    f"🤖 Bot: Legajo válido. Hola {self.usuario_nombre}.\n"
                    f"Tu saldo actual es de {saldo} días.\n"
                    f"¿Cuántos días deseás solicitar?"
                )
            else:
                return "Bot (Error): El legajo no existe. Intentalo de nuevo:"

        # 3. ESTADO: ESPERANDO_DIAS (Validación de cantidad de días)
        elif self.estado_actual == "ESPERANDO_DIAS":
            try:
                self.dias_solicitados = int(mensaje)
            except ValueError:
                return "Bot (Error): Entrada inválida. Ingresá un número entero:"

            saldo_disponible = BASE_DE_DATOS[self.usuario_legajo]["dias_disponibles"]

            if self.dias_solicitados <= 0:
                return "Bot (Error): La cantidad debe ser mayor a cero. Ingresá otro número:"
            elif self.dias_solicitados > saldo_disponible:
                return (
                    f"Bot (Error): Saldo insuficiente. Solicitaste {self.dias_solicitados} días "
                    f"pero disponés de {saldo_disponible}. Ingresá una cantidad menor:"
                )
            else:
                # Si pasa el filtro de días, avanzamos al nuevo estado temporal
                self.estado_actual = "ESPERANDO_FECHA"
                return (
                    "Bot: Cantidad de días disponible.\n"
                    "RESTRICCIÓN: Las solicitudes deben cargarse con un mínimo de 15 días de anticipación.\n"
                    "Por favor, ingresá la fecha de inicio deseada (Formato: DD/MM/AAAA):"
                )

        # 4. ESTADO NUEVO: ESPERANDO_FECHA (Validación de Restricción Temporal de 15 días)
        elif self.estado_actual == "ESPERANDO_FECHA":
            try:
                # Convierte el texto del usuario en una fecha real
                fecha_inicio = datetime.strptime(mensaje, "%d/%m/%r").date() if "%r" in mensaje else datetime.strptime(mensaje, "%d/%m/%Y").date()
            except ValueError:
                return "Bot (Error): Formato de fecha incorrecto. Usá el formato DD/MM/AAAA (Ejemplo: 25/12/2026):"

            fecha_hoy = datetime.now().date()
            # Calculamos cuántos días de anticipación hay entre hoy y la fecha elegida
            dias_anticipacion = (fecha_inicio - fecha_hoy).days

            # COMPUERTA LOGICA: ¿Días de anticipación >= 15?
            if dias_anticipacion >= 15:
                # CAMINO FELIZ: Cumple con los días y con la anticipación
                saldo_disponible = BASE_DE_DATOS[self.usuario_legajo]["dias_disponibles"]
                nuevo_saldo = saldo_disponible - self.dias_solicitados
                BASE_DE_DATOS[self.usuario_legajo]["dias_disponibles"] = nuevo_saldo
                
                self.estado_actual = "FINALIZADO"
                return (
                    f"Bot (Aprobado): ¡Solicitud registrada con éxito!\n"
                    f"Inicio de vacaciones: {fecha_inicio.strftime('%d/%m/%Y')} ({dias_anticipacion} días de anticipación).\n"
                    f"Nuevo saldo disponible: {nuevo_saldo} días. ¡Que disfrutes tu descanso!\n"
                    f"[Proceso Finalizado]"
                )
            else:
                # CAMINO INFELIZ TEMPORAL: No cumple la anticipación, se queda en el estado para reintentar
                return (
                    f"Bot (Error): No se cumple la restricción temporal. La fecha ingresada está a solo "
                    f"{dias_anticipacion} días de anticipación (Mínimo requerido: 15 días).\n"
                    f"Por favor, ingresá una fecha posterior (DD/MM/AAAA):"
                )


# --- Ejecución ---
if __name__ == "__main__":
    bot = VacacionesChatbot()
    print("==================================================")
    print("    --- SIMULADOR CON RESTRICCIÓN TEMPORAL ---")
    print("==================================================")

    while bot.estado_actual != "FINALIZADO":
        entrada = input("\nEmpleado: ")
        respuesta_bot = bot.procesar_mensaje(entrada)
        print(respuesta_bot)