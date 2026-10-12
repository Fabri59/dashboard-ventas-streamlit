# dashboard-ventas-streamlit

Dashboard interactivo para explorar datos de ventas. Está desarrollado con Python, Streamlit, Pandas y Plotly, y usa un conjunto de datos de ejemplo incluido en el repositorio.

## Funcionalidades

- Indicadores de ventas totales, unidades vendidas, promedio por registro y pedidos.
- Filtros por rango de fechas y categoría.
- Gráficos de ventas por categoría, evolución mensual y productos más vendidos.
- Tabla de registros filtrados.

## Requisitos

- Python 3.10 o superior.

## Ejecución local

Desde la raíz del repositorio, instala las dependencias y ejecuta la aplicación:

```bash
cd dashboard_ventas_streamlit
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit mostrará la dirección local para abrir el dashboard en el navegador.

## Datos

El archivo `dashboard_ventas_streamlit/data/sales.csv` contiene datos de ejemplo creados con fines académicos; no representan ventas reales.
