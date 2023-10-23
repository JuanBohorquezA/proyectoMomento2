import pyodbc

# Parámetros de conexión
server = 'DESKTOP-T2MURQ7\SQLEXPRESS'
database = 'prueba'
username = 'sa'
password = '1118020878'

# Cadena de conexión
connection_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

# Intentar establecer la conexión
def conneccion():
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
    except:
        print("Conexión fallida")
    return cursor