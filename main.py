import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database_manager import DatabaseManager
from datetime import datetime
import json

class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestor de Productos")
        self.ventana.geometry("850x550")
        self.ventana.configure(bg="#e6f2e6")

        # MEJORA 3: Temas visuales (ttk.Style)
        style = ttk.Style()
        style.theme_use('clam') # Puedes probar 'alt', 'default' o 'clam'
        
        self.db = DatabaseManager('productos.db')

        self.crear_menu()

        # Frames
        frame_formulario = tk.Frame(self.ventana, bg="#e6f2e6", pady=10)
        frame_botones = tk.Frame(self.ventana, bg="#e6f2e6")
        frame_busqueda = tk.Frame(self.ventana, bg="#e6f2e6", pady=5)
        frame_lista = tk.Frame(self.ventana, bg="#e6f2e6", pady=10)

        frame_formulario.pack()
        frame_botones.pack()
        frame_busqueda.pack(fill=tk.X, padx=20)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        # --- FORMULARIO ---
        etiqueta = lambda txt, r, c: tk.Label(frame_formulario, text=txt, bg="#e6f2e6", fg="#2e8b57")
        entrada = lambda r, c, width=40: ttk.Entry(frame_formulario, width=width)

        etiqueta("Nombre:", 0, 0).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.campo_nombre = entrada(0, 1)
        self.campo_nombre.grid(row=0, column=1, padx=5, pady=5)

        etiqueta("Fecha Caducidad (AAAA-MM-DD):", 1, 0).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.campo_fecha = entrada(1, 1)
        self.campo_fecha.grid(row=1, column=1, padx=5, pady=5)

        # RETO BÁSICO: Sustituir campo de texto por ttk.Combobox (ReadOnly)
        etiqueta("Categoría:", 2, 0).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.campo_categoria = ttk.Combobox(frame_formulario, width=37, state="readonly", 
                                            values=["Lácteos", "Bebidas", "Fruta", "Limpieza", "Otros"])
        self.campo_categoria.grid(row=2, column=1, padx=5, pady=5)

        etiqueta("Marca:", 3, 0).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.campo_marca = entrada(3, 1)
        self.campo_marca.grid(row=3, column=1, padx=5, pady=5)

        etiqueta("Precio:", 4, 0).grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.campo_precio = entrada(4, 1)
        self.campo_precio.grid(row=4, column=1, padx=5, pady=5)

        etiqueta("Stock:", 5, 0).grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.campo_stock = entrada(5, 1)
        self.campo_stock.grid(row=5, column=1, padx=5, pady=5)

        # --- BOTONES PRINCIPALES ---
        ttk.Button(frame_botones, text="Añadir Producto", command=self.añadir_producto).pack(side=tk.LEFT, padx=8, pady=8)
        ttk.Button(frame_botones, text="Modificar Producto", command=self.modificar_producto).pack(side=tk.LEFT, padx=8, pady=8)
        ttk.Button(frame_botones, text="Eliminar Producto", command=self.eliminar_producto).pack(side=tk.LEFT, padx=8, pady=8)

        # --- BÚSQUEDA ---
        tk.Label(frame_busqueda, text="Buscar:", bg="#e6f2e6", fg="#2e8b57").pack(side=tk.LEFT)
        self.campo_buscar = ttk.Entry(frame_busqueda, width=30)
        self.campo_buscar.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_busqueda, text="Buscar", command=self.buscar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_busqueda, text="Limpiar", command=self.limpiar_busqueda).pack(side=tk.LEFT, padx=5)

        # --- LISTA ---
        self.lista_productos = tk.Listbox(frame_lista, width=100, height=10, bg="#f0fff0", fg="#006400")
        self.lista_productos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.lista_productos.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_productos.config(yscrollcommand=scrollbar.set)
        
        self.lista_productos.bind('<<ListboxSelect>>', self.cargar_producto_seleccionado)
        self.actualizar_lista()

    def crear_menu(self):
        """Crea la barra de menú superior."""
        barra_menu = tk.Menu(self.ventana)
        self.ventana.config(menu=barra_menu)

        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Importar JSON...", command=self.importar_json)
        menu_archivo.add_command(label="Exportar JSON...", command=self.exportar_json)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.cerrar)
        
        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        menu_ayuda.add_command(label="Acerca de...", command=self.mostrar_acerca_de)

        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

    def mostrar_acerca_de(self):
        """Ventana emergente Acerca de (Toplevel)."""
        ventana_acerca = tk.Toplevel(self.ventana)
        ventana_acerca.title("Acerca de")
        ventana_acerca.geometry("300x150")
        ventana_acerca.configure(bg="#e6f2e6")
        tk.Label(ventana_acerca, text="Gestor de Productos v2.0\n\nDesarrollado para la Fase 5.\nIncluye mejoras avanzadas.", 
                 bg="#e6f2e6", pady=20).pack()
        ttk.Button(ventana_acerca, text="Cerrar", command=ventana_acerca.destroy).pack()

    def validar_fecha(self, fecha_str):
        """Valida que la fecha tenga el formato AAAA-MM-DD."""
        if not fecha_str: # Permitimos fecha vacía (opcional)
            return True
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def actualizar_lista(self, filas=None):
        self.lista_productos.delete(0, tk.END)
        if filas is None:
            filas = self.db.actualizar_lista()
        for fila in filas:
            id_p, nombre, fecha, categoria, marca, precio, stock = fila
            texto = f"{id_p}: {nombre} | {fecha or '-'} | {categoria or '-'} | {marca or '-'} | {precio or '-'} | stock: {stock if stock is not None else '-'}"
            self.lista_productos.insert(tk.END, texto)

    def limpiar_campos(self):
        self.campo_nombre.delete(0, tk.END)
        self.campo_fecha.delete(0, tk.END)
        self.campo_categoria.set('')
        self.campo_marca.delete(0, tk.END)
        self.campo_precio.delete(0, tk.END)
        self.campo_stock.delete(0, tk.END)
        self.lista_productos.selection_clear(0, tk.END)

    def obtener_datos_formulario(self):
        nombre = self.campo_nombre.get().strip()
        fecha = self.campo_fecha.get().strip()
        categoria = self.campo_categoria.get()
        marca = self.campo_marca.get().strip()
        precio = self.campo_precio.get().strip()
        stock_text = self.campo_stock.get().strip()
        return nombre, fecha, categoria, marca, precio, stock_text

    def añadir_producto(self):
        nombre, fecha, categoria, marca, precio, stock_text = self.obtener_datos_formulario()

        if not nombre:
            messagebox.showwarning("Aviso", "El campo Nombre es obligatorio.")
            return

        if not self.validar_fecha(fecha):
            messagebox.showerror("Error", "La fecha debe tener el formato AAAA-MM-DD.")
            return

        try:
            stock = int(stock_text) if stock_text else None
        except ValueError:
            messagebox.showwarning("Aviso", "El Stock debe ser un número entero.")
            return

        self.db.añadir_producto(nombre, fecha, categoria, marca, precio, stock)
        self.limpiar_campos()
        self.actualizar_lista()
        messagebox.showinfo("Éxito", "Producto añadido.")

    def modificar_producto(self):
        id_p = self.get_id_seleccionado()
        if not id_p:
            messagebox.showinfo("Aviso", "Selecciona un producto para modificar.")
            return

        nombre, fecha, categoria, marca, precio, stock_text = self.obtener_datos_formulario()

        if not nombre:
            messagebox.showwarning("Aviso", "El campo Nombre es obligatorio.")
            return

        if not self.validar_fecha(fecha):
            messagebox.showerror("Error", "La fecha debe tener el formato AAAA-MM-DD.")
            return

        try:
            stock = int(stock_text) if stock_text else None
        except ValueError:
            messagebox.showwarning("Aviso", "El Stock debe ser un número entero.")
            return

        self.db.modificar_producto(nombre, fecha, categoria, marca, precio, stock, id_p)
        self.limpiar_campos()
        self.actualizar_lista()
        messagebox.showinfo("Éxito", "Producto modificado.")

    def eliminar_producto(self):
        id_p = self.get_id_seleccionado()
        if not id_p:
            messagebox.showinfo("Aviso", "Selecciona un producto para eliminar.")
            return

        seleccionado_text = self.lista_productos.get(self.lista_productos.curselection())
        if messagebox.askyesno("Confirmar", f"¿Eliminar el producto?\n\n{seleccionado_text}"):
            self.db.eliminar_producto(id_p)
            self.limpiar_campos()
            self.actualizar_lista()
            messagebox.showinfo("Éxito", "Producto eliminado.")

    def buscar_producto(self):
        termino = self.campo_buscar.get().strip()
        if termino:
            resultados = self.db.buscar_producto(termino)
            self.actualizar_lista(resultados)

    def limpiar_busqueda(self):
        self.campo_buscar.delete(0, tk.END)
        self.actualizar_lista()

    def get_id_seleccionado(self):
        try:
            seleccionado = self.lista_productos.get(self.lista_productos.curselection())
            return int(seleccionado.split(":")[0])
        except (tk.TclError, IndexError, ValueError):
            return None

    def cargar_producto_seleccionado(self, event):
        if not self.lista_productos.curselection():
            return
        id_p = self.get_id_seleccionado()
        if id_p:
            producto = self.db.cargar_producto_seleccionado(id_p)
            if producto:
                nombre, fecha, categoria, marca, precio, stock = producto
                self.limpiar_campos()
                self.campo_nombre.insert(0, nombre)
                self.campo_fecha.insert(0, fecha or "")
                self.campo_categoria.set(categoria or "")
                self.campo_marca.insert(0, marca or "")
                self.campo_precio.insert(0, precio or "")
                self.campo_stock.insert(0, str(stock) if stock is not None else "")

    def exportar_json(self):
        """MEJORA 1: Exportar con filedialog"""
        ruta = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            title="Guardar copia de seguridad"
        )
        if ruta:
            filas = self.db.actualizar_lista()
            datos = [{"id": f[0], "nombre": f[1], "fecha": f[2], "categoria": f[3], 
                      "marca": f[4], "precio": f[5], "stock": f[6]} for f in filas]
            try:
                with open(ruta, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=4)
                messagebox.showinfo("Éxito", "Datos exportados correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def importar_json(self):
        """MEJORA 1 y 2: Importar con filedialog y de forma 'Inteligente'"""
        ruta = filedialog.askopenfilename(
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            title="Abrir copia de seguridad"
        )
        if ruta:
            try:
                with open(ruta, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                
                importados = 0
                omitidos = 0
                for item in datos:
                    # Importación Inteligente: Comprueba si existe el nombre
                    if not self.db.producto_existe(item['nombre']):
                        self.db.añadir_producto(item['nombre'], item.get('fecha'), item.get('categoria'), 
                                                item.get('marca'), item.get('precio'), item.get('stock'))
                        importados += 1
                    else:
                        omitidos += 1
                
                self.actualizar_lista()
                messagebox.showinfo("Importación Completada", 
                                    f"Nuevos productos: {importados}\nOmitidos (ya existían): {omitidos}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

    def cerrar(self):
        try:
            self.db.cerrar() # MEJORA 4: Cierre seguro de BD
        except:
            pass
        self.ventana.destroy()

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = App(ventana_principal)
    ventana_principal.protocol("WM_DELETE_WINDOW", app.cerrar)
    ventana_principal.mainloop()