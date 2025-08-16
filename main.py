# main.py - menú interactivo para CMD/Terminal
from inventario import Inventario
from ventas import Ventas
from reportes import Reportes

def print_tabla(rows, headers):
    if not rows:
        print("(sin datos)")
        return
    widths = [max(len(str(x)) for x in [h] + [r[i] for r in rows]) for i, h in enumerate(headers)]
    fmt = " | ".join("{:<" + str(w) + "}" for w in widths)
    print(fmt.format(*headers))
    print("-+-".join("-" * w for w in widths))
    for r in rows:
        print(fmt.format(*[str(x) for x in r]))

def pedir_int(msg, minimo=None):
    while True:
        try:
            v = int(input(msg).strip())
            if minimo is not None and v < minimo:
                print(f"Debe ser >= {minimo}")
                continue
            return v
        except ValueError:
            print("Ingresa un número entero válido.")

def pedir_float(msg, minimo=None):
    while True:
        try:
            txt = input(msg).strip().replace(",", ".")
            v = float(txt)
            if minimo is not None and v < minimo:
                print(f"Debe ser >= {minimo}")
                continue
            return v
        except ValueError:
            print("Ingresa un número (usa punto para decimales).")

def pausa():
    input("\n(Enter para continuar...)")

def menu():
    inv = Inventario()
    ven = Ventas()
    rep = Reportes()

    while True:
        print("\n==== SIS INVENTARIO (Python + MySQL) ====")
        print("1) Listar inventario (agregado por producto)")
        print("2) Ver inventario detallado (por bodega)")
        print("3) Agregar producto (con stock inicial)")
        print("4) Actualizar producto")
        print("5) Registrar venta (descontar stock)")
        print("6) Eliminar producto")
        print("7) Resumen por bodega")
        print("0) Salir")

        op = input("Elige una opción: ").strip()
        if op == "1":
            data = inv.listar_productos()
            print("\n=== Inventario (agregado) ===")
            print_tabla(data, ["id", "nombre", "descripcion", "precio", "stock_total", "bodegas"])
            pausa()

        elif op == "2":
            data = rep.inventario_detallado()
            print("\n=== Inventario detallado (por bodega) ===")
            print_tabla(data, ["id", "nombre", "descripcion", "precio", "cantidad", "bodega", "valor_total"])
            pausa()

        elif op == "3":
            print("\n=== Agregar producto ===")
            nombre = input("Nombre: ").strip()
            descripcion = input("Descripción: ").strip()
            precio = pedir_float("Precio: ", minimo=0)
            imagen = input("Imagen (opcional, nombre de archivo): ").strip() or None
            cantidad = pedir_int("Stock inicial (puede ser 0): ", minimo=0)
            bodega = input("Bodega (por defecto 'Bodega Central'): ").strip() or "Bodega Central"
            nuevo_id = inv.agregar_producto(nombre, descripcion, precio, imagen, cantidad, bodega)
            print(f"✅ Producto creado con id={nuevo_id}")
            pausa()

        elif op == "4":
            print("\n=== Actualizar producto ===")
            idp = pedir_int("ID del producto a actualizar: ", minimo=1)
            nombre = input("Nuevo nombre: ").strip()
            descripcion = input("Nueva descripción: ").strip()
            precio = pedir_float("Nuevo precio: ", minimo=0)
            imagen = input("Nueva imagen (opcional): ").strip() or None
            ok = inv.actualizar_producto(idp, nombre, descripcion, precio, imagen)
            print("✅ Producto actualizado" if ok else "⚠️ No se encontró el producto.")
            pausa()

        elif op == "5":
            print("\n=== Registrar venta ===")
            idp = pedir_int("ID del producto: ", minimo=1)
            cantidad = pedir_int("Cantidad a vender: ", minimo=1)
            bodega = input("Bodega (por defecto 'Bodega Central'): ").strip() or "Bodega Central"
            ok = ven.registrar_venta(idp, cantidad, bodega)
            print("✅ Venta registrada y stock actualizado" if ok else "❌ No hay stock suficiente o no existe el producto/bodega.")
            pausa()

        elif op == "6":
            print("\n=== Eliminar producto ===")
            idp = pedir_int("ID del producto a eliminar: ", minimo=1)
            conf = input(f"Confirmas eliminar el producto {idp}? (sí/no): ").strip().lower()
            if conf in ("si", "sí", "s"):
                try:
                    ok = inv.eliminar_producto(idp)
                    print("✅ Producto eliminado" if ok else "⚠️ No se encontró el producto.")
                except Exception as e:
                    print(f"❌ Error al eliminar: {e}")
            else:
                print("Operación cancelada.")
            pausa()

        elif op == "7":
            data = rep.resumen_por_bodega()
            print("\n=== Resumen por bodega ===")
            print_tabla(data, ["bodega", "prod_dif", "unidades", "valor_total"])
            pausa()

        elif op == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()

