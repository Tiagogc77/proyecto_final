import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='4568',
            database='Covid_19'
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
