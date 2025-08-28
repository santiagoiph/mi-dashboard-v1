import streamlit as st
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="🌍 Dashboard Demo", layout="wide")

st.title("🌍 Dashboard interactivo con Streamlit")

# Datos de ejemplo de Plotly
df = px.data.gapminder().query("year == 2007")

# Filtro
continente = st.selectbox("🌎 Selecciona un continente", df["continent"].unique())

# Filtrar datos
df_filtrado = df[df["continent"] == continente]

# Gráfico
fig = px.scatter(df_filtrado, 
                 x="gdpPercap", 
                 y="lifeExp",
                 size="pop", 
                 color="country",
                 hover_name="country", 
                 log_x=True)

st.plotly_chart(fig, use_container_width=True)
