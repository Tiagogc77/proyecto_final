# Importar módulos necesarios
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from conexion_mysql import conectar
from ventana_3 import VentanaEdicion
from ventana_4 import eliminar_datos
import pandas as pd
import io
from sqlalchemy import create_engine
from ventana_1 import Ventana1

# Definir la clase para la ventana 2
class Ventana2:
    def __init__(self, root):
        # Inicializar la instancia y crear la ventana secundaria (Toplevel)
        self.root = root
        self.ventana2 = tk.Toplevel(self.root)
        self.ventana2.title("Ventana 2")
        self.ventana2.geometry("800x600")

        # Crear un Treeview para mostrar datos en forma de tabla
        self.lista_datos = ttk.Treeview(self.ventana2, columns=("ID", "Tipo", "Fuente", "Imagen"), show="headings")
        self.lista_datos.heading("ID", text="ID")
        self.lista_datos.heading("Tipo", text="Tipo")
        self.lista_datos.heading("Fuente", text="Fuente")
        self.lista_datos.heading("Imagen", text="Imagen")
        self.lista_datos.column("ID", width=50)
        self.lista_datos.column("Tipo", width=100)
        self.lista_datos.column("Fuente", width=100)
        self.lista_datos.column("Imagen", width=100)

        # Diccionario para almacenar miniaturas de imágenes
        self.imagenes_miniatura = {}
        # Cargar datos en la tabla
        self.cargar_datos()

        self.lista_datos.pack(pady=20)

        # Botón para editar el elemento seleccionado
        self.btn_editar_externo = tk.Button(self.ventana2, text="Editar Seleccionado", command=self.editar_seleccionado)
        self.btn_editar_externo.pack(pady=10)
        # Botón para eliminar el elemento seleccionado
        btn_eliminar = tk.Button(self.ventana2, text="Eliminar Dato Seleccionado", command=self.eliminar_seleccionado)
        btn_eliminar.pack(pady=10)

        # Botón para abrir la Ventana1
        btn_agregar = tk.Button(self.ventana2, text="Agregar Nuevo", command=self.abrir_ventana1)
        btn_agregar.pack(pady=10)

    # Método para cargar datos desde la base de datos y mostrarlos en la tabla
    def cargar_datos(self):
        conexion = conectar()

        if conexion:
            try:
                # Cargar datos de la tabla datos_covid
                consulta = "SELECT id, tipo, fuente, imagen FROM datos_covid"
                # Crear un objeto engine para interactuar con la base de datos usando SQLAlchemy
                engine = create_engine('mysql+mysqlconnector://root:4568@localhost/Covid_19', echo=True)

                df = pd.read_sql_query(consulta, engine)

                # Mostrar datos en la lista
                for index, fila in df.iterrows():
                    id_dato = fila['id']
                    tipo = fila['tipo']
                    fuente = fila['fuente']

                    imagen_blob = fila['imagen']
                    imagen_pil = Image.open(io.BytesIO(imagen_blob))
                    imagen_miniatura_pil = imagen_pil.resize((100, 100), Image.LANCZOS)
                    imagen_miniatura_tk = ImageTk.PhotoImage(imagen_miniatura_pil)

                    self.lista_datos.insert("", "end", values=(id_dato, tipo, fuente, ""), iid=id_dato)
                    self.imagenes_miniatura[id_dato] = imagen_miniatura_tk
                    self.lista_datos.item(id_dato, tags=(id_dato,))
                    self.lista_datos.tag_configure(id_dato, image=imagen_miniatura_tk)

            except Exception as e:
                print(f"Error al cargar datos: {e}")
            finally:
                conexion.close()

    # Método para editar el elemento seleccionado
    def editar_seleccionado(self):
        seleccion = self.lista_datos.selection()

        if seleccion:
            id_seleccionado = seleccion[0]
            tipo = self.lista_datos.item(id_seleccionado, 'values')[1]
            fuente = self.lista_datos.item(id_seleccionado, 'values')[2]
            imagen_original = self.imagenes_miniatura.get(id_seleccionado)

            # Llamar a la clase VentanaEdicion para editar el elemento seleccionado
            VentanaEdicion(self.ventana2, id_seleccionado, tipo, fuente, imagen_original)

    # Método para eliminar el elemento seleccionado
    def eliminar_seleccionado(self):
        seleccion = self.lista_datos.selection()

        if seleccion:
            id_seleccionado = seleccion[0]
            confirmar = messagebox.askyesno("Confirmar Eliminación",
                                            "¿Estás seguro de que deseas eliminar el dato seleccionado?")
            if confirmar:
                # Llamar a la función eliminar_datos para eliminar el elemento seleccionado
                eliminar_datos(id_seleccionado, self)
                messagebox.showinfo("Eliminación Exitosa", "El dato ha sido eliminado correctamente.")
                self.recargar_tabla()  # Llamar a la función para recargar la tabla

    # Método para abrir la Ventana1
    def abrir_ventana1(self):
        Ventana1(self.root)

    # Método para recargar la tabla con datos actualizados
    def recargar_tabla(self):
        # Limpiar la tabla
        for item in self.lista_datos.get_children():
            self.lista_datos.delete(item)

        # Volver a cargar los datos
        self.cargar_datos()

# Bloque principal para ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = Ventana2(root)
    root.mainloop()
