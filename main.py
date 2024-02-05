import mysql.connector
from mysql.connector import MySQLConnection, Error
import time

# Configura la conexión a la base de datos
def conectar():
    try:
        conexion = mysql.connector.connect(
            host='tu_host',
            database='tu_base_de_datos',
            user='tu_usuario',
            password='tu_contraseña'
        )
        if conexion.is_connected():
            print('Conexión establecida.')
            return conexion
    except Error as e:
        print(f'Error: {e}')

# Verifica si hay una nueva tabla en la base de datos
def verificar_nueva_tabla(conexion, tablas_anteriores):
    cursor = conexion.cursor()
    cursor.execute("SHOW TABLES;")
    tablas_actuales = [tabla[0] for tabla in cursor.fetchall()]

    nueva_tabla = set(tablas_actuales) - set(tablas_anteriores)

    if nueva_tabla:
        print(f'Se ha creado una nueva tabla: {nueva_tabla.pop()}')

    cursor.close()

# Verifica el número de datos en una tabla
def verificar_numero_datos(conexion, tabla, limite=1000):
    cursor = conexion.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {tabla};")
    numero_datos = cursor.fetchone()[0]

    if numero_datos >= limite:
        print(f'La tabla {tabla} ha alcanzado {limite} datos.')

    cursor.close()

# Función principal
def main():
    conexion = conectar()
    tablas_anteriores = set()

    try:
        while True:
            verificar_nueva_tabla(conexion, tablas_anteriores)

            # Especifica aquí las tablas que deseas monitorear
            tablas_a_monitorear = ['tabla1', 'tabla2']

            for tabla in tablas_a_monitorear:
                verificar_numero_datos(conexion, tabla)

            tablas_anteriores = set(tablas_a_monitorear)

            # Espera 60 segundos antes de volver a verificar
            time.sleep(60)

    except KeyboardInterrupt:
        print('Script finalizado.')

    finally:
        if conexion.is_connected():
            conexion.close()
            print('Conexión cerrada.')

if __name__ == '__main__':
    main()
