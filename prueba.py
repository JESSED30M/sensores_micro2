
import serial
import threading
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import time
import os
import subprocess

# === Configuración del puerto y repo ===#
puerto = 'COM6'  # Cambiar según tu puerto
baudrate = 9600

# Ruta donde tienes tu repositorio de git clonado
ruta_repo = r"C:\Users\migue\Documents\DATOS\Datos_sensores"

arduino = None
lectura_activa = False
datos_guardados = []

# === Función para subir CSV a GitHub ===
def subir_a_github(ruta_csv):
    nombre_archivo = os.path.basename(ruta_csv)
    try:
        comandos = [
            f'cd "{ruta_repo}"',
            f'git add "{nombre_archivo}"',
            f'git commit -m "Nuevo archivo de datos: {nombre_archivo}"',
            'git push'
        ]
        resultado = subprocess.run(" && ".join(comandos), shell=True, capture_output=True, text=True)

        if resultado.returncode == 0:
            messagebox.showinfo("Éxito", f"CSV '{nombre_archivo}' subido correctamente a GitHub.")
        else:
            messagebox.showerror("Error", f"Error al subir a GitHub:\n{resultado.stderr}")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo subir a GitHub.\n{e}")

# === Función para leer datos del Arduino ===
def leer_serial():
    global lectura_activa
    buffer = []
    while lectura_activa:
        try:
            if arduino.in_waiting:
                linea = arduino.readline().decode('utf-8', errors='ignore').strip()

                if "LM35" in linea:
                    buffer = [linea]  # reiniciar buffer con LM35

                    # Capturar las siguientes 4 líneas para audio incluido
                    while len(buffer) < 6:
                        if arduino.in_waiting:
                            nueva_linea = arduino.readline().decode('utf-8', errors='ignore').strip()
                            if nueva_linea:
                                buffer.append(nueva_linea)

                    print("======== MEDICIÓN ========")
                    for l in buffer:
                        print(l)
                    print("==========================\n")

                    actualizar_interfaz(buffer)

        except Exception as e:
            print("Error al leer datos del puerto:", e)

        time.sleep(0.1)

# === Función para actualizar etiquetas de la GUI ===
def actualizar_interfaz(lineas):
    datos = {"LM35": "---", "DHT": "---", "Humedad": "---", "Distancia": "---", "Audio": "---"}
    for l in lineas:
        if "LM35" in l:
            datos["LM35"] = l.split(":")[1].strip()
        elif "DHT11 Temp" in l:
            datos["DHT"] = l.split(":")[1].strip()
        elif "Humedad" in l:
            datos["Humedad"] = l.split(":")[1].strip()
        elif "Distancia" in l:
            datos["Distancia"] = l.split(":")[1].strip()
        elif "Nivel de sonido" in l:
            datos["Audio"] = l.split(":")[1].strip()

    label_lm35.config(text=f"LM35 (°C): {datos['LM35']}")
    label_dht.config(text=f"DHT11 Temp (°C): {datos['DHT']}")
    label_hum.config(text=f"Humedad (%): {datos['Humedad']}")
    label_dist.config(text=f"Distancia (cm): {datos['Distancia']}")
    label_audio.config(text=f"Nivel de sonido (KY-038): {datos['Audio']}")

    datos_guardados.append([
        time.strftime("%Y-%m-%d %H:%M:%S"),
        datos["LM35"],
        datos["DHT"],
        datos["Humedad"],
        datos["Distancia"],
        datos["Audio"]
    ])

# === Funciones de los botones ===
def iniciar():
    global arduino, lectura_activa
    try:
        if not arduino:
            arduino = serial.Serial(puerto, baudrate, timeout=1)
            time.sleep(2)  # espera a que el Arduino reinicie
        lectura_activa = True
        threading.Thread(target=leer_serial, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir {puerto}.\n{e}")

def pausar():
    global lectura_activa
    lectura_activa = False

def guardar_excel_y_csv():
    if not datos_guardados:
        messagebox.showwarning("Atención", "No hay datos para guardar.")
        return

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    nombre_excel = f"datos_sensores_{timestamp}.xlsx"
    nombre_csv = f"datos_sensores_{timestamp}.csv"

    ruta_excel = os.path.join(ruta_repo, nombre_excel)
    ruta_csv = os.path.join(ruta_repo, nombre_csv)

    df = pd.DataFrame(datos_guardados, columns=["FechaHora", "LM35 (°C)", "DHT11 (°C)", "Humedad (%)", "Distancia (cm)", "Nivel de sonido"])

    try:
        df.to_excel(ruta_excel, index=False)
        df.to_csv(ruta_csv, index=False)

        messagebox.showinfo("Guardado", f"Datos guardados en:\n{ruta_excel}\n{ruta_csv}")

        # Subir CSV a GitHub
        subir_a_github(ruta_csv)

        # Vaciar datos para próximas mediciones
        datos_guardados.clear()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar.\n{e}")

# === Interfaz Gráfica ===
ventana = tk.Tk()
ventana.title("Monitor de Sensores Arduino")
ventana.configure(bg="#f0f4f8")
ventana.geometry("460x440")

estilo_label = {"font": ("Arial", 14, "bold"), "bg": "#f0f4f8"}
estilo_titulo = {"font": ("Arial", 16, "bold"), "bg": "#ddeefc", "fg": "#0a3d62", "padx": 10, "pady": 10}

tk.Label(ventana, text="Lectura de Sensores", **estilo_titulo).pack(pady=10, fill="x")

label_lm35 = tk.Label(ventana, text="LM35 (°C): ---", fg="#e74c3c", **estilo_label)
label_dht = tk.Label(ventana, text="DHT11 Temp (°C): ---", fg="#3498db", **estilo_label)
label_hum = tk.Label(ventana, text="Humedad (%): ---", fg="#16a085", **estilo_label)
label_dist = tk.Label(ventana, text="Distancia (cm): ---", fg="#9b59b6", **estilo_label)
label_audio = tk.Label(ventana, text="Nivel de sonido (KY-038): ---", fg="#d35400", **estilo_label)

label_lm35.pack(pady=5)
label_dht.pack(pady=5)
label_hum.pack(pady=5)
label_dist.pack(pady=5)
label_audio.pack(pady=5)

tk.Button(ventana, text="Iniciar", command=iniciar, bg="#2ecc71", fg="white", font=("Arial", 12), width=15).pack(pady=8)
tk.Button(ventana, text="Pausar", command=pausar, bg="#f39c12", fg="white", font=("Arial", 12), width=15).pack(pady=8)
tk.Button(ventana, text="Guardar Excel y CSV", command=guardar_excel_y_csv, bg="#3498db", fg="white", font=("Arial", 12), width=20).pack(pady=8)

ventana.mainloop()







