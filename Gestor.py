class Producto:
    """
    Representa un producto en nuestra lista de productos.
    """
    def __init__(self, nombre, fecha_caducidad, precio, categoria, marca, stock=True):
        """
        Constructor para crear un nuevo objeto Producto.
        """
        self.id = None
        self.nombre = nombre
        self.fecha_caducidad = fecha_caducidad
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        self.marca = marca

    def __str__(self):
        """
        Representación legible del objeto Producto.
        """
        return (f"Producto(ID: {self.id}, Nombre: {self.nombre}, Fecha caducidad: {self.fecha_caducidad}, "
                f"Precio: {self.precio}, Categoría: {self.categoria}, Marca: {self.marca}, Stock: {self.stock})")
# --- CÓDIGO DE PRUEBA ---

# 1. Creamos dos objetos (instancias) de la clase Producto
producto1 = Producto("yogurt", "2026-10-20", "2.99", "lacteos", "hacendado" )
producto2 = Producto("agua", "2029-10-18", "1,99", "bebidas", "bezoya" )

# 2. Usamos print() con f-strings para mostrar los datos del primer producto
print("--- DATOS DEL PRODUCTO 1 ---")
print(f"ID: {producto1.id}")
print(f"nombre: {producto1.nombre}")
print(f"Fecha caducidad: {producto1.fecha_caducidad}")
print(f"precio: {producto1.precio}")
print(f"categoria: {producto1.categoria}")
print(f"marca: {producto1.marca}")
print(f"stock: {producto1.stock}")

# 3. Hacemos lo mismo para el segundo producto
print("\n--- DATOS DEL PRODUCTO 2 ---") # '\\n' añade una línea en blanco para separar
print(f"ID: {producto2.id}")
print(f"nombre: {producto2.nombre}")
print(f"Fecha caducidad: {producto2.fecha_caducidad}")
print(f"precio: {producto2.precio}")
print(f"categoria: {producto2.categoria}")
print(f"marca: {producto2.marca}")
print(f"stock: {producto2.stock}")

print("--- DATOS DEL PRODUCTO 1 ---")
print(producto1)

print("\n--- DATOS DEL PRODUCTO 2 ---")
print(producto2)


