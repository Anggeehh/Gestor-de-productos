import tkinter as tk
from tkinter import messagebox
import sqlite3

class App:
    def __init__(self, ventana):
        # Guarda la ventana raíz y ajusta propiedades básicas
        self.ventana = ventana
        self.ventana.title("Gestor de Productos")      # Título de la ventana
        self.ventana.geometry("820x450")               # Tamaño inicial de la ventana
        self.ventana.configure(bg="#e6f2e6")           # Color de fondo

        # Conexión a la Base de Datos SQLite (crea el fichero si no existe)
        self.conexion = sqlite3.connect('productos.db') # Abre/crea productos.db
        self.cursor = self.conexion.cursor()            # Cursor para ejecutar SQL
        self.crear_tabla()                              # Garantiza que la tabla exista

        # Frames: contenedores para organizar controles (formulario, botones, lista)
        frame_formulario = tk.Frame(self.ventana, bg="#e6f2e6", pady=10)
        frame_botones = tk.Frame(self.ventana, bg="#e6f2e6")
        frame_lista = tk.Frame(self.ventana, bg="#e6f2e6", pady=10)

        # Empaquetado de los frames en la ventana
        frame_formulario.pack()
        frame_botones.pack()
        frame_lista.pack(fill=tk.BOTH, expand=True)     # La lista se expande al redimensionar

        # Helpers (lambdas) para crear etiquetas y entradas con estilos consistentes
        etiqueta = lambda txt, r, c: tk.Label(frame_formulario, text=txt, bg="#e6f2e6", fg="#2e8b57")
        entrada = lambda r, c, width=40: tk.Entry(frame_formulario, bg="#f0fff0", fg="#006400", width=width)

        # Campo: Nombre
        etiqueta("Nombre:", 0, 0).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.campo_nombre = entrada(0, 1)
        self.campo_nombre.grid(row=0, column=1, padx=5, pady=5)

        # Campo: Fecha caducidad (texto YYYY-MM-DD, sin validación estricta aquí)
        etiqueta("Fecha Caducidad (AAAA-MM-DD):", 1, 0).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.campo_fecha = entrada(1, 1)
        self.campo_fecha.grid(row=1, column=1, padx=5, pady=5)

        # Campo: Categoría
        etiqueta("Categoría:", 2, 0).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.campo_categoria = entrada(2, 1)
        self.campo_categoria.grid(row=2, column=1, padx=5, pady=5)

        # Campo: Marca
        etiqueta("Marca:", 3, 0).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.campo_marca = entrada(3, 1)
        self.campo_marca.grid(row=3, column=1, padx=5, pady=5)

        # Campo: Precio (guardado como texto; podría ser numérico si se valida)
        etiqueta("Precio:", 4, 0).grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.campo_precio = entrada(4, 1)
        self.campo_precio.grid(row=4, column=1, padx=5, pady=5)

        # Campo: Stock (entero opcional)
        etiqueta("Stock:", 5, 0).grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.campo_stock = entrada(5, 1)
        self.campo_stock.grid(row=5, column=1, padx=5, pady=5)

        # Botones principales: Añadir, Modificar, Eliminar (con comandos asociados)
        boton_add = tk.Button(
            frame_botones, text="Añadir Producto",
            bg="#b2d8b2", fg="#004d00", activebackground="#a3cfa3",
            command=self.añadir_producto # Llama a método para insertar en BD
        )
        boton_update = tk.Button(
            frame_botones, text="Modificar Producto",
            bg="#b2d8b2", fg="#004d00", activebackground="#a3cfa3",
            command=self.modificar_producto # Llama a método para actualizar en BD
        )
        boton_delete = tk.Button(
            frame_botones, text="Eliminar Producto",
            bg="#b2d8b2", fg="#004d00", activebackground="#a3cfa3",
            command=self.eliminar_producto # Llama a método para borrar en BD
        )

        # Coloca los botones en línea
        boton_add.pack(side=tk.LEFT, padx=8, pady=8)
        boton_update.pack(side=tk.LEFT, padx=8, pady=8)
        boton_delete.pack(side=tk.LEFT, padx=8, pady=8)

        # Lista para visualizar los productos
        etiqueta_lista = tk.Label(frame_lista, text="Lista de productos:", bg="#e6f2e6", fg="#2e8b57")
        etiqueta_lista.pack(anchor="w", padx=10)
        self.lista_productos = tk.Listbox(frame_lista, width=100, height=12, bg="#f0fff0", fg="#006400")
        self.lista_productos.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Vincula la selección en la lista a la carga de los campos del formulario
        self.lista_productos.bind('<<ListboxSelect>>', self.cargar_producto_seleccionado)

        # Carga inicial de datos desde la BD a la lista
        self.actualizar_lista()

    
    
    def actualizar_lista(self):
        self.lista_productos.delete(0, tk.END)  # Limpia la lista

        for fila in filas:
            id_p, nombre, fecha, categoria, marca, precio, stock = fila
            # Formatea cada producto en una línea amigable
            texto = f"{id_p}: {nombre} | {fecha or '-'} | {categoria or '-'} | {marca or '-'} | {precio or '-'} | stock: {stock if stock is not None else '-'}"
            self.lista_productos.insert(tk.END, texto)


    def limpiar_campos(self):
        """
        Limpia todos los campos del formulario y deselecciona la lista.
        """
        self.campo_nombre.delete(0, tk.END)
        self.campo_fecha.delete(0, tk.END)
        self.campo_categoria.delete(0, tk.END)
        self.campo_marca.delete(0, tk.END)
        self.campo_precio.delete(0, tk.END)
        self.campo_stock.delete(0, tk.END)
        self.lista_productos.selection_clear(0, tk.END)  # Quita la selección

    def añadir_producto(self):
        """
        Inserta un nuevo producto en la BD:
        
        """
        nombre = self.campo_nombre.get().strip()
        fecha = self.campo_fecha.get().strip()
        categoria = self.campo_categoria.get().strip()
        marca = self.campo_marca.get().strip()
        precio = self.campo_precio.get().strip()
        stock_text = self.campo_stock.get().strip()

        # Validación mínima
        if not nombre:
            messagebox.showwarning("Campo vacío", "El campo Nombre es obligatorio.")
            return

        # Conversión segura de stock a entero (o None si vacío)
        try:
            stock = int(stock_text) if stock_text != "" else None
        except ValueError:
            messagebox.showwarning("Valor incorrecto", "Stock debe ser un número entero.")
            return

        # Inserción en la tabla
        
    
        self.limpiar_campos()
        self.actualizar_lista()
        messagebox.showinfo("Éxito", "Producto añadido correctamente.")

    def get_id_seleccionado(self):
        """
        Obtiene el id del producto seleccionado en la Listbox.
        
        """
        try:
            seleccionado = self.lista_productos.get(self.lista_productos.curselection())
            id_producto = int(seleccionado.split(":")[0])  # Extrae todo antes de ':'
            return id_producto
        except (tk.TclError, IndexError, ValueError):
            return None

    def cargar_producto_seleccionado(self, event):
        """
        Cuando el usuario selecciona un elemento en la Listbox:
        
        """
        if not self.lista_productos.curselection():
            return
        id_p = self.get_id_seleccionado()
        if id_p:
            self.cursor.execute(
                "SELECT nombre, fecha_caducidad, categoria, marca, precio, stock FROM producto WHERE id = ?",
                (id_p,)
            )
            fila = self.cursor.fetchone()
            if fila:
                nombre, fecha, categoria, marca, precio, stock = fila
                # Rellena cada campo limpiándolo antes
                self.campo_nombre.delete(0, tk.END); self.campo_nombre.insert(0, nombre)
                self.campo_fecha.delete(0, tk.END); self.campo_fecha.insert(0, fecha or "")
                self.campo_categoria.delete(0, tk.END); self.campo_categoria.insert(0, categoria or "")
                self.campo_marca.delete(0, tk.END); self.campo_marca.insert(0, marca or "")
                self.campo_precio.delete(0, tk.END); self.campo_precio.insert(0, precio or "")
                self.campo_stock.delete(0, tk.END); self.campo_stock.insert(0, str(stock) if stock is not None else "")

    def modificar_producto(self):
        """
        Actualiza el producto seleccionado:
        
        """
        id_p = self.get_id_seleccionado()
        if not id_p:
            messagebox.showinfo("Sin selección", "Selecciona un producto para modificar.")
            return

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
            "UPDATE producto SET nombre = ?, fecha_caducidad = ?, categoria = ?, marca = ?, precio = ?, stock = ? WHERE id = ?",
            (nombre, fecha, categoria, marca, precio, stock, id_p)
        )
        self.conexion.commit()
        self.limpiar_campos()
        self.actualizar_lista()
        messagebox.showinfo("Éxito", "Producto modificado correctamente.")

    def eliminar_producto(self):
        """
        Elimina el producto seleccionado:
        
    
        """
        id_p = self.get_id_seleccionado()
        if not id_p:
            messagebox.showinfo("Sin selección", "Selecciona un producto para eliminar.")
            return

        seleccionado_text = self.lista_productos.get(self.lista_productos.curselection())
        if messagebox.askyesno("Confirmar borrado", f"¿Eliminar el producto?\n\n{seleccionado_text}"):
            self.cursor.execute("DELETE FROM producto WHERE id = ?", (id_p,))
            self.conexion.commit()
            self.limpiar_campos()
            self.actualizar_lista()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")

    def cerrar(self):
        """
        Cierra la conexión a la BD y la ventana con manejo básico de errores.
        """
        try:
            self.conexion.close()
        except:
            pass
        self.ventana.destroy()

if __name__ == "__main__":
    # Punto de entrada: crea la ventana raíz y la instancia de la app
    ventana_principal = tk.Tk()
    app = App(ventana_principal)

    # Intercepta el evento de cierre de la ventana para cerrar la BD correctamente
    ventana_principal.protocol("WM_DELETE_WINDOW", app.cerrar)

    # Inicia el bucle principal de Tkinter (event loop)
    ventana_principal.mainloop()