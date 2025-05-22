import streamlit as st

# Definición de los TradePosts
tradeposts = [
    "Riverend", "Margrove", "Orca Bay", "Seabreeze", "Tarmire", 
    "Darzuac", "Gilead", "Glaceforde", "Ravencrest", "Defiance", 
    "Dras Ashar", "Kari Vir"
]

# Distancias desde Dras Ashar y Gilead (en km)
distancias_dras_ashar = {
    "Riverend": 1954,
    "Margrove": 2616,
    "Orca Bay": 2699,
    "Seabreeze": 3591,
    "Tarmire": 1989,
    "Darzuac": 1233,
    "Gilead": 3679,
    "Glaceforde": 3380,
    "Ravencrest": 2013,
    "Defiance": 2285,
    "Kari Vir": 0  # No proporcionada, asumo 0 (ajusta si es necesario)
}

distancias_gilead = {
    "Riverend": 2316,
    "Margrove": 2185,
    "Orca Bay": 1068,
    "Seabreeze": 1300,
    "Tarmire": 2500,
    "Darzuac": 2681,
    "Glaceforde": 2151,
    "Ravencrest": 1666,
    "Defiance": 2809,
    "Dras Ashar": 3679,
    "Kari Vir": 3704
}

# Función para calcular la puntuación total con bonificaciones
def calcular_puntuacion(tradepost, porcentaje, referencia, bartering1, bartering2, plunder):
    base = 35000 * (porcentaje / 100)  # <<< Ahora acepta >100% (ej: 500% = 35k * 5)
    
    # Obtener distancia según referencia
    if referencia == "Dras Ashar":
        distancia = distancias_dras_ashar.get(tradepost, 0)
    else:  # Gilead
        distancia = distancias_gilead.get(tradepost, 0)
    
    puntuacion = base + (distancia * 8.5)
    
    # Aplicar bonificaciones acumulables
    if bartering1:
        puntuacion *= 1.05
    if bartering2:
        puntuacion *= 1.10
    if plunder:
        puntuacion *= 1.10
    
    return puntuacion

# Interfaz de Streamlit
st.title("Calculadora de Puntuación para TradePosts")

st.markdown("""
Esta aplicación calcula la puntuación de cada TradePost basada en:
- **Porcentaje del TradePost** (100% = 35,000 puntos, **hasta 500%**).  # <<< Actualizado
- **Distancia desde Dras Ashar o Gilead** (multiplicada por 8.5).
- **Bonificaciones acumulables**: Bartering 1 (+5%), Bartering 2 (+10%), Plunder (+10%).
""")

# Seleccionar punto de referencia (Dras Ashar o Gilead)
referencia = st.selectbox("Selecciona el punto de referencia:", ["Dras Ashar", "Gilead"])

# Opciones de bonificación
st.header("Bonificaciones")
bartering1 = st.checkbox("Bartering 1 (+5%)")
bartering2 = st.checkbox("Bartering 2 (+10%)")
plunder = st.checkbox("Plunder (+10%)")

# Ingresar porcentajes para cada TradePost (ahora hasta 500%)  <<< Cambio clave
st.header("Ingresar Porcentajes")
porcentajes = {}
for tp in tradeposts:
    porcentajes[tp] = st.number_input(  # <<< Usamos number_input en lugar de slider
        f"Porcentaje para {tp} (0-500%)",
        min_value=0,
        max_value=500,  # <<< Límite aumentado a 500%
        value=50,  # Valor por defecto
        step=1
    )

# Calcular puntuaciones
puntuaciones = {}
for tp in tradeposts:
    puntuaciones[tp] = calcular_puntuacion(
        tp, porcentajes[tp], referencia, bartering1, bartering2, plunder
    )

# Mostrar resultados ordenados
st.header("Resultados")
sorted_puntuaciones = sorted(puntuaciones.items(), key=lambda x: x[1], reverse=True)

st.write(f"Puntuaciones ordenadas (referencia: {referencia}):")
for tp, punt in sorted_puntuaciones:
    distancia = distancias_dras_ashar.get(tp, 0) if referencia == "Dras Ashar" else distancias_gilead.get(tp, 0)
    st.write(
        f"- **{tp}**: {punt:.2f} puntos "
        f"(Porcentaje: {porcentajes[tp]}%, "
        f"Distancia a {referencia}: {distancia} km)"
    )
