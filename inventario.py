# inventario.py
from typing import Optional, List, Tuple
from db import get_conn

class Inventario:
    """Operaciones CRUD de productos e inventario en tienda_online."""

    def listar_productos(self) -> List[Tuple]:
        """
        Lista productos con stock total (suma en todas las bodegas) y
        muestra en qué bodegas hay existencias.
        """
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

    def agregar_producto(self, nombre: str, descripcion: str, precio: float,
                         imagen: Optional[str] = None,
                         cantidad_inicial: int = 0,
                         ubicacion_bodega: str = "Bodega Central") -> int:
        """
        Crea producto (si no existe uno con mismo nombre y descripción) y,
        opcionalmente, una fila de inventario inicial.
        """
        with get_conn() as cn, cn.cursor() as cur:
            # 0) Verificar duplicado por nombre + descripción
            cur.execute(
                "SELECT id_producto FROM producto WHERE nombre=%s AND descripcion=%s",
                (nombre, descripcion)
            )
            row = cur.fetchone()
            if row:
                existente = row[0]
                print(f"⚠ El producto ya existe con ID {existente}. No se insertó.")
                # Si llega cantidad_inicial, se suma stock en la bodega indicada
                if cantidad_inicial and cantidad_inicial > 0:
                    cur.execute(
                        "UPDATE inventario SET cantidad = cantidad + %s "
                        "WHERE id_producto=%s AND ubicacion_bodega=%s",
                        (cantidad_inicial, existente, ubicacion_bodega)
                    )
                    if cur.rowcount == 0:
                        cur.execute(
                            "INSERT INTO inventario (id_producto, cantidad, ubicacion_bodega) "
                            "VALUES (%s, %s, %s)",
                            (existente, cantidad_inicial, ubicacion_bodega)
                        )
                    cn.commit()
                return existente

            # 1) Insertar nuevo producto
            cur.execute(
                "INSERT INTO producto (nombre, descripcion, precio, imagen) VALUES (%s, %s, %s, %s)",
                (nombre, descripcion, precio, imagen)
            )
            nuevo_id = cur.lastrowid

            # 2) Insertar stock inicial si aplica
            if cantidad_inicial and cantidad_inicial > 0:
                cur.execute(
                    "INSERT INTO inventario (id_producto, cantidad, ubicacion_bodega) VALUES (%s, %s, %s)",
                    (nuevo_id, cantidad_inicial, ubicacion_bodega)
                )
            cn.commit()
            print(f"✅ Producto creado con ID {nuevo_id}")
            return nuevo_id

    def actualizar_producto(self, id_producto: int, nombre: str, descripcion: str,
                            precio: float, imagen: Optional[str] = None) -> bool:
        with get_conn() as cn, cn.cursor() as cur:
            cur.execute(
                "UPDATE producto SET nombre=%s, descripcion=%s, precio=%s, imagen=%s WHERE id_producto=%s",
                (nombre, descripcion, precio, imagen, id_producto)
            )
            cn.commit()
            return cur.rowcount > 0

    def eliminar_producto(self, id_producto: int) -> bool:
        """Elimina ventas -> inventario -> producto en una transacción."""
        with get_conn() as cn, cn.cursor() as cur:
            try:
                cn.start_transaction()
                # 1) borrar ventas del producto
                cur.execute("DELETE FROM venta WHERE id_producto=%s", (id_producto,))
                # 2) borrar inventario del producto
                cur.execute("DELETE FROM inventario WHERE id_producto=%s", (id_producto,))
                # 3) borrar el producto
                cur.execute("DELETE FROM producto WHERE id_producto=%s", (id_producto,))
                cn.commit()
                return cur.rowcount > 0  # del último DELETE
            except Exception:
                cn.rollback()
                raise

    def ajustar_stock(self, id_producto: int, delta: int,
                      ubicacion_bodega: str = "Bodega Central") -> None:
        """
        Suma/resta stock en una bodega. Si no existe la fila en esa bodega, la crea con delta>=0.
        """
        with get_conn() as cn, cn.cursor() as cur:
            cur.execute(
                "UPDATE inventario SET cantidad = cantidad + %s WHERE id_producto=%s AND ubicacion_bodega=%s",
                (delta, id_producto, ubicacion_bodega)
            )
            if cur.rowcount == 0:
                cur.execute(
                    "INSERT INTO inventario (id_producto, cantidad, ubicacion_bodega) VALUES (%s, %s, %s)",
                    (id_producto, max(delta, 0), ubicacion_bodega)
                )
            cn.commit()

