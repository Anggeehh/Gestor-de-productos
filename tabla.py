


import sqlite3 # Importamos la librería

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

