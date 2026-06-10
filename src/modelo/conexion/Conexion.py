import os
import jpype
import jaydebeapi

def obtener_conexion():
    """Establece y devuelve la conexión JDBC a SQL Server"""
    jar_name = "mssql-jdbc-13.4.0.jre11.jar"

    base_dir = os.path.dirname(os.path.abspath(__file__))
    jar_path = os.path.normpath(os.path.join(base_dir, '..', '..', '..', 'lib', jar_name))

    if not os.path.exists(jar_path):
        raise FileNotFoundError(f"No se encuentra el archivo JAR en: {jar_path}")

    if not jpype.isJVMStarted():
        jpype.startJVM(jpype.getDefaultJVMPath(), f"-Djava.class.path={jar_path}")

    server = "localhost\\SQLEXPRESS"
    port = "1433"
    database = "SGA_Database"
    user = "sa"
    password = "password"

    driver_class = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    connection_url = f"jdbc:sqlserver://{server}:{port};databaseName={database};encrypt=true;trustServerCertificate=true;"

    return jaydebeapi.connect(driver_class, connection_url, [user, password], jar_path)