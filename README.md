# 📊 Sistema Automatizado de Análisis, Auditoría Defensiva y Reportes CSV

Sistema corporativo de procesamiento de datos desarrollado en Python. Diseñado para transformar archivos CSV masivos de transacciones comerciales en un **Dashboard Ejecutivo** claro, realizando una auditoría defensiva estricta de registros corruptos y permitiendo la exportación de reportes limpios mediante una interfaz de línea de comandos (CLI).

---

## 🚀 Características Principales

* **🛡️ Programación Defensiva (Data Cleansing):** Valida de forma segura cada celda numérica (`int` y `float`) utilizando bloques `try/except`. Si una celda contiene datos corruptos, vacíos o negativos, el sistema la aísla, incrementa el contador de errores e imprime un **Log de Auditoría detallado** sin interrumpir la ejecución.
* **⚡ Procesamiento de Un Solo Pase (*Single-Pass Processing*):** Lee, valida, acumula métricas financieras y filtra los datos en un solo recorrido del archivo, optimizando el rendimiento de memoria y velocidad.
* **📈 Dashboard Ejecutivo Completo:** Calcula en tiempo real:
  * Ingresos totales globales.
  * Ventas desagregadas por categoría comercial.
  * Producto más vendido (Top Performer).
  * Fecha histórica con récord de ventas.
* **💻 Interfaz de Línea de Comandos (CLI):** Configurado con `argparse` para recibir parámetros flexibles desde la terminal (`--entrada`, `--salida`, `--categoria`).
* **📋 Vista Previa Tabular:** Renderiza una tabla limpia directamente en la consola con los primeros registros del reporte procesado.

---

## 🛠️ Tecnologías y Módulos Utilizados

* **Python 3.14+** (Lenguaje principal)
* **`csv`**: Manipulación nativa de archivos tabulares (`DictReader`, `DictWriter`).
* **`argparse`**: Gestión nativa de argumentos de consola.
* **`collections.defaultdict`**: Agregaciones eficientes de datos corporativos.
* **`os`**: Verificación de rutas del sistema operativo.

---

## ⚙️ Instrucciones de Uso (CLI)

Puedes ejecutar el programa directamente desde tu terminal utilizando las banderas configuradas:

1. **Ejecución por defecto (Filtra la categoría 'Electrónica'):**
   ```bash
   python main.py
   python main.py --categoria Muebles --salida datos/reporte_muebles.csv
   python main.py --help
   ```