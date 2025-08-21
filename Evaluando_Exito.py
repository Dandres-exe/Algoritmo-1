import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime
import os

class SistemaVentasExito:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Ventas - Grupo Éxito")
        self.root.geometry("1000x700")
        self.root.configure(bg="#FFF8DC")  # Color amarillo suave

        # Variables para almacenar datos
        self.num_tiendas = 0
        self.num_dias = 0
        self.nombres_tiendas = []
        self.matriz_ventas = []
        self.entries_ventas = []

        self.logo_image = None  # Referencia para la imagen

        # --- NUEVO: Canvas principal con scrollbar ---
        self.main_canvas = tk.Canvas(self.root, bg="#FFF8DC")
        self.main_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.main_scrollbar.pack(side="right", fill="y")

        self.main_frame = tk.Frame(self.main_canvas, bg="#FFF8DC")
        self.main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        self.main_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        # --- FIN NUEVO ---

        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame principal con padding
        # main_frame = tk.Frame(self.root, bg="#FFF8DC", padx=20, pady=20)
        # main_frame.pack(fill="both", expand=True)
        main_frame = self.main_frame  # Usar el frame dentro del canvas

        # Header con espacio para logo
        header_frame = tk.Frame(main_frame, bg="#FFF8DC", height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)

        # Espacio reservado para logo (esquina superior izquierda)
        logo_frame = tk.Frame(header_frame, bg="#FFD700", width=320, height=90, relief="solid", bd=2)
        logo_frame.pack(side="left", padx=(0, 20))
        logo_frame.pack_propagate(False)

        # Cargar y mostrar logo desde archivo PNG usando Tkinter PhotoImage
        try:
            img_path = os.path.join(os.path.dirname(__file__), "Exito.png")
            self.logo_image = tk.PhotoImage(file=img_path)
            # Ajustar tamaño si la imagen es muy grande
            img_width = self.logo_image.width()
            img_height = self.logo_image.height()
            frame_width = 320
            frame_height = 90
            if img_width > frame_width or img_height > frame_height:
                x_sub = max(1, int(img_width / frame_width))
                y_sub = max(1, int(img_height / frame_height))
                self.logo_image = self.logo_image.subsample(x_sub, y_sub)
            self.logo_label = tk.Label(logo_frame, bg="#FFD700", image=self.logo_image)
            self.logo_label.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
        except Exception as e:
            self.logo_label = tk.Label(logo_frame, bg="#FFD700", text="Sin logo")
            self.logo_label.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        # Título principal
        title_label = tk.Label(header_frame, text="SISTEMA DE CONTROL DE VENTAS", 
                              bg="#FFF8DC", font=("Arial", 18, "bold"), fg="#8B4513")
        title_label.pack(side="left", fill="x", expand=True)
        
        # Frame de configuración inicial
        self.config_frame = tk.LabelFrame(main_frame, text="Configuración Inicial", 
                                         bg="#FFFFE0", fg="#8B4513", font=("Arial", 12, "bold"),
                                         relief="ridge", bd=2, padx=15, pady=10)
        self.config_frame.pack(fill="x", pady=(0, 20))
        
        # Número de tiendas
        tiendas_frame = tk.Frame(self.config_frame, bg="#FFFFE0")
        tiendas_frame.pack(fill="x", pady=5)
        
        tk.Label(tiendas_frame, text="Número de tiendas (m):", bg="#FFFFE0", 
                font=("Arial", 10), fg="#8B4513").pack(side="left")
        
        self.entry_tiendas = tk.Entry(tiendas_frame, font=("Arial", 10), width=10, 
                                     bg="white", relief="solid", bd=1)
        self.entry_tiendas.pack(side="left", padx=(10, 0))
        
        # Número de días
        dias_frame = tk.Frame(self.config_frame, bg="#FFFFE0")
        dias_frame.pack(fill="x", pady=5)
        
        tk.Label(dias_frame, text="Número de días (n):", bg="#FFFFE0", 
                font=("Arial", 10), fg="#8B4513").pack(side="left")
        
        self.entry_dias = tk.Entry(dias_frame, font=("Arial", 10), width=10, 
                                  bg="white", relief="solid", bd=1)
        self.entry_dias.pack(side="left", padx=(10, 0))
        
        # Botón para configurar matriz
        btn_configurar = tk.Button(self.config_frame, text="Configurar Matriz", 
                                  command=self.configurar_matriz, bg="#FFD700", 
                                  fg="#8B4513", font=("Arial", 10, "bold"),
                                  relief="raised", bd=2, padx=20)
        btn_configurar.pack(pady=10)
        
        # Frame principal para la matriz (inicialmente oculto)
        self.matriz_frame = tk.Frame(main_frame, bg="#FFF8DC")
        
        # Frame de resultados
        self.resultados_frame = tk.LabelFrame(main_frame, text="Resultados", 
                                            bg="#FFFFE0", fg="#8B4513", 
                                            font=("Arial", 12, "bold"),
                                            relief="ridge", bd=2, padx=15, pady=10)
        
        # Frame de botones de acción
        self.botones_frame = tk.Frame(main_frame, bg="#FFF8DC")
        
    def configurar_matriz(self):
        try:
            self.num_tiendas = int(self.entry_tiendas.get())
            self.num_dias = int(self.entry_dias.get())
            
            if self.num_tiendas <= 0 or self.num_dias <= 0:
                raise ValueError("Los números deben ser positivos")
                
            self.crear_matriz_interfaz()
            
        except ValueError as e:
            messagebox.showerror("Error", "Por favor ingrese números válidos y positivos")
    
    def crear_matriz_interfaz(self):
        # Limpiar frame anterior si existe
        for widget in self.matriz_frame.winfo_children():
            widget.destroy()
        
        self.matriz_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Crear canvas y scrollbar para manejar muchas tiendas/días
        canvas = tk.Canvas(self.matriz_frame, bg="#FFF8DC")
        scrollbar = ttk.Scrollbar(self.matriz_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FFF8DC")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título de la matriz
        titulo_matriz = tk.Label(scrollable_frame, text="REGISTRO DE VENTAS DIARIAS", 
                               bg="#FFF8DC", font=("Arial", 14, "bold"), fg="#8B4513")
        titulo_matriz.pack(pady=10)
        
        # Crear tabla
        tabla_frame = tk.Frame(scrollable_frame, bg="#FFF8DC")
        tabla_frame.pack(padx=20)
        
        # Headers
        tk.Label(tabla_frame, text="TIENDA", bg="#FFD700", fg="#8B4513", 
                font=("Arial", 10, "bold"), relief="solid", bd=1, width=20).grid(row=0, column=0, sticky="nsew")
        
        for dia in range(self.num_dias):
            tk.Label(tabla_frame, text=f"DÍA {dia + 1}", bg="#FFD700", fg="#8B4513", 
                    font=("Arial", 10, "bold"), relief="solid", bd=1, width=12).grid(row=0, column=dia + 1, sticky="nsew")
        
        # Crear entries para nombres de tiendas y ventas
        self.nombres_tiendas = []
        self.entries_ventas = []
        
        for tienda in range(self.num_tiendas):
            # Entry para nombre de tienda
            entry_nombre = tk.Entry(tabla_frame, font=("Arial", 9), width=20, 
                                  bg="white", relief="solid", bd=1)
            entry_nombre.grid(row=tienda + 1, column=0, padx=1, pady=1, sticky="nsew")
            entry_nombre.insert(0, f"Tienda {tienda + 1}")
            self.nombres_tiendas.append(entry_nombre)
            
            # Entries para ventas diarias
            fila_ventas = []
            for dia in range(self.num_dias):
                entry_venta = tk.Entry(tabla_frame, font=("Arial", 9), width=12, 
                                     bg="white", relief="solid", bd=1)
                entry_venta.grid(row=tienda + 1, column=dia + 1, padx=1, pady=1, sticky="nsew")
                entry_venta.insert(0, "0.00")
                fila_ventas.append(entry_venta)
            
            self.entries_ventas.append(fila_ventas)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mostrar frames de resultados y botones
        self.resultados_frame.pack(fill="x", pady=(0, 20))
        self.botones_frame.pack(fill="x")
        self.crear_botones()
    
    def crear_botones(self):
        # Limpiar botones anteriores
        for widget in self.botones_frame.winfo_children():
            widget.destroy()
        
        # Botón calcular totales
        btn_calcular = tk.Button(self.botones_frame, text="📊 Calcular Totales", 
                               command=self.calcular_totales, bg="#FFD700", 
                               fg="#8B4513", font=("Arial", 11, "bold"),
                               relief="raised", bd=2, padx=20, pady=5)
        btn_calcular.pack(side="left", padx=5)
        
        # Botón guardar CSV
        btn_guardar = tk.Button(self.botones_frame, text="💾 Guardar CSV", 
                              command=self.guardar_csv, bg="#90EE90", 
                              fg="#8B4513", font=("Arial", 11, "bold"),
                              relief="raised", bd=2, padx=20, pady=5)
        btn_guardar.pack(side="left", padx=5)
        
        # Botón cargar CSV
        btn_cargar = tk.Button(self.botones_frame, text="📁 Cargar CSV", 
                             command=self.cargar_csv, bg="#87CEEB", 
                             fg="#8B4513", font=("Arial", 11, "bold"),
                             relief="raised", bd=2, padx=20, pady=5)
        btn_cargar.pack(side="left", padx=5)
        
        # Botón limpiar
        btn_limpiar = tk.Button(self.botones_frame, text="🗑️ Limpiar Todo", 
                              command=self.limpiar_datos, bg="#FFB6C1", 
                              fg="#8B4513", font=("Arial", 11, "bold"),
                              relief="raised", bd=2, padx=20, pady=5)
        btn_limpiar.pack(side="right", padx=5)
    
    def calcular_totales(self):
        try:
            # Limpiar resultados anteriores
            for widget in self.resultados_frame.winfo_children():
                widget.destroy()
            
            # Obtener datos de la matriz
            self.matriz_ventas = []
            nombres_finales = []
            
            for tienda in range(self.num_tiendas):
                nombre_tienda = self.nombres_tiendas[tienda].get().strip()
                nombres_finales.append(nombre_tienda)
                
                fila_ventas = []
                for dia in range(self.num_dias):
                    venta = float(self.entries_ventas[tienda][dia].get())
                    fila_ventas.append(venta)
                
                self.matriz_ventas.append(fila_ventas)
            
            # Calcular totales por tienda (recorrido por columnas)
            totales_tiendas = []
            for tienda in range(self.num_tiendas):
                total_tienda = sum(self.matriz_ventas[tienda])
                totales_tiendas.append(total_tienda)
            
            # Mostrar resultados
            titulo_resultados = tk.Label(self.resultados_frame, text="💰 TOTALES DE VENTAS POR TIENDA", 
                                       bg="#FFFFE0", font=("Arial", 12, "bold"), fg="#8B4513")
            titulo_resultados.pack(pady=5)
            
            # Frame con scrollbar para resultados
            results_canvas = tk.Canvas(self.resultados_frame, bg="#FFFFE0", height=150)
            results_scrollbar = ttk.Scrollbar(self.resultados_frame, orient="vertical", command=results_canvas.yview)
            results_scrollable = tk.Frame(results_canvas, bg="#FFFFE0")
            
            results_scrollable.bind(
                "<Configure>",
                lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
            )
            
            results_canvas.create_window((0, 0), window=results_scrollable, anchor="nw")
            results_canvas.configure(yscrollcommand=results_scrollbar.set)
            
            # Mostrar cada total
            total_general = 0
            for i, (nombre, total) in enumerate(zip(nombres_finales, totales_tiendas)):
                resultado_frame = tk.Frame(results_scrollable, bg="#FFFACD", relief="solid", bd=1)
                resultado_frame.pack(fill="x", padx=10, pady=2)
                
                tk.Label(resultado_frame, text=f"{nombre}:", bg="#FFFACD", 
                        font=("Arial", 10, "bold"), fg="#8B4513").pack(side="left", padx=10, pady=5)
                
                tk.Label(resultado_frame, text=f"${total:,.2f}", bg="#FFFACD", 
                        font=("Arial", 10), fg="#006400").pack(side="right", padx=10, pady=5)
                
                total_general += total
            
            # Total general
            total_frame = tk.Frame(results_scrollable, bg="#FFD700", relief="solid", bd=2)
            total_frame.pack(fill="x", padx=10, pady=5)
            
            tk.Label(total_frame, text="TOTAL GENERAL:", bg="#FFD700", 
                    font=("Arial", 11, "bold"), fg="#8B4513").pack(side="left", padx=10, pady=8)
            
            tk.Label(total_frame, text=f"${total_general:,.2f}", bg="#FFD700", 
                    font=("Arial", 11, "bold"), fg="#006400").pack(side="right", padx=10, pady=8)
            
            results_canvas.pack(side="left", fill="both", expand=True)
            results_scrollbar.pack(side="right", fill="y")
            
            # --- NO limpiar ni ocultar los botones de acción ---
            # self.botones_frame.pack(fill="x")  # Ya está visible, no se oculta
            # --- FIN CORRECCIÓN ---

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos en todas las celdas de ventas")
    
    def guardar_csv(self):
        if not self.matriz_ventas:
            messagebox.showwarning("Advertencia", "Primero debe calcular los totales")
            return

        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Guardar datos de ventas",
                initialfile=f"ventas_exito_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"  # <-- corregido aquí
            )

            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)

                    # Escribir header
                    header = ['Tienda'] + [f'Día {i+1}' for i in range(self.num_dias)] + ['Total']
                    writer.writerow(header)

                    # Escribir datos
                    for tienda in range(self.num_tiendas):
                        nombre_tienda = self.nombres_tiendas[tienda].get()
                        fila = [nombre_tienda] + self.matriz_ventas[tienda] + [sum(self.matriz_ventas[tienda])]
                        writer.writerow(fila)

                    # Escribir información adicional
                    writer.writerow([])
                    writer.writerow(['Información del reporte'])
                    writer.writerow(['Fecha de generación:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                    writer.writerow(['Número de tiendas:', self.num_tiendas])
                    writer.writerow(['Número de días evaluados:', self.num_dias])
                    total_general = sum(sum(self.matriz_ventas[tienda]) for tienda in range(self.num_tiendas))
                    writer.writerow(['Total general:', total_general])

                messagebox.showinfo("Éxito", f"Datos guardados exitosamente en:\n{filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo:\n{str(e)}")
    
    def cargar_csv(self):
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Cargar datos de ventas"
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    data = list(reader)
                
                if len(data) < 2:
                    messagebox.showerror("Error", "El archivo CSV no tiene el formato correcto")
                    return
                
                # Leer header para determinar dimensiones
                header = data[0]
                self.num_dias = len(header) - 2  # -2 porque hay 'Tienda' y 'Total'
                self.num_tiendas = len(data) - 1  # -1 por el header
                
                # Buscar donde terminan los datos reales
                for i, row in enumerate(data[1:], 1):
                    if not row or len(row) < 2:  # Fila vacía o incompleta
                        self.num_tiendas = i - 1
                        break
                
                # Actualizar entries de configuración
                self.entry_tiendas.delete(0, tk.END)
                self.entry_tiendas.insert(0, str(self.num_tiendas))
                self.entry_dias.delete(0, tk.END)
                self.entry_dias.insert(0, str(self.num_dias))
                
                # Crear matriz con datos cargados
                self.crear_matriz_interfaz()
                
                # Llenar datos
                for tienda in range(self.num_tiendas):
                    row_data = data[tienda + 1]  # +1 por el header
                    
                    # Nombre de tienda
                    self.nombres_tiendas[tienda].delete(0, tk.END)
                    self.nombres_tiendas[tienda].insert(0, row_data[0])
                    
                    # Ventas diarias
                    for dia in range(self.num_dias):
                        self.entries_ventas[tienda][dia].delete(0, tk.END)
                        self.entries_ventas[tienda][dia].insert(0, str(row_data[dia + 1]))
                
                messagebox.showinfo("Éxito", "Datos cargados exitosamente")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo:\n{str(e)}")
    
    def limpiar_datos(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea limpiar todos los datos?"):
            # Limpiar configuración
            self.entry_tiendas.delete(0, tk.END)
            self.entry_dias.delete(0, tk.END)
            
            # Ocultar matriz y resultados
            self.matriz_frame.pack_forget()
            self.resultados_frame.pack_forget()
            self.botones_frame.pack_forget()
            
            # Limpiar variables
            self.num_tiendas = 0
            self.num_dias = 0
            self.nombres_tiendas = []
            self.matriz_ventas = []
            self.entries_ventas = []
            
            # Limpiar frames
            for widget in self.resultados_frame.winfo_children():
                widget.destroy()

def main():
    root = tk.Tk()
    app = SistemaVentasExito(root)
    root.mainloop()

if __name__ == "__main__":
    main()