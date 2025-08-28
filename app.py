import streamlit as st
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="🌍 Dashboard Demo", layout="wide")

st.title("🌍 Dashboard interactivo con tooltips personalizados")

# Datos de ejemplo de Plotly
df = px.data.gapminder().query("year == 2007")

# Filtro
continente = st.selectbox("🌎 Selecciona un continente", df["continent"].unique())

# Filtrar datos
df_filtrado = df[df["continent"] == continente]

# Crear gráfico con Plotly
fig = px.scatter(
    df_filtrado, 
    x="gdpPercap", 
    y="lifeExp", 
    size="pop", 
    color="country"
)

# Personalizar tooltips en español
fig.update_traces(
    hovertemplate="<b>País:</b> %{customdata[0]}<br>" +
                  "<b>PIB per cápita:</b> %{x}<br>" +
                  "<b>Esperanza de vida:</b> %{y}<br>" +
                  "<b>Población:</b> %{marker.size}<extra></extra>",
    customdata=df_filtrado[["country"]]  # datos extra para usar en tooltip
)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)

