# ventas.py
from db import get_conn

class Ventas:
    """Registra ventas y descuenta stock con transacción."""

    def __init__(self):
        self._ensure_table()

    def _ensure_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS venta (
            id_venta INT AUTO_INCREMENT PRIMARY KEY,
            id_producto INT NOT NULL,
            cantidad INT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        ) ENGINE=InnoDB;
        """
        with get_conn() as cn, cn.cursor() as cur:
            cur.execute(sql)
            cn.commit()

    def registrar_venta(self, id_producto: int, cantidad: int,
                        ubicacion_bodega: str = "Bodega Central") -> bool:
        with get_conn() as cn, cn.cursor() as cur:
            cn.start_transaction()
            cur.execute(
                "SELECT cantidad FROM inventario WHERE id_producto=%s AND ubicacion_bodega=%s FOR UPDATE",
                (id_producto, ubicacion_bodega)
            )
            row = cur.fetchone()
            if not row or row[0] < cantidad:
                cn.rollback()
                return False
            cur.execute(
                "UPDATE inventario SET cantidad = cantidad - %s WHERE id_producto=%s AND ubicacion_bodega=%s",
                (cantidad, id_producto, ubicacion_bodega)
            )
            cur.execute(
                "INSERT INTO venta (id_producto, cantidad) VALUES (%s, %s)",
                (id_producto, cantidad)
            )
            cn.commit()
            return True
