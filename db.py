# db.py
import mysql.connector as mysql

DB_CFG = {
    "host": "localhost",
    "user": "root",            # Usuario MySQL
    "password": "123456", # <-- cámbialo por tu clave
    "database": "tienda_online"
}

def get_conn():
    """Devuelve una conexión a la base de datos MySQL."""
    return mysql.connect(**DB_CFG)
