import streamlit as st
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="🌍 Dashboard Demo", layout="wide")

st.title("🌍 Dashboard con tooltip personalizado")

# Datos de ejemplo
df = px.data.gapminder().query("year == 2007")
df_filtrado = df[df["continent"] == "Americas"]

# Crear gráfico
fig = px.scatter(
    df_filtrado,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="country"
)

# Tooltip en español y bordes redondeados
fig.update_traces(
    hovertemplate="<b>País:</b> %{customdata[0]}<br>" +
                  "<b>PIB per cápita:</b> %{x}<br>" +
                  "<b>Esperanza de vida:</b> %{y}<br>" +
                  "<b>Población:</b> %{marker.size}<extra></extra>",
    customdata=df_filtrado[["country"]]
)

# Personalización del estilo del tooltip
fig.update_layout(
    hoverlabel=dict(
        bgcolor="rgba(30,30,40,0.9)",   # Fondo oscuro semitransparente
        font_size=13,
        font_color="white",
        bordercolor="#00f5d4",          # Borde neón tech
    )
)

# ⚠️ Hack para bordes redondeados (Plotly no lo soporta directamente)
# Usamos CSS inyectado a través de Streamlit
st.markdown("""
    <style>
    .hoverlayer .hovertext {
        border-radius: 12px !important;
        padding: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)

