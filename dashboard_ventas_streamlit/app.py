import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Dashboard de Ventas", page_icon="📊", layout="wide")

st.title("📊 Dashboard interactivo de ventas")
st.caption("Proyecto académico de visualización de datos con Python, Streamlit y Plotly.")

DATA_PATH = Path(__file__).parent / "data" / "sales.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df

df = load_data()

st.sidebar.header("Filtros")
min_date = df["fecha"].min().date()
max_date = df["fecha"].max().date()
date_range = st.sidebar.date_input("Rango de fechas", value=(min_date, max_date),
                                   min_value=min_date, max_value=max_date)
categories = sorted(df["categoria"].unique().tolist())
selected_categories = st.sidebar.multiselect("Categorías", categories, default=categories)

filtered = df.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[(filtered["fecha"].dt.date >= start_date) & (filtered["fecha"].dt.date <= end_date)]
if selected_categories:
    filtered = filtered[filtered["categoria"].isin(selected_categories)]
else:
    filtered = filtered.iloc[0:0]

if filtered.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

total_sales = filtered["ventas"].sum()
total_units = filtered["unidades"].sum()
avg_sale = filtered["ventas"].mean()
num_orders = filtered["pedido_id"].nunique()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Ventas totales", f"S/ {total_sales:,.2f}")
c2.metric("Unidades vendidas", f"{total_units:,}")
c3.metric("Promedio por registro", f"S/ {avg_sale:,.2f}")
c4.metric("Pedidos registrados", f"{num_orders:,}")

st.divider()
left, right = st.columns(2)
with left:
    by_category = filtered.groupby("categoria", as_index=False)["ventas"].sum().sort_values("ventas", ascending=False)
    fig_cat = px.bar(by_category, x="categoria", y="ventas", title="Ventas por categoría",
                     labels={"categoria": "Categoría", "ventas": "Ventas (S/)"},
                     text_auto=".2s")
    st.plotly_chart(fig_cat, use_container_width=True)
with right:
    by_date = filtered.groupby(filtered["fecha"].dt.to_period("M").astype(str), as_index=False)["ventas"].sum()
    by_date = by_date.rename(columns={"fecha": "mes"})
    fig_time = px.line(by_date, x="mes", y="ventas", markers=True, title="Evolución mensual de ventas",
                       labels={"mes": "Mes", "ventas": "Ventas (S/)"})
    st.plotly_chart(fig_time, use_container_width=True)

left2, right2 = st.columns(2)
with left2:
    by_product = filtered.groupby("producto", as_index=False)["ventas"].sum().sort_values("ventas", ascending=False).head(10)
    fig_prod = px.bar(by_product, x="ventas", y="producto", orientation="h",
                      title="10 productos con mayores ventas",
                      labels={"producto": "Producto", "ventas": "Ventas (S/)"})
    st.plotly_chart(fig_prod, use_container_width=True)
with right2:
    st.subheader("Datos filtrados")
    st.dataframe(filtered.sort_values("fecha", ascending=False), use_container_width=True, hide_index=True)

st.caption("Nota: el archivo incluido contiene datos de ejemplo creados para fines académicos. Reemplázalos por datos reales si tu docente lo solicita.")
