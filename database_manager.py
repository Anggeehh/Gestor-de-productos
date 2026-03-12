import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.conexion = sqlite3.connect(db_path)
        self.cursor = self.conexion.cursor()
        self.crear_tabla()
    
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

    def actualizar_lista(self):
        self.cursor.execute(
            "SELECT id, nombre, fecha_caducidad, categoria, marca, precio, stock FROM producto ORDER BY id"
        )
        return self.cursor.fetchall()

    def buscar_producto(self, termino):
        """Busca productos que coincidan con el término usando LIKE de SQL."""
        query = "SELECT id, nombre, fecha_caducidad, categoria, marca, precio, stock FROM producto WHERE nombre LIKE ?"
        self.cursor.execute(query, ('%' + termino + '%',))
        return self.cursor.fetchall()

    def añadir_producto(self, nombre, fecha, categoria, marca, precio, stock):
        self.cursor.execute(
            "INSERT INTO producto (nombre, fecha_caducidad, categoria, marca, precio, stock) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, fecha, categoria, marca, precio, stock)
        )
        self.conexion.commit()

    def modificar_producto(self, nombre, fecha, categoria, marca, precio, stock, id_p):
        self.cursor.execute(
            "UPDATE producto SET nombre = ?, fecha_caducidad = ?, categoria = ?, marca = ?, precio = ?, stock = ? WHERE id = ?",
            (nombre, fecha, categoria, marca, precio, stock, id_p)
        )
        self.conexion.commit()

    def eliminar_producto(self, id_p):
        self.cursor.execute("DELETE FROM producto WHERE id = ?", (id_p,))
        self.conexion.commit()

    def cargar_producto_seleccionado(self, id_p):
        self.cursor.execute(
            "SELECT nombre, fecha_caducidad, categoria, marca, precio, stock FROM producto WHERE id = ?",
            (id_p,)
        )
        return self.cursor.fetchone()
        
    def producto_existe(self, nombre):
        """Comprueba si un producto ya existe por su nombre (para importación inteligente)."""
        self.cursor.execute("SELECT id FROM producto WHERE nombre = ?", (nombre,))
        return self.cursor.fetchone() is not None

    def cerrar(self):
        """Hace un commit final y cierra la conexión (Mejora 4)."""
        self.conexion.commit()
        self.conexion.close()