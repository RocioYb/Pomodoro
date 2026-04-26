import tkinter as tk
from tkinter import messagebox #messagebox es para mostrar ventanas emergentes con mensajes


# --- Variables Globales ---
corriendo = False
tiempo_total_segundos = 0
tiempo_restante_segundos = 0
estado_temporizador = "Detenido" # Puede ser "Concentración", "Descanso" o "Detenido"
job_id = None
MINUTOS_DESCANSO = 5

# --- Lógica del Temporizador ---

def formatear_tiempo(segundos):
    """Convierte segundos totales a formato MM:SS."""
    minutos = segundos // 60
    segundos_restantes = segundos % 60
    return f"{minutos:02d}:{segundos_restantes:02d}"

def actualizar_temporizador():
    """Actualiza la cuenta regresiva cada segundo."""
    global tiempo_restante_segundos, estado_temporizador, job_id, corriendo
    
    if tiempo_restante_segundos > 0:
        tiempo_restante_segundos -= 1
        
        # Muestra el tiempo restante
        reloj.config(text=formatear_tiempo(tiempo_restante_segundos))
        
        # Vuelve a llamar a la función después de 1 segundo (1000 ms)
        job_id = ventana.after(1000, actualizar_temporizador)
        
    else:
        # El tiempo actual ha terminado
        parar_temporizador()
        
        if estado_temporizador == "Concentración":
            messagebox.showinfo("¡Tiempo Terminado!", "¡Tu tiempo de concentración ha finalizado!\n¡Comienza el Descanso!")
            iniciar_descanso()
        elif estado_temporizador == "Descanso":
            messagebox.showinfo("¡Descanso Terminado!", "El descanso ha terminado. ¡Listo para otro bloque!")
            # Vuelve al estado inicial para iniciar un nuevo ciclo
            resetear_temporizador()


def iniciar_descanso():
    """Configura e inicia el temporizador de 5 minutos de descanso."""
    global tiempo_restante_segundos, estado_temporizador
    
    tiempo_restante_segundos = MINUTOS_DESCANSO * 60
    estado_temporizador = "Descanso"
    reloj.config(fg='green', bg='lightyellow') # Cambia el color para indicar Descanso
    label_estado.config(text="ESTADO: ⏸️ Descanso de 5 min")
    
    # Inicia la cuenta regresiva del descanso
    job_id = ventana.after(1000, actualizar_temporizador)


def iniciar_concentracion():
    """Obtiene los minutos y empieza la cuenta regresiva."""
    global tiempo_total_segundos, tiempo_restante_segundos, estado_temporizador, corriendo
    
    if corriendo:
        return # Evita iniciar si ya está en marcha
    
    try:
        minutos_input = int(entrada_minutos.get())
        if minutos_input <= 0:
            messagebox.showerror("Error", "Ingresa un número positivo de minutos.")
            return
    except ValueError:
        messagebox.showerror("Error", "Ingresa un número válido para los minutos.")
        return
        
    # Inicializa el temporizador de concentración
    tiempo_total_segundos = minutos_input * 60
    tiempo_restante_segundos = tiempo_total_segundos
    estado_temporizador = "Concentración"
    corriendo = True
    
    # Configura la interfaz y empieza
    reloj.config(fg='white', bg='blue') # Color para Concentración
    label_estado.config(text=f"ESTADO: 🧠 Concentración por {minutos_input} min")
    boton_inicio.config(text="Pausar", command=pausar_temporizador)
    
    actualizar_temporizador()


def pausar_temporizador():
    """Pausa el temporizador actual (Concentración o Descanso)."""
    global corriendo, job_id
    if corriendo:
        corriendo = False
        if job_id:
            ventana.after_cancel(job_id)
            job_id = None
        
        # Cambia los botones y el estado visual
        boton_inicio.config(text="Reanudar", command=reanudar_temporizador)
        label_estado.config(text=f"ESTADO: ⏸️ Pausado ({estado_temporizador})")
        reloj.config(fg='red')


def reanudar_temporizador():
    """Reanuda la cuenta regresiva."""
    global corriendo
    if not corriendo:
        corriendo = True
        
        # Vuelve a configurar los botones y el estado visual
        boton_inicio.config(text="Pausar", command=pausar_temporizador)
        label_estado.config(text=f"ESTADO: {'🧠 Concentración' if estado_temporizador == 'Concentración' else '⏸️ Descanso'}")
        reloj.config(fg='white' if estado_temporizador == 'Concentración' else 'green')
        
        # Reanuda el bucle
        actualizar_temporizador()


def parar_temporizador():
    """Detiene cualquier temporizador en marcha sin resetear el tiempo."""
    global corriendo, job_id
    corriendo = False
    if job_id:
        ventana.after_cancel(job_id)
        job_id = None


def resetear_temporizador():
    """Detiene y reinicia el estado y la interfaz."""
    global corriendo, tiempo_restante_segundos, estado_temporizador
    parar_temporizador()
    corriendo = False
    tiempo_restante_segundos = 0
    estado_temporizador = "Detenido"
    
    # Restaura la interfaz
    reloj.config(text="00:00", fg='black', bg='lightgray')
    label_estado.config(text="ESTADO: 🛑 Detenido. Ingresa minutos.")
    boton_inicio.config(text="Iniciar", command=iniciar_concentracion)
    
# --- Configuración de la Ventana Principal (Tkinter) ---

ventana = tk.Tk()
ventana.title('Temporizador de Concentración (Pomodoro)')
ventana.geometry('400x350')
ventana.resizable(False, False)

# 1. Entrada de Minutos de Concentración
frame_entrada = tk.Frame(ventana, pady=10)
frame_entrada.pack()

tk.Label(frame_entrada, text="Minutos de Concentración:", font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
entrada_minutos = tk.Entry(frame_entrada, width=5, font=('Arial', 12), justify='center')
entrada_minutos.insert(0, "25") # Valor por defecto
entrada_minutos.pack(side=tk.LEFT)

# 2. Etiqueta de Estado
label_estado = tk.Label(ventana, text="ESTADO: 🛑 Detenido. Ingresa minutos.", font=('Arial', 12, 'bold'), pady=5)
label_estado.pack()

# 3. Etiqueta del Temporizador (Reloj)
reloj = tk.Label(ventana, font=('Arial', 70), bg='lightgray', fg='black', text='00:00')
reloj.pack(anchor='center', pady=10, padx=10)

# 4. Frame y Botones de Control
frame_botones = tk.Frame(ventana, pady=10)
frame_botones.pack()

boton_inicio = tk.Button(frame_botones, text='Iniciar', command=iniciar_concentracion, font=('Arial', 14), bg='blue', fg='white', width=10)
boton_inicio.pack(side=tk.LEFT, padx=10)

boton_reset = tk.Button(frame_botones, text='Resetear', command=resetear_temporizador, font=('Arial', 14), bg='red', fg='white', width=10)
boton_reset.pack(side=tk.LEFT, padx=10)

# Inicializa el estado visual del temporizador
resetear_temporizador()

ventana.mainloop()