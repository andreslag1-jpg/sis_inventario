# reportes.py
from typing import List, Tuple
from db import get_conn

class Reportes:
    def inventario_detallado(self) -> List[Tuple]:
        sql = """
        SELECT p.id_producto, p.nombre, p.descripcion, p.precio,
               i.cantidad, i.ubicacion_bodega,
               (p.precio * i.cantidad) AS valor_total
        FROM producto p
        JOIN inventario i ON p.id_producto = i.id_producto
        ORDER BY i.ubicacion_bodega, p.nombre;
        """
        with get_conn() as cn, cn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    def resumen_por_bodega(self) -> List[Tuple]:
        sql = """
        SELECT i.ubicacion_bodega,
               COUNT(DISTINCT p.id_producto) AS productos_diferentes,
               SUM(i.cantidad) AS total_unidades,
               SUM(p.precio * i.cantidad) AS valor_total_bodega
        FROM producto p
        JOIN inventario i ON p.id_producto = i.id_producto
        GROUP BY i.ubicacion_bodega
        ORDER BY i.ubicacion_bodega;
        """
        with get_conn() as cn, cn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
