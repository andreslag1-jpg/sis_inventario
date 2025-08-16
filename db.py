# db.py
import mysql.connector as mysql

DB_CFG = {
    "host": "localhost",
    "user": "root",           
    "password": "CAMBIAR_EN_LOCAL",
    "database": "tienda_online"
}

def get_conn():
    """Devuelve una conexión a la base de datos MySQL."""
    return mysql.connect(**DB_CFG)

