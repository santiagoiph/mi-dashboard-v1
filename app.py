# ... tu código para crear df_filtrado y la figura ...
fig = px.scatter(
    df_filtrado,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="country"
)

# Tooltip en español y sin info extra (cuadro <extra> oculto)
fig.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "PIB per cápita: %{x:,.0f}<br>"
        "Esperanza de vida: %{y:.1f}<br>"
        "Población: %{marker.size:,}"
        "<extra></extra>"
    ),
    customdata=df_filtrado[["country"]]
)

# Estilo base del tooltip (fondo claro, borde neutro, texto oscuro)
fig.update_layout(
    hoverlabel=dict(
        bgcolor="rgba(255,255,255,0.98)",
        bordercolor="#e5e7eb",
        font_color="#111111",
        font_size=13
    )
)

# CSS para esquinas redondeadas (y mantenerlo limpio)
st.markdown("""
<style>
/* Fondo claro + borde sutil + esquinas redondeadas del tooltip */
.hoverlayer .hovertext .bg {
    fill: #ffffff !important;      /* fondo claro */
    stroke: #e5e7eb !important;    /* sin celeste: gris muy sutil */
    stroke-width: 1 !important;
    rx: 10;
    ry: 10;
}
/* Texto del tooltip en color oscuro */
.hoverlayer .hovertext text {
    fill: #111111 !important;
}
</style>
""", unsafe_allow_html=True)

st.plotly_chart(fig, use_container_width=True)

