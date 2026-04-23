import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Monitor Dólar Argentina",
    page_icon="💵",
    layout="wide"
)

st.title("💵 Monitor Dólar Argentina")
st.caption("Valores del dólar Blue y Oficial — datos históricos vía Bluelytics")

# ── Fetch de datos ────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def cargar_datos(dias: int) -> pd.DataFrame:
    url = f"https://api.bluelytics.com.ar/v2/evolution.json?days={dias}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    datos = r.json()

    df = pd.DataFrame(datos)
    df["date"] = pd.to_datetime(df["date"])

    blue   = df[df["source"] == "Blue"].rename(columns={"value_sell": "blue_venta", "value_buy": "blue_compra"})
    oficial = df[df["source"] == "Oficial"].rename(columns={"value_sell": "oficial_venta", "value_buy": "oficial_compra"})

    merged = pd.merge(
        blue[["date", "blue_venta", "blue_compra"]],
        oficial[["date", "oficial_venta", "oficial_compra"]],
        on="date"
    ).sort_values("date").reset_index(drop=True)

    merged = merged.rename(columns={"date": "fecha"})
    return merged

@st.cache_data(ttl=300)
def cargar_actual():
    url = "https://api.bluelytics.com.ar/v2/latest"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Configuración")
    periodo = st.selectbox(
        "Período histórico",
        options=[30, 90, 180, 365, 730],
        format_func=lambda x: {
            30: "1 mes", 90: "3 meses", 180: "6 meses",
            365: "1 año", 730: "2 años"
        }[x],
        index=3
    )
    mostrar_compra = st.checkbox("Mostrar precio compra", value=False)
    mostrar_blue   = st.checkbox("Mostrar Blue", value=True)
    mostrar_ofic   = st.checkbox("Mostrar Oficial", value=True)

# ── Carga ─────────────────────────────────────────────────────────────────────
try:
    df     = cargar_datos(periodo)
    actual = cargar_actual()
except Exception as e:
    st.error(f"No se pudo conectar a la API: {e}")
    st.stop()

# ── Métricas actuales ─────────────────────────────────────────────────────────
blue_venta   = actual["blue"]["value_sell"]
blue_compra  = actual["blue"]["value_buy"]
ofic_venta   = actual["oficial"]["value_sell"]
ofic_compra  = actual["oficial"]["value_buy"]
brecha       = round((blue_venta / ofic_venta - 1) * 100, 1)
ultima_act   = actual["last_update"][:10]

st.subheader("Valores actuales")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🔵 Blue venta",    f"${blue_venta:,.0f}")
col2.metric("🔵 Blue compra",   f"${blue_compra:,.0f}")
col3.metric("🏦 Oficial venta", f"${ofic_venta:,.0f}")
col4.metric("🏦 Oficial compra",f"${ofic_compra:,.0f}")
col5.metric("📊 Brecha",        f"{brecha}%")

st.caption(f"Última actualización: {ultima_act}")
st.divider()

# ── Gráfico ───────────────────────────────────────────────────────────────────
fig = go.Figure()

if mostrar_blue:
    fig.add_trace(go.Scatter(
        x=df["fecha"], y=df["blue_venta"],
        name="Blue venta",
        line=dict(color="#3B82F6", width=2),
        hovertemplate="<b>Blue venta</b><br>%{x|%d/%m/%Y}<br>$%{y:,.0f}<extra></extra>"
    ))
    if mostrar_compra:
        fig.add_trace(go.Scatter(
            x=df["fecha"], y=df["blue_compra"],
            name="Blue compra",
            line=dict(color="#93C5FD", width=1.5, dash="dot"),
            hovertemplate="<b>Blue compra</b><br>%{x|%d/%m/%Y}<br>$%{y:,.0f}<extra></extra>"
        ))

if mostrar_ofic:
    fig.add_trace(go.Scatter(
        x=df["fecha"], y=df["oficial_venta"],
        name="Oficial venta",
        line=dict(color="#10B981", width=2),
        hovertemplate="<b>Oficial venta</b><br>%{x|%d/%m/%Y}<br>$%{y:,.0f}<extra></extra>"
    ))
    if mostrar_compra:
        fig.add_trace(go.Scatter(
            x=df["fecha"], y=df["oficial_compra"],
            name="Oficial compra",
            line=dict(color="#6EE7B7", width=1.5, dash="dot"),
            hovertemplate="<b>Oficial compra</b><br>%{x|%d/%m/%Y}<br>$%{y:,.0f}<extra></extra>"
        ))

fig.update_layout(
    title="Evolución del dólar",
    xaxis_title="Fecha",
    yaxis_title="Precio (ARS)",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=480,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# ── Tabla de datos ────────────────────────────────────────────────────────────
with st.expander("Ver datos históricos"):
    df_show = df.copy()
    df_show["fecha"] = df_show["fecha"].dt.strftime("%d/%m/%Y")
    df_show.columns = ["Fecha", "Blue compra", "Blue venta", "Oficial compra", "Oficial venta"]
    st.dataframe(df_show.sort_values("Fecha", ascending=False), use_container_width=True)