from tabulate import tabulate
from inventario import Inventario
from ventas import Ventas
from reportes import Reportes

inv = Inventario()
ven = Ventas()
rep = Reportes()

def pause():
    input("\n(Enter para continuar...)")

def listar_agregado():
    datos = inv.listar_productos()
    print("\n=== Inventario (agregado) ===")
    print(tabulate(datos, headers=["id","nombre","descripcion","precio","stock_total","bodegas"], tablefmt="github"))
    pause()

def inventario_detallado():
    datos = rep.inventario_detallado()
    print("\n=== Inventario detallado (por bodega) ===")
    print(tabulate(datos, headers=["id","nombre","descripcion","precio","cantidad","bodega"], tablefmt="github"))
    pause()

def agregar_producto():
    print("\n=== Agregar producto ===")
    nombre = input("Nombre: ").strip()
    descripcion = input("Descripción: ").strip()
    precio = float(input("Precio: ").strip())
    imagen = input("Imagen (opcional): ").strip() or None
    cantidad = int(input("Stock inicial (puede ser 0): ").strip() or "0")
    bodega = input("Bodega (defecto 'Bodega Central'): ").strip() or "Bodega Central"
    nuevo_id = inv.agregar_producto(nombre, descripcion, precio, imagen, cantidad, bodega)
    print(f"Producto id={nuevo_id}")
    pause()

def actualizar_producto():
    print("\n=== Actualizar producto ===")
    pid = int(input("ID producto: ").strip())
    nombre = input("Nombre: ").strip()
    descripcion = input("Descripción: ").strip()
    precio = float(input("Precio: ").strip())
    imagen = input("Imagen (opcional): ").strip() or None
    ok = inv.actualizar_producto(pid, nombre, descripcion, precio, imagen)
    print("Actualizado" if ok else "Sin cambios")
    pause()

def registrar_venta():
    print("\n=== Registrar venta ===")
    pid = int(input("ID producto: ").strip())
    cant = int(input("Cantidad: ").strip())
    bodega = input("Bodega (defecto 'Bodega Central'): ").strip() or "Bodega Central"
    ok, msg = ven.registrar_venta(pid, cant, bodega)
    print(msg)
    print("\nVenta registrada y stock actualizado" if ok else "\nNo se pudo registrar la venta")
    listar_agregado()

def eliminar_producto():
    print("\n=== Eliminar producto ===")
    pid = int(input("ID producto: ").strip())
    ok = inv.eliminar_producto(pid)
    print("Eliminado" if ok else "No existía o no se eliminó")
    pause()

def resumen_bodega():
    datos = rep.resumen_por_bodega()
    print("\n=== Resumen por bodega ===")
    print(tabulate(datos, headers=["bodega","prod_dif","unidades","valor_total"], tablefmt="github", floatfmt=".2f"))
    pause()

def menu():
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
        if op == "1": listar_agregado()
        elif op == "2": inventario_detallado()
        elif op == "3": agregar_producto()
        elif op == "4": actualizar_producto()
        elif op == "5": registrar_venta()
        elif op == "6": eliminar_producto()
        elif op == "7": resumen_bodega()
        elif op == "0": break
        else: print("Opción inválida")

if __name__ == "__main__":
    menu()



