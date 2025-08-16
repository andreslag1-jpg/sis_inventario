# inventario.py
from typing import Optional, List, Tuple
from db import get_conn

class Inventario:
    def listar_productos(self) -> List[Tuple]:
        sql = """
        SELECT p.id_producto, p.nombre, p.descripcion, p.precio,
               COALESCE(SUM(i.cantidad), 0) AS cantidad_total,
               GROUP_CONCAT(DISTINCT i.ubicacion_bodega ORDER BY i.ubicacion_bodega SEPARATOR ', ') AS bodegas
        FROM producto p
        LEFT JOIN inventario i ON p.id_producto = i.id_producto
        GROUP BY p.id_producto, p.nombre, p.descripcion, p.precio
        ORDER BY p.id_producto;
        """
        with get_conn() as cn, cn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    def agregar_producto(
        self,
        nombre: str,
        descripcion: str,
        precio: float,
        imagen: Optional[str] = None,
        cantidad_inicial: int = 0,
        ubicacion_bodega: str = "Bodega Central",
    ) -> int:
        with get_conn() as cn, cn.cursor() as cur:
            cur.execute(
                "SELECT id_producto FROM producto WHERE nombre=%s AND descripcion=%s",
                (nombre, descripcion),
            )
            row = cur.fetchone()
            if row:
                existente = row[0]
                if cantidad_inicial and cantidad_inicial > 0:
                    cur.execute(
                        "UPDATE inventario SET cantidad = cantidad + %s "
                        "WHERE id_producto=%s AND ubicacion_bodega=%s",
                        (cantidad_inicial, existente, ubicacion_bodega),
                    )
                    if cur.rowcount == 0:
                        cur.execute(
                            "INSERT INTO inventario (id_producto, cantidad, ubicacion_bodega) "
                            "VALUES (%s, %s, %s)",
                            (existente, cantidad_inicial, ubicacion_bodega),
                        )
                    cn.commit()
                return existente

            cur.execute(
                "INSERT INTO producto (nombre, descripcion, precio, imagen) VALUES (%s, %s, %s, %s)",
                (nombre, descripcion, precio, imagen),
            )
            nuevo_id = cur.lastrowid

            if cantidad_inicial and cantidad_inicial > 0:
                cur.execute(
                    "INSERT INTO inventario (id_producto, cantidad, ubicacion_bodega) VALUES (%s, %s, %s)",
                    (nuevo_id, cantidad_inicial, ubicacion_bodega),
                )
            cn.commit()
            return nuevo_id

    def actualizar_producto(
        self,
        id_producto: int,
        nombre: str,
        descripcion: str,
        precio: float,
        imagen: Optional[str] = None,
    ) -> bool:
        with get_conn() as cn, cn.cursor() as cur:
            cur.execute(
                "UPDATE producto SET nombre=%s, descripcion=%s, precio=%s, imagen=%s WHERE id_producto=%s",
                (nombre, descripcion, precio, imagen, id_producto),
            )
            cn.commit()
            return cur.rowcount > 0

    def eliminar_producto(self, id_producto: int) -> bool:
        with get_conn() as cn, cn.cursor() as cur:
            try:
                cn.start_transaction()
                cur.execute("DELETE FROM venta WHERE id_producto=%s", (id_producto,))
                cur.execute("DELETE FROM inventario WHERE id_producto=%s", (id_producto,))
                cur.execute("DELETE FROM producto WHERE id_producto=%s", (id_producto,))
                cn.commit()
                return cur.rowcount > 0
            except Exception:
                cn.rollback()
                raise

    def ajustar_stock(
        self,
        id_producto: int,
        delta: int,
        ubicacion_bodega: str = "Bodega Central",
    ) -> None:
        with get_conn() as cn, cn.cursor() as cur:
            cur.execute(
                "UPDATE inventario SET cantidad = cantidad + %s "
                "WHERE id_producto=%s AND ubicacion_bodega=%s",
                (delta, id_producto, ubicacion_bodega),
            )
            if cur.rowcount == 0:
                cur.execute(
                    "INSERT INTO inventario (id_producto, cantidad, ubicacion_bodega) VALUES (%s, %s, %s)",
                    (id_producto, max(delta, 0), ubicacion_bodega),
                )
            cn.commit()


