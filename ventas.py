from typing import Tuple
from db import get_conn

class Ventas:
    def registrar_venta(self, id_producto: int, cantidad: int, ubicacion_bodega: str = "Bodega Central") -> Tuple[bool, str]:
        with get_conn() as cn, cn.cursor() as cur:
            try:
                cn.start_transaction()
                cur.execute(
                    "SELECT cantidad FROM inventario WHERE id_producto=%s AND ubicacion_bodega=%s FOR UPDATE",
                    (id_producto, ubicacion_bodega),
                )
                row = cur.fetchone()
                if not row or row[0] < cantidad:
                    cn.rollback()
                    return False, "Stock insuficiente o producto inexistente en la bodega"
                cur.execute(
                    "INSERT INTO venta (id_producto, cantidad, ubicacion_bodega, fecha) VALUES (%s, %s, %s, NOW())",
                    (id_producto, cantidad, ubicacion_bodega),
                )
                cur.execute(
                    "UPDATE inventario SET cantidad = cantidad - %s WHERE id_producto=%s AND ubicacion_bodega=%s",
                    (cantidad, id_producto, ubicacion_bodega),
                )
                cn.commit()
                return True, "Venta registrada"
            except Exception:
                cn.rollback()
                raise

