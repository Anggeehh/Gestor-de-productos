import tkinter as tk

# 1. Ventana principal
ventana = tk.Tk()
ventana.title("Gestor de productos")
ventana.geometry("820x450")  # Ancho x Alto
ventana.configure(bg="#e6f2e6")  # Fondo general verde claro

# --- Frame para el formulario ---
frame_formulario = tk.Frame(ventana, bg="#e6f2e6")
frame_formulario.pack(padx=10, pady=10)

def crear_label(texto, fila):
    etiqueta = tk.Label(frame_formulario, text=texto, bg="#e6f2e6", fg="#2e8b57")
    etiqueta.grid(row=fila, column=0, sticky="e")
    campo = tk.Entry(frame_formulario, bg="#f0fff0", fg="#006400")
    campo.grid(row=fila, column=1)
    return campo

campo_nombre = crear_label("Nombre:", 0)
campo_fecha = crear_label("Fecha Caducidad (AAAA-MM-DD):", 1)
campo_cat = crear_label("Categoría:", 2)
campo_marca = crear_label("Marca:", 3)
campo_prec = crear_label("Precio:", 4)
campo_stock = crear_label("Stock:", 5)

# --- Frame para los botones ---
frame_botones = tk.Frame(ventana, bg="#e6f2e6")
frame_botones.pack(pady=10)

#---botones---
boton_add = tk.Button(frame_botones, text="Añadir Tarea" , bg="#b2d8b2", fg="#004d00", activebackground="#a3cfa3")
boton_update = tk.Button(frame_botones, text="Modificar Tarea" , bg="#b2d8b2", fg="#004d00", activebackground="#a3cfa3")
boton_delete = tk.Button(frame_botones, text="Eliminar Tarea" , bg="#b2d8b2", fg="#004d00", activebackground="#a3cfa3")

boton_add.grid(row=6, column=1, padx=10, pady=10)
boton_update.grid(row=6, column=2, padx=10, pady=10)
boton_delete.grid(row=6, column=3, padx=10, pady=10)


# --- Lista de productos ---
etiqueta_lista = tk.Label(ventana, text="Lista de productos:", bg="#e6f2e6", fg="#2e8b57")
etiqueta_lista.pack()
lista_tareas = tk.Listbox(ventana, width=60, height=10, bg="#f0fff0", fg="#006400")
lista_tareas.pack(padx=10, pady=5)

<<<<<<< HEAD
ventana.mainloop()
=======

ventana.mainloop()








>>>>>>> 051596f7049954c4b5a03efae1d25f1a73702522
