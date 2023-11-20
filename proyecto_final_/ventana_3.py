# Importar módulos necesarios
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from conexion_mysql import conectar  # Suponiendo que hay un módulo de conexión llamado conexion_mysql
import io
import tempfile

# Definir la clase para la ventana de edición
class VentanaEdicion:
    def __init__(self, root, id_dato, tipo, fuente, imagen_original_db):
        # Inicializar variables de la instancia
        self.root = root
        self.id_dato = id_dato
        self.tipo_var = tk.StringVar(self.root, value=tipo)
        self.fuente_var = tk.StringVar(self.root, value=fuente)
        self.nueva_ruta_imagen = None  # Variable para almacenar la nueva ruta de la imagen
        self.imagen_original_db = imagen_original_db  # Datos de la imagen almacenada en la base de datos

        # Definir opciones para el menú desplegable
        tipos = ['COVID', 'Normal', 'Opacidad', 'Viral Pneumonia']
        fuentes = ['PadChest', 'GitHub', 'Kaggle', 'SIRM', 'RSNA', 'Chest X-Ray Images']

        # Crear la ventana de edición
        self.ventana_edicion = tk.Toplevel(self.root)
        self.ventana_edicion.title("Ventana de Edición")
        self.ventana_edicion.geometry("500x400")

        # Crear etiquetas, menús desplegables, lienzo y botones
        lbl_tipo = tk.Label(self.ventana_edicion, text="Tipo:")
        menu_tipo = tk.OptionMenu(self.ventana_edicion, self.tipo_var, *tipos)

        lbl_fuente = tk.Label(self.ventana_edicion, text="Fuente:")
        menu_fuente = tk.OptionMenu(self.ventana_edicion, self.fuente_var, *fuentes)

        self.lbl_imagen = tk.Label(self.ventana_edicion, text="Imagen:")
        self.canvas_imagen = tk.Canvas(self.ventana_edicion, width=40, height=40)

        # Convertir y mostrar la imagen original almacenada en la base de datos
        self.mostrar_imagen_desde_bytes(self.imagen_original_db)

        btn_seleccionar_imagen = tk.Button(self.ventana_edicion, text="Seleccionar Nueva Imagen",
                                           command=self.seleccionar_nueva_imagen)
        btn_guardar_cambios = tk.Button(self.ventana_edicion, text="Guardar Cambios", command=self.guardar_cambios)
        btn_cancelar = tk.Button(self.ventana_edicion, text="Cancelar", command=self.ventana_edicion.destroy)

        # Organizar widgets en la ventana
        lbl_tipo.pack(pady=10)
        menu_tipo.pack(pady=10)
        lbl_fuente.pack(pady=10)
        menu_fuente.pack(pady=10)
        self.lbl_imagen.pack(pady=10)
        self.canvas_imagen.pack(pady=10)
        btn_seleccionar_imagen.pack(pady=10)
        btn_guardar_cambios.pack(pady=10)
        btn_cancelar.pack(pady=10)

    # Función para manejar la selección de una nueva imagen
    def seleccionar_nueva_imagen(self):
        self.nueva_ruta_imagen = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
        if self.nueva_ruta_imagen:
            # Verificar el tamaño de la nueva imagen
            if not self.verificar_tamano_imagen(self.nueva_ruta_imagen, 299, 299):
                messagebox.showwarning("Tamaño incorrecto", "La imagen debe ser de tamaño 299x299 píxeles.")
            else:
                # Actualizar el Canvas con la nueva imagen
                self.mostrar_imagen_en_canvas(self.nueva_ruta_imagen)

    # Función para mostrar una imagen en el lienzo
    def mostrar_imagen_en_canvas(self, ruta_imagen):
        imagen = Image.open(ruta_imagen)
        imagen_resized = imagen.resize((40, 40), Image.NEAREST)  # Sin antialiasing
        imagen_tk = ImageTk.PhotoImage(imagen_resized)
        self.canvas_imagen.delete("all")  # Limpiar el Canvas
        self.canvas_imagen.create_image(0, 0, anchor=tk.NW, image=imagen_tk)
        self.canvas_imagen.image = imagen_tk  # Mantener una referencia para evitar que se elimine la imagen

    # Función para verificar el tamaño de una imagen
    def verificar_tamano_imagen(self, ruta_imagen, ancho_esperado, alto_esperado):
        try:
            imagen = Image.open(ruta_imagen)
            ancho, alto = imagen.size
            return ancho == ancho_esperado and alto == alto_esperado
        except Exception as e:
            print(f"Error al verificar el tamaño de la imagen: {e}")
            return False

    # Función para mostrar una imagen desde bytes en el lienzo
    def mostrar_imagen_desde_bytes(self, imagen_bytes):
        try:
            if imagen_bytes is not None:
                # Crear un archivo temporal para guardar los bytes
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(imagen_bytes)
                    temp_file_path = temp_file.name

                # Mostrar la imagen desde el archivo temporal
                self.mostrar_imagen_en_canvas(temp_file_path)
        except Exception as e:
            print(f"Error al mostrar la imagen desde bytes: {e}")

    # Función para guardar los cambios en la base de datos
    def guardar_cambios(self):
        tipo = self.tipo_var.get()
        fuente = self.fuente_var.get()

        if tipo or fuente or self.nueva_ruta_imagen:
            # Verificar el tamaño de la imagen
            if self.nueva_ruta_imagen and not self.verificar_tamano_imagen(self.nueva_ruta_imagen, 299, 299):
                messagebox.showwarning("Tamaño incorrecto", "La imagen debe ser de tamaño 299x299 píxeles.")
                return

            try:
                conexion = conectar()

                if conexion:
                    try:
                        cursor = conexion.cursor()
                        # Asumiendo que tienes una tabla llamada datos_covid con columnas tipo, fuente, imagen
                        consulta = "UPDATE datos_covid SET "
                        valores = []

                        if tipo:
                            consulta += "tipo=%s, "
                            valores.append(tipo)
                        if fuente:
                            consulta += "fuente=%s, "
                            valores.append(fuente)
                        if self.nueva_ruta_imagen:
                            # Convertir la nueva imagen a bytes y actualizar la consulta
                            with open(self.nueva_ruta_imagen, 'rb') as file:
                                nueva_imagen_bytes = file.read()
                            consulta += "imagen=%s, "
                            valores.append(nueva_imagen_bytes)

                        consulta = consulta.rstrip(', ') + " WHERE id=%s"
                        valores.append(self.id_dato)

                        cursor.execute(consulta, tuple(valores))
                        conexion.commit()
                        print("Datos actualizados en la base de datos")
                        self.ventana_edicion.destroy()  # Cerrar la ventana de edición después de guardar
                        self.ventana_padre.recargar_tabla()  # Llamar a la función para recargar la tabla
                    except Exception as err:
                        print(f"Error al actualizar en la base de datos: {err}")
                    finally:
                        cursor.close()
                        conexion.close()
            except Exception as e:
                print(f"Error al establecer conexión con la base de datos: {e}")
        else:
            messagebox.showwarning("Sin cambios", "No se realizaron cambios para guardar.")


# Bloque principal para ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    # Crear instancia de la clase VentanaEdicion y ejecutar el bucle principal de tkinter
    app = VentanaEdicion(root, id_dato=1, tipo="COVID", fuente="GitHub", imagen_original_db=b'')  # Reemplazar valores según sea necesario
    root.mainloop()
