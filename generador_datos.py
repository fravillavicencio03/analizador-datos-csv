import csv
import os
import random
from datetime import datetime, timedelta

# Aseguramos que la carpeta 'datos' exista
os.makedirs("datos", exist_ok=True)
RUTA_SALIDA = "datos/ventas_masivas.csv"

# Listas de datos para combinar de forma aleatoria
PRODUCTOS = [
    ("Laptop Gamer", "Electrónica", 850.00),
    ("Teclado Mecánico", "Electrónica", 45.50),
    ("Mouse Inalámbrico", "Electrónica", 25.00),
    ("Monitor 24 pulgadas", "Electrónica", 150.00),
    ("Audífonos Bluetooth", "Electrónica", 60.00),
    ("Silla Ergonómica", "Muebles", 180.00),
    ("Escritorio Minimalista", "Muebles", 220.00),
    ("Libreta de Notas", "Papelería", 5.00),
    ("Bolígrafos (Caja)", "Papelería", 8.50),
    ("Organizador de Escritorio", "Papelería", 12.00),
    ("Impresora Láser", "Electrónica", 130.00),
    ("Lámpara LED de Escritorio", "Muebles", 35.00),
]

# Fecha inicial para simular un rango de tiempo
FECHA_INICIO = datetime(2026, 1, 1)


def generar_csv_masivo(nombre_archivo, total_registros=550):
    """Genera un archivo CSV con una cantidad masiva de transacciones simuladas."""
    print(f"Generando {total_registros} registros de prueba...")

    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)

        # Escribimos los encabezados
        escritor.writerow(
            ["id", "producto", "categoria", "cantidad", "precio_unitario", "fecha"]
        )

        for i in range(1, total_registros + 1):
            # Seleccionamos un producto aleatorio de nuestra lista
            producto_info = random.choice(PRODUCTOS)
            nombre_producto = producto_info[0]
            categoria = producto_info[1]
            precio = producto_info[2]

            # Cantidad aleatoria entre 1 y 15
            cantidad = random.randint(1, 15)

            # Fecha aleatoria dentro de los últimos 300 días del 2026
            dias_aleatorios = random.randint(0, 280)
            fecha_transaccion = FECHA_INICIO + timedelta(days=dias_aleatorios)
            fecha_str = fecha_transaccion.strftime("%Y-%m-%d")

            # Escribimos la fila en el CSV
            escritor.writerow(
                [i, nombre_producto, categoria, cantidad, precio, fecha_str]
            )

    print(
        f"✅ ¡Archivo masivo generado con éxito en '{nombre_archivo}' con {total_registros} registros!"
    )


if __name__ == "__main__":
    generar_csv_masivo(RUTA_SALIDA, 550)