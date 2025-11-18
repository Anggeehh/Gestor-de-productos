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


        
# --- Conexión a la Base de Datos ---
        self.conexion = sqlite3.connect('productos.db')
        self.cursor = self.conexion.cursor()
        self.crear_tabla()
# ... (resto de la clase) ...

    def crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha_caducidad TEXT,
            categoria TEXT,
            marca TEXT,
            precio TEXT,
            stock INTEGER
        )
        """)
        self.conexion.commit()
        print("Tabla creada con éxito (si no existía ya).")


    def actualizar_lista(self):
        self.lista_productos.delete(0, tk.END)
        self.cursor.execute("SELECT id, nombre, fecha_caducidad, categoria, marca, precio, stock FROM producto ORDER BY id")
        filas = self.cursor.fetchall()
        for fila in filas:
            id_p, nombre, fecha, categoria, marca, precio, stock = fila
            texto = f"{id_p}: {nombre} | {fecha or '-'} | {categoria or '-'} | {marca or '-'} | {precio or '-'} | stock: {stock if stock is not None else '-'}"
            self.lista_productos.insert(tk.END, texto)
    
    def limpiar_campos(self):
        self.campo_nombre.delete(0, tk.END)
        self.campo_fecha.delete(0, tk.END)
        self.campo_categoria.delete(0, tk.END)
        self.campo_marca.delete(0, tk.END)
        self.campo_precio.delete(0, tk.END)
        self.campo_stock.delete(0, tk.END)
        self.lista_productos.selection_clear(0, tk.END)

    def añadir_producto(self):
        nombre = self.campo_nombre.get().strip()
        fecha = self.campo_fecha.get().strip()
        categoria = self.campo_categoria.get().strip()
        marca = self.campo_marca.get().strip()
        precio = self.campo_precio.get().strip()
        stock_text = self.campo_stock.get().strip()
        
        if not nombre:
            messagebox.showwarning("Campo vacío", "El campo Nombre es obligatorio.")
            return

        try:
            stock = int(stock_text) if stock_text != "" else None
        except ValueError:
            messagebox.showwarning("Valor incorrecto", "Stock debe ser un número entero.")
            return

        self.cursor.execute(
            "INSERT INTO producto (nombre, fecha_caducidad, categoria, marca, precio, stock) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, fecha, categoria, marca, precio, stock)
        )
        self.conexion.commit()
        self.limpiar_campos()
        self.actualizar_lista()
        messagebox.showinfo("Éxito", "Producto añadido correctamente.")
    
    def get_id_seleccionado(self):
            try:
                seleccionado = self.lista_productos.get(self.lista_productos.curselection())
                id_producto = int(seleccionado.split(":")[0])
                return id_producto
            except (tk.TclError, IndexError, ValueError):
                return None

    def cargar_producto_seleccionado(self, event):
        if not self.lista_productos.curselection():
            return
        id_p = self.get_id_seleccionado()
        if id_p:
            self.cursor.execute("SELECT nombre, fecha_caducidad, categoria, marca, precio, stock FROM producto WHERE id = ?", (id_p,))
            fila = self.cursor.fetchone()
            if fila:
                nombre, fecha, categoria, marca, precio, stock = fila
                self.campo_nombre.delete(0, tk.END); self.campo_nombre.insert(0, nombre)
                self.campo_fecha.delete(0, tk.END); self.campo_fecha.insert(0, fecha)
                self.campo_categoria.delete(0, tk.END); self.campo_categoria.insert(0, categoria)
                self.campo_marca.delete(0, tk.END); self.campo_marca.insert(0, marca)
                self.campo_precio.delete(0, tk.END); self.campo_precio.insert(0, precio)
                self.campo_stock.delete(0, tk.END); self.campo_stock.insert(0, str(stock) if stock is not None else "SI")

# --- Lanzar la aplicación ---
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = App(ventana_principal)
    ventana_principal.mainloop()
