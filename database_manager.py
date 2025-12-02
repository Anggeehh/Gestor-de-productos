import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        # El constructor ahora solo se encarga de la BD
        self.conexion = sqlite3.connect(db_path)
        self.cursor = self.conexion.cursor()
        self.crear_tabla()
    
    def crear_tabla(self):
        """
        Crea la tabla 'producto' si no existe.
        
        """
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
        self.conexion.commit()  # Guarda la operación en el fichero de BD

    
    def actualizar_lista(self):
       
        self.cursor.execute(
            "SELECT id, nombre, fecha_caducidad, categoria, marca, precio, stock FROM producto ORDER BY id"
        )
        filas = self.cursor.fetchall()
        return filas

    def añadir_producto(self):
        
        self.cursor.execute(
            "INSERT INTO producto (nombre, fecha_caducidad, categoria, marca, precio, stock) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, fecha, categoria, marca, precio, stock)
        )
        self.conexion.commit()

    def modificar_producto(self):
        self.cursor.execute(
                    "UPDATE producto SET nombre = ?, fecha_caducidad = ?, categoria = ?, marca = ?, precio = ?, stock = ? WHERE id = ?",
                    (nombre, fecha, categoria, marca, precio, stock, id_p)
                )
        self.conexion.commit()        
    
    def eliminar_producto(self):
        self.cursor.execute("DELETE FROM producto WHERE id = ?", (id_p,))
        self.conexion.commit()
    
    def cargar_producto_seleccionado(self, event):
        self.cursor.execute(
            "SELECT nombre, fecha_caducidad, categoria, marca, precio, stock FROM producto WHERE id = ?",
            (id_p,)
        )
        fila = self.cursor.fetchone()
        return fila
   

    
