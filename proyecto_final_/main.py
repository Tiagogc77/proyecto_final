# Importar módulos necesarios
import tkinter as tk
from tkinter import messagebox
from ventana_1 import Ventana1
from ventana_2 import Ventana2
from conexion_mysql import conectar

# Definir la clase para la VentanaPrincipal
class VentanaPrincipal:
    def __init__(self, root):
        # Inicializar la instancia y crear la ventana principal
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("300x200")

        # Crear etiquetas, entradas y botón para el inicio de sesión
        self.lbl_correo = tk.Label(root, text="Correo:")
        self.entry_correo = tk.Entry(root)

        self.lbl_contrasena = tk.Label(root, text="Contraseña:")
        self.entry_contrasena = tk.Entry(root, show="*")

        self.btn_iniciar_sesion = tk.Button(root, text="Iniciar Sesión", command=self.iniciar_sesion)

        # Empaquetar widgets en la ventana
        self.lbl_correo.pack(pady=10)
        self.entry_correo.pack(pady=10)
        self.lbl_contrasena.pack(pady=10)
        self.entry_contrasena.pack(pady=10)
        self.btn_iniciar_sesion.pack(pady=10)

    # Método para el inicio de sesión
    def iniciar_sesion(self):
        # Obtener valores de las entradas
        correo = self.entry_correo.get()
        contrasena = self.entry_contrasena.get()

        # Verificar las credenciales
        if verificar_credenciales(correo, contrasena):
            # Mostrar mensaje de inicio de sesión exitoso
            messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso.")
            self.root.withdraw()  # Ocultar la ventana de inicio de sesión
            app = Ventana2(self.root)  # Mostrar la ventana de datos de COVID
        else:
            # Mostrar mensaje de credenciales incorrectas
            messagebox.showwarning("Inicio de Sesión", "Credenciales incorrectas. Inténtelo nuevamente.")

# Función para verificar las credenciales en la base de datos
def verificar_credenciales(correo, contrasena):
    try:
        conexion = conectar()
        if conexion:
            cursor = conexion.cursor()
            consulta = "SELECT * FROM usuarios WHERE correo = %s AND contrasena = %s"
            cursor.execute(consulta, (correo, contrasena))
            usuario = cursor.fetchone()
            return usuario is not None
    except Exception as e:
        print(f"Error al verificar credenciales: {e}")
    finally:
        if conexion:
            conexion.close()

# Bloque principal para ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()
