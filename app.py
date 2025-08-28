import streamlit as st
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="🌍 Dashboard Demo", layout="wide")

st.markdown(
    """
    <style>
    /* Fondo general oscuro tipo tech */
    body {
        background-color: #0e1117;
        color: #fafafa;
    }
    /* Estilo de tarjeta */
    .card {
        background: linear-gradient(145deg, #1e222b, #15171c);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        border: 1px solid #2c303a;
    }
    .card h1 {
        color: #00f5d4;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Datos de ejemplo de Plotly
df = px.data.gapminder().query("year == 2007")

# Contenedor tipo tarjeta
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("<h1>🌍 Dashboard interactivo con estilo tech</h1>", unsafe_allow_html=True)

# Filtro
continente = st.selectbox("🌎 Selecciona un continente", df["continent"].unique())

# Filtrar datos
df_filtrado = df[df["continent"] == continente]

# Crear gráfico
fig = px.scatter(
    df_filtrado,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="country"
)

# Personalizar tooltip
fig.update_traces(
    hovertemplate="<b>País:</b> %{customdata[0]}<br>" +
                  "<b>PIB per cápita:</b> %{x}<br>" +
                  "<b>Esperanza de vida:</b> %{y}<br>" +
                  "<b>Población:</b> %{marker.size}<extra></extra>",
    customdata=df_filtrado[["country"]]
)

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

