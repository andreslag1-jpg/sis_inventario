# SIS INVENTARIO (Python + MySQL)

Sistema de inventario por bodegas con registro de ventas y menú en consola.
Incluye respaldo SQL del esquema **tienda_online**.

## Arquitectura
- **Python 3.x** + **MySQL**
- Dependencias: `mysql-connector-python`, `tabulate`
- Módulos:
  - `db.py` — conexión a MySQL.
  - `inventario.py` — CRUD de productos e inventario.
  - `ventas.py` — registro de ventas (descuenta stock).
  - `reportes.py` — consultas y reportes (inventario por bodega, etc.).
  - `main.py` — menú CLI que orquesta todo.

## Requisitos
```bash
pip install -r requirements.txt
