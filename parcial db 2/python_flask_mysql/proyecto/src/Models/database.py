import mysql.connector

try:
    database = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='parcial3'
    )
    print("Se conectó correctamente a la base de datos")
except mysql.connector.Error as err:
    print(f"No se pudo conectar a la base de datos: {err}")
