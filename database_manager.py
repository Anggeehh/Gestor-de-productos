import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        # Conexión a la base de datos
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
        self.conexion.commit()

    def actualizar_lista(self):
        """
        Devuelve todas las filas de la tabla producto.
        """
        self.cursor.execute(
            "SELECT id, nombre, fecha_caducidad, categoria, marca, precio, stock FROM producto ORDER BY id"
        )
        filas = self.cursor.fetchall()
        return filas

    def añadir_producto(self, nombre, fecha, categoria, marca, precio, stock):
        """
        Inserta un nuevo producto en la tabla.
        """
        self.cursor.execute(
            "INSERT INTO producto (nombre, fecha_caducidad, categoria, marca, precio, stock) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, fecha, categoria, marca, precio, stock)
        )
        self.conexion.commit()

    def modificar_producto(self, nombre, fecha, categoria, marca, precio, stock, id_p):
        """
        Actualiza un producto existente.
        """
        self.cursor.execute(
            "UPDATE producto SET nombre = ?, fecha_caducidad = ?, categoria = ?, marca = ?, precio = ?, stock = ? WHERE id = ?",
            (nombre, fecha, categoria, marca, precio, stock, id_p)
        )
        self.conexion.commit()

    def eliminar_producto(self, id_p):
        """
        Elimina un producto por su id.
        """
        self.cursor.execute("DELETE FROM producto WHERE id = ?", (id_p,))
        self.conexion.commit()

    def cargar_producto_seleccionado(self, id_p):
        """
        Devuelve los datos de un producto por su id.
        """
        self.cursor.execute(
            "SELECT nombre, fecha_caducidad, categoria, marca, precio, stock FROM producto WHERE id = ?",
            (id_p,)   # la coma es obligatoria para que sea tupla
        )
        fila = self.cursor.fetchone()
        return fila

    def cerrar(self):
        """
        Cierra la conexión con la base de datos.
        """
        self.conexion.close()