# Importar módulos necesarios
from tkinter import messagebox
from conexion_mysql import conectar

# Función para eliminar datos de la base de datos
def eliminar_datos(id_dato, ventana):
    try:
        # Establecer conexión a la base de datos
        conexion = conectar()

        if conexion:
            try:
                # Crear un cursor para ejecutar consultas SQL
                cursor = conexion.cursor()

                # Definir la consulta SQL para eliminar datos con un ID específico
                consulta = "DELETE FROM datos_covid WHERE id=%s"

                # Ejecutar la consulta con el ID proporcionado
                cursor.execute(consulta, (id_dato,))

                # Confirmar la transacción en la base de datos
                conexion.commit()

                # Imprimir mensaje indicando que el dato fue eliminado
                print(f"Dato con id={id_dato} eliminado de la base de datos")

                # Recargar los datos en la ventana después de la eliminación
                ventana.cargar_datos()

            except Exception as err:
                # Imprimir mensaje en caso de error al eliminar datos
                print(f"Error al eliminar datos de la base de datos: {err}")

            finally:
                # Cerrar el cursor y la conexión
                cursor.close()
                conexion.close()

    except Exception as e:
        # Imprimir mensaje en caso de error al establecer conexión con la base de datos
        print(f"Error al establecer conexión con la base de datos: {e}")
