import tkinter as tk
import sqlite3

class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestor de Productos")
        self.ventana.geometry("820x450")
        self.ventana.configure(bg="#e6f2e6")

        # --- Frame para el formulario ---
        self.frame_formulario = tk.Frame(self.ventana, bg="#e6f2e6")
        self.frame_formulario.pack(padx=10, pady=10)
        
        # Campos del formulario
        self.campo_nombre = self.crear_label("Nombre:", 0)
        self.campo_fecha = self.crear_label("Fecha Caducidad (AAAA-MM-DD):", 1)
        self.campo_cat = self.crear_label("Categoría:", 2)
        self.campo_marca = self.crear_label("Marca:", 3)
        self.campo_prec = self.crear_label("Precio:", 4)
        self.campo_stock = self.crear_label("Stock:", 5)

        # --- Frame para los botones ---
        self.frame_botones = tk.Frame(self.ventana, bg="#e6f2e6")
        self.frame_botones.pack(pady=10)

        # --- Botones ---
        boton_add = tk.Button(self.frame_botones, text="Añadir Producto",
                              bg="#b2d8b2", fg="#004d00", activebackground="#a3cfa3",
                              command=self.añadido)
        boton_update = tk.Button(self.frame_botones, text="Modificar Producto",
                                 bg="#b2d8b2", fg="#004d00", activebackground="#a3cfa3",
                                 command=self.modificado)
        boton_delete = tk.Button(self.frame_botones, text="Eliminar Producto",
                                 bg="#b2d8b2", fg="#004d00", activebackground="#a3cfa3",
                                 command=self.eliminado)

        boton_add.grid(row=0, column=0, padx=10, pady=10)
        boton_update.grid(row=0, column=1, padx=10, pady=10)
        boton_delete.grid(row=0, column=2, padx=10, pady=10)

        # --- Lista de productos ---
        etiqueta_lista = tk.Label(self.ventana, text="Lista de productos:", bg="#e6f2e6", fg="#2e8b57")
        etiqueta_lista.pack()

        self.lista_tareas = tk.Listbox(self.ventana, width=60, height=10, bg="#f0fff0", fg="#006400")
        self.lista_tareas.pack(padx=10, pady=5)

    def crear_label(self, texto, fila):
        etiqueta = tk.Label(self.frame_formulario, text=texto, bg="#e6f2e6", fg="#2e8b57")
        etiqueta.grid(row=fila, column=0, sticky="e")
        campo = tk.Entry(self.frame_formulario, bg="#f0fff0", fg="#006400")
        campo.grid(row=fila, column=1)
        return campo

    # --- Funciones de botones ---
    def añadido(self):
        print("Has añadido un nuevo producto")

    def modificado(self):
        print("Has modificado un producto")

    def eliminado(self):
        print("Has eliminado un producto")

    # --- PASO 1: Conectar a la base de datos ---
# Se crea el archivo 'tareas.db' si no existe
conexion = sqlite3.connect('productos.db')

# Para poder enviar comandos, necesitamos un "cursor"
cursor = conexion.cursor()

# --- PASO 2: Ejecutar un comando SQL ---
# Usamos un string multilínea con triples comillas para que el SQL sea más legible
comando_sql = """
CREATE TABLE IF NOT EXISTS producto (
    id INTEGER PRIMARY KEY,
    nombre TEXT ,
    fecha_caducidad TEXT,
    precio TEXT,
    categoria TEXT,
    marca TEXT, 
    stock INTEGER
)
"""
# 'IF NOT EXISTS' evita que nos dé un error si la tabla ya ha sido creada
cursor.execute(comando_sql)

# Para que los cambios se guarden de forma permanente, hacemos un "commit"
conexion.commit()

# --- PASO 3: Cerrar la conexión ---
conexion.close()

print("Tabla 'Producto' creada con éxito (si no existía ya).")

# --- Lanzar la aplicación ---
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = App(ventana_principal)
    ventana_principal.mainloop()
