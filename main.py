import argparse
import csv
import os
from collections import defaultdict


def validar_entero_seguro(valor_str):
    """Convierte un string de una celda a entero de forma segura. Devuelve 0 si hay error."""
    try:
        valor = int(valor_str)
        return valor if valor > 0 else 0
    except ValueError:
        return 0


def validar_flotante_seguro(valor_str):
    """Convierte un string de una celda a float de forma segura. Devuelve 0.0 si hay error."""
    try:
        valor = float(valor_str)
        return valor if valor > 0 else 0.0
    except ValueError:
        return 0.0


def analizar_y_exportar_reporte_maestro(ruta_entrada, ruta_salida, categoria_filtro):
    """Procesa el CSV, realiza auditoría defensiva detallada, calcula métricas ejecutivas y exporta el reporte."""
    if not os.path.exists(ruta_entrada):
        print(f"[ERROR] No se encontró el archivo de origen: {ruta_entrada}")
        return

    registros_totales = 0
    registros_corruptos = 0
    detalles_errores = []  # <--- NUEVO: Lista para almacenar el log de registros corruptos
    transacciones_validas = []
    transacciones_filtradas = []

    total_ingresos_global = 0.0
    ventas_por_categoria = defaultdict(float)
    unidades_por_producto = defaultdict(int)
    ventas_por_fecha = defaultdict(float)

    try:
        # 1. Lectura, Auditoría y Cálculo de Métricas en un solo pase
        with open(ruta_entrada, mode="r", encoding="utf-8") as archivo_in:
            lector = csv.DictReader(archivo_in)
            for fila in lector:
                registros_totales += 1

                # Extracción de identificadores para auditoría visual
                id_transaccion = fila.get("id", "N/A")
                nombre_producto = fila.get("producto", "Desconocido")

                cantidad = validar_entero_seguro(fila["cantidad"])
                precio_unitario = validar_flotante_seguro(fila["precio_unitario"])

                # Validación defensiva con registro detallado de errores
                if cantidad <= 0 or precio_unitario <= 0:
                    registros_corruptos += 1
                    detalles_errores.append(
                        f"  -> Fila ID {id_transaccion} ({nombre_producto}): Cantidad ({fila['cantidad']}) o Precio ({fila['precio_unitario']}) inválidos."
                    )
                    continue

                total_venta = cantidad * precio_unitario
                fila["total_venta"] = f"{total_venta:.2f}"  # Formato con 2 decimales limpios

                total_ingresos_global += total_venta
                ventas_por_categoria[fila["categoria"]] += total_venta
                unidades_por_producto[nombre_producto] += cantidad
                ventas_por_fecha[fila["fecha"]] += total_venta

                transacciones_validas.append(fila)

                if fila["categoria"].strip().lower() == categoria_filtro.strip().lower():
                    transacciones_filtradas.append(fila)

        producto_top = (
            max(unidades_por_producto, key=unidades_por_producto.get)
            if unidades_por_producto
            else "N/A"
        )
        fecha_top = (
            max(ventas_por_fecha, key=ventas_por_fecha.get)
            if ventas_por_fecha
            else "N/A"
        )

        # 2. Impresión del Dashboard Ejecutivo y Log de Errores
        print("==================================================")
        print("     📈 DASHBOARD EJECUTIVO Y AUDITORÍA DE DATOS   ")
        print("==================================================")
        print(f"📄 Registros Totales Procesados: {registros_totales}")
        print(f"⚠️ Registros Corruptos/Omitidos: {registros_corruptos}")
        
        # Si hubo errores, imprimimos el detalle exacto de cada uno (Log de Auditoría)
        if detalles_errores:
            print("\n   [DETALLE DE REGISTROS OMITIDOS]:")
            for error in detalles_errores:
                print(error)

        print(f"\n✅ Registros Válidos Auditados: {len(transacciones_validas)}")
        print("-" * 50)
        print(f"💰 Ingresos Totales Globales: ${total_ingresos_global:,.2f}")
        print(f"🏆 Producto Más Vendido: {producto_top} ({unidades_por_producto[producto_top]} pzas)")
        print(f"📅 Fecha Récord de Ventas: {fecha_top} (${ventas_por_fecha[fecha_top]:,.2f})")
        print("-" * 50)
        print("📁 VENTAS TOTALES POR CATEGORÍA:")
        for cat, monto in ventas_por_categoria.items():
            print(f"   • {cat:<18}: ${monto:,.2f}")
        print("==================================================")

        # 3. Exportación del Reporte Filtrado
        encabezados = [
            "id",
            "producto",
            "categoria",
            "cantidad",
            "precio_unitario",
            "total_venta",
            "fecha",
        ]

        with open(ruta_salida, mode="w", newline="", encoding="utf-8") as archivo_out:
            escritor = csv.DictWriter(archivo_out, fieldnames=encabezados)
            escritor.writeheader()
            for transaccion in transacciones_filtradas:
                escritor.writerow(transaccion)

        print(f"\n✅ ¡Reporte de '{categoria_filtro}' exportado con éxito a '{ruta_salida}'!")
        print(f"   Total de registros en este reporte: {len(transacciones_filtradas)}")

        # 4. NUEVO: Vista Tabular Limpia en Consola (primeros 5 registros del reporte)
        if transacciones_filtradas:
            print("\n📋 VISTA PREVIA TABULAR (Primeros registros del reporte):")
            print(f"{'ID':<5} | {'PRODUCTO':<22} | {'CANT':<5} | {'PRECIO':<8} | {'TOTAL':<8} | {'FECHA'}")
            print("-" * 65)
            # Mostramos un máximo de 5 filas para no saturar la terminal
            for t in transacciones_filtradas[:5]:
                print(
                    f"{t['id']:<5} | {t['producto']:<22} | {t['cantidad']:<5} | ${float(t['precio_unitario']):<7.2f} | ${float(t['total_venta']):<7.2f} | {t['fecha']}"
                )
            if len(transacciones_filtradas) > 5:
                print(f"   ... [Y {len(transacciones_filtradas) - 5} registros más guardados en el archivo]")
            print("==================================================")

    except Exception as e:
        print(f"[ERROR] Ocurrió un fallo en el procesamiento maestro: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sistema corporativo de análisis, auditoría defensiva y filtrado de reportes CSV."
    )
    parser.add_argument(
        "--entrada",
        default="datos/ventas_masivas.csv",
        help="Ruta del archivo CSV de origen con los datos masivos.",
    )
    parser.add_argument(
        "--salida",
        default="datos/reporte_filtrado.csv",
        help="Ruta donde se exportará el nuevo reporte CSV limpio.",
    )
    parser.add_argument(
        "--categoria",
        default="Electrónica",
        help="Categoría comercial específica a filtrar (ej. Electrónica, Muebles, Papelería).",
    )

    args = parser.parse_args()

    print("🚀 Iniciando Sistema Maestro CLI de Análisis y Auditoría CSV...")
    analizar_y_exportar_reporte_maestro(args.entrada, args.salida, args.categoria)