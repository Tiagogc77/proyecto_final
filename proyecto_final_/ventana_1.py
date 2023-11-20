# Importar módulos necesarios
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from conexion_mysql import conectar
import io
from sqlalchemy import create_engine

# Definir la clase para la Ventana1
class Ventana1:
    def __init__(self, root):
        # Inicializar la instancia y crear la ventana secundaria (Toplevel)
        self.root = root
        self.ventana1 = tk.Toplevel(self.root)
        self.ventana1.title("Ventana 1")

        # Configurar el Canvas como contenedor principal
        self.canvas = tk.Canvas(self.ventana1)
        self.canvas.pack(fill="both", expand=True)

        # Configurar barras de desplazamiento
        scrollbar_vertical = tk.Scrollbar(self.ventana1, command=self.canvas.yview)
        scrollbar_vertical.pack(side="right", fill="y")

        scrollbar_horizontal = tk.Scrollbar(self.ventana1, orient=tk.HORIZONTAL, command=self.canvas.xview)
        scrollbar_horizontal.pack(side="bottom", fill="x")

        self.canvas.config(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

        # Frame interno para contener los widgets
        self.frame_contenedor = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_contenedor, anchor="nw")

        # Llamar al método para inicializar la interfaz
        self.inicializar_interfaz()

    # Método para inicializar la interfaz gráfica
    def inicializar_interfaz(self):
        # Inicializar variables de control y de almacenamiento de la ruta de la imagen
        self.tipo_var = tk.StringVar(self.frame_contenedor)
        self.fuente_var = tk.StringVar(self.frame_contenedor)
        self.ruta_imagen = None  # Variable para almacenar la ruta de la imagen

        # Opciones para los menús desplegables
        tipos = ['COVID', 'Normal', 'Opacidad', 'Viral Pneumonia']
        fuentes = ['PadChest', 'GitHub', 'Kaggle', 'SIRM', 'RSNA', 'Chest X-Ray Images']

        # Crear widgets y botones
        lbl_tipo = tk.Label(self.frame_contenedor, text="Tipo:")
        menu_tipo = tk.OptionMenu(self.frame_contenedor, self.tipo_var, *tipos)
        lbl_fuente = tk.Label(self.frame_contenedor, text="Fuente:")
        menu_fuente = tk.OptionMenu(self.frame_contenedor, self.fuente_var, *fuentes)

        self.lbl_imagen = tk.Label(self.frame_contenedor)  # Widget Label para mostrar la imagen
        btn_cargar_imagen = tk.Button(self.frame_contenedor, text="Cargar Imagen", command=self.cargar_imagen)
        btn_guardar = tk.Button(self.frame_contenedor, text="Guardar en DB", command=self.guardar_en_db)
        btn_volver = tk.Button(self.frame_contenedor, text="Volver al Menú Principal", command=self.volver_al_menu_principal)

        # Colocar widgets en la cuadrícula
        lbl_tipo.grid(row=0, column=0, pady=10)
        menu_tipo.grid(row=0, column=1, pady=10)
        lbl_fuente.grid(row=1, column=0, pady=10)
        menu_fuente.grid(row=1, column=1, pady=10)
        btn_cargar_imagen.grid(row=0, column=2, rowspan=2, padx=20)
        self.lbl_imagen.grid(row=2, column=0, columnspan=3, pady=10)  # Agregado el widget Label para mostrar la imagen
        btn_guardar.grid(row=3, column=0, columnspan=2, pady=10)
        btn_volver.grid(row=3, column=2, columnspan=2, pady=10)

    # Método para verificar el tamaño de la imagen
    def verificar_tamano_imagen(self, ruta_imagen, ancho_esperado, alto_esperado):
        try:
            imagen = Image.open(ruta_imagen)
            ancho, alto = imagen.size
            return ancho == ancho_esperado and alto == alto_esperado
        except Exception as e:
            print(f"Error al verificar el tamaño de la imagen: {e}")
            return False

    # Método para mostrar la imagen en el widget Label
    def mostrar_imagen(self, ruta_imagen):
        # Mostrar la imagen en un tamaño de 100x100
        imagen_original_pil = Image.open(ruta_imagen)
        imagen_miniatura_pil = imagen_original_pil.resize((100, 100), Image.LANCZOS)
        imagen_original_tk = ImageTk.PhotoImage(imagen_miniatura_pil)

        # Configurar la imagen en el widget Label
        self.lbl_imagen.configure(image=imagen_original_tk)
        self.lbl_imagen.image = imagen_original_tk  # Evitar que la imagen sea recolectada por el recolector de basura

    # Método para cargar una nueva imagen desde el sistema de archivos
    def cargar_imagen(self):
        if self.ruta_imagen:
            print(f"Ya se ha cargado una imagen: {self.ruta_imagen}")
        else:
            ruta_imagen = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
            if ruta_imagen:
                # Verificar el tamaño de la imagen
                if self.verificar_tamano_imagen(ruta_imagen, 299, 299):
                    print(f"Imagen seleccionada: {ruta_imagen}")
                    self.ruta_imagen = ruta_imagen  # Almacenar la ruta de la imagen
                    # Continuar con el procesamiento de la imagen (mostrar o guardar)
                    self.mostrar_imagen(ruta_imagen)
                else:
                    messagebox.showwarning("Tamaño incorrecto", "La imagen debe ser de tamaño 299x299 píxeles.")

    # Método para guardar la imagen en la base de datos
    def guardar_en_db(self):
        tipo = self.tipo_var.get()
        fuente = self.fuente_var.get()

        if self.ruta_imagen:
            # Verificar el tamaño de la imagen
            if self.verificar_tamano_imagen(self.ruta_imagen, 299, 299):
                print(f"Imagen seleccionada para guardar en la base de datos: {self.ruta_imagen}")
                # Continuar con el procesamiento de la imagen (guardar en la base de datos)
                self.guardar_imagen_en_db(tipo, fuente, self.ruta_imagen)
                messagebox.showinfo("Guardado Exitoso", "La imagen ha sido guardada en la base de datos con éxito.")
            else:
                messagebox.showwarning("Tamaño incorrecto", "La imagen debe ser de tamaño 299x299 píxeles.")
        else:
            messagebox.showwarning("Imagen no cargada", "Primero debes cargar una imagen.")

    # Método para guardar la imagen en la base de datos
    def guardar_imagen_en_db(self, tipo, fuente, ruta_imagen):
        try:
            conexion = conectar()

            if conexion:
                try:
                    cursor = conexion.cursor()

                    # Asumiendo que tienes una tabla llamada datos_covid con columnas tipo, fuente, imagen
                    consulta = "INSERT INTO datos_covid (tipo, fuente, imagen) VALUES (%s, %s, %s)"

                    # Convertir la imagen a bytes y guardarla en la base de datos
                    with open(ruta_imagen, 'rb') as file:
                        imagen_bytes = file.read()

                    # Aquí puedes imprimir la longitud de los datos de imagen antes de guardar
                    print(f"Tamaño de datos de imagen: {len(imagen_bytes)} bytes")

                    # Ejecutar la consulta con los datos
                    datos = (tipo, fuente, imagen_bytes)
                    cursor.execute(consulta, datos)
                    conexion.commit()
                    print("Datos guardados en la base de datos")
                except Exception as err:
                    print(f"Error al guardar en la base de datos: {err}")
                finally:
                    cursor.close()
                    conexion.close()
        except Exception as e:
            print(f"Error al establecer conexión con la base de datos: {e}")

    # Método para volver al menú principal
    def volver_al_menu_principal(self):
        self.ventana1.withdraw()
        self.root.update()
        self.root.deiconify()

# Bloque principal para ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = Ventana1(root)
    root.mainloop()
