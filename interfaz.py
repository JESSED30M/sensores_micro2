
import tkinter as tk
from tkinter import ttk
import random

class SistemaMonitoreo:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Monitoreo - Arduino")
        self.root.geometry("450x470")
        self.root.configure(bg="#e3f2fd")  # Fondo general azul claro

        # Estilos
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#e3f2fd", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), background="#e3f2fd", foreground="#0d47a1")
        style.configure("Sensor.TLabel", font=("Segoe UI", 11, "bold"), background="#bbdefb")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)

        # Variables
        self.temp_var = tk.StringVar(value="-- °C")
        self.hum_var = tk.StringVar(value="-- %")
        self.prox_var = tk.StringVar(value="-- cm")
        self.incl_var = tk.StringVar(value="-- °")

        # Título
        ttk.Label(root, text="📟 Sistema de Monitoreo", style="Title.TLabel").pack(pady=15)

        # Marco para lecturas
        sensor_frame = tk.Frame(root, bg="#bbdefb", bd=2, relief="ridge")
        sensor_frame.pack(padx=20, pady=10, fill="x")

        self.create_sensor_display(sensor_frame, " Humedad:", self.hum_var, "#f44336")
        self.create_sensor_display(sensor_frame, " Temperatura:", self.temp_var, "#03a9f4")
        self.create_sensor_display(sensor_frame, " Proximidad:", self.prox_var, "#4caf50")
        self.create_sensor_display(sensor_frame, "otro:", self.incl_var, "#ff9800")

        # Botones coloridos
        btn_frame = tk.Frame(root, bg="#e3f2fd")
        btn_frame.pack(pady=20)

        self.start_btn = tk.Button(btn_frame, text="▶️ Iniciar", command=self.iniciar, bg="#4caf50", fg="white", width=12)
        self.start_btn.grid(row=0, column=0, padx=8)

        self.pause_btn = tk.Button(btn_frame, text="⏸️ Pausar", command=self.pausar, bg="#fbc02d", fg="black", width=12)
        self.pause_btn.grid(row=0, column=1, padx=8)

        self.save_btn = tk.Button(btn_frame, text="💾 Guardar", command=self.guardar, bg="#1976d2", fg="white", width=12)
        self.save_btn.grid(row=0, column=2, padx=8)

    def create_sensor_display(self, parent, label_text, variable, color):
        frame = tk.Frame(parent, bg=color, bd=1, relief="solid")
        frame.pack(pady=7, padx=10, fill="x")

        label = tk.Label(frame, text=label_text, bg=color, fg="white", font=("Segoe UI", 11, "bold"))
        label.pack(side="left", padx=10)

        value = tk.Label(frame, textvariable=variable, bg=color, fg="white", font=("Segoe UI", 11))
        value.pack(side="left")

    def iniciar(self):
        print("Iniciar presionado")
        # Simulación de valores
        self.temp_var.set(f"{random.randint(20, 30)} °C")
        self.hum_var.set(f"{random.randint(40, 60)} %")
        self.prox_var.set(f"{random.randint(10, 50)} cm")
        self.incl_var.set(f"{random.randint(0, 90)} °")

    def pausar(self):
        print("Pausar presionado")

    def guardar(self):
        print("Guardar presionado")

# Ejecutar la app
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaMonitoreo(root)
    root.mainloop()
