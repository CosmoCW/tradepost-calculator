import streamlit as st
import pandas as pd

# ========== DATOS ==========
tradeposts = ["Riverend", "Margrove", "Orca Bay", "Seabreeze", "Tarmire", 
              "Darzuac", "Gilead", "Glaceforde", "Ravencrest", "Defiance", 
              "Dras Ashar", "Kari Vir"]

# Distancias desde Dras Ashar y Gilead (en km)
distancias_dras_ashar = {
    "Riverend": 1954, "Margrove": 2616, "Orca Bay": 2699, "Seabreeze": 3591, "Tarmire": 1989,
    "Darzuac": 1233, "Gilead": 3679, "Glaceforde": 3380, "Ravencrest": 2013, "Defiance": 2285, "Kari Vir": 0
}

distancias_gilead = {
    "Riverend": 2316, "Margrove": 2185, "Orca Bay": 1068, "Seabreeze": 1300, "Tarmire": 2500,
    "Darzuac": 2681, "Glaceforde": 2151, "Ravencrest": 1666, "Defiance": 2809, "Dras Ashar": 3679, "Kari Vir": 3704
}

# TradePacks e ingredientes
tradepacks = {
    "Aged Meat": {"Beef": 75, "Salt": 10, "Garlic": 208},
    "Bakers basics": {"Milk": 97, "Egg": 240, "Ground Flour": 230},
    "Barbecue Speciality": {"Beef": 68, "Chicken": 26, "Coal": 42, "Honey": 100},
    "Basic Rations": {"Wheat": 316, "Corn": 110, "Apple": 35, "Shank": 25},
    "Berry Basket": {"Strawberry": 200, "Blueberry": 445, "Moonberry": 30, "Sunberry": 100},
    "Bittersweet Delights": {"Cherry": 65, "Ambar Dust": 140, "Green Cap": 180, "Thin Roots": 105},
    "Brined Shank": {"Shank": 70, "Salt": 14, "Pepper": 165},
    "Building Materials": {"Stone": 240, "Small Log": 185, "Hide": 68},
    "Butcher Box": {"Chicken": 38, "Beef": 90, "Shank": 30, "Cheese": 5},
    "Campfire Roast": {"Small Log": 120, "Stone": 220, "Chicken": 68, "Potato": 155},
    "Cavedweller Findings": {"Cobalt Ore": 110, "Stone": 148, "Glowing Spores": 120, "Thorny Roots": 120},
    "Crafting Basics": {"Copper Ore": 140, "Hide": 55, "Small Log": 200},
    "Crisp Produce": {"Apple": 55, "Brocolli": 55, "Pea": 133, "Bean": 133},
    "Dairy Delivery": {"Milk": 80, "Cheese": 22, "Egg": 246},
    "Exotic Fruit": {"Watermelon": 52, "Sunberry": 70, "Moonberry": 62},
    "Fried Chicken": {"Chicken": 75, "Onion": 80, "Garlic": 120, "Ground Flour": 95},
    "Fruit Basket": {"Grape": 136, "Watermelon": 30, "Cherry": 45},
    "General Spices": {"Garlic": 148, "Onion": 105, "Pepper": 118, "Salt": 13},
    "Glaceforde Explorers Kit": {"Wool": 106, "Small Log": 110, "Coal": 100, "Cotton": 20},
    "Juicers Box": {"Apple": 64, "Strawberry": 162, "Cherry": 26, "Banana": 12},
    "Kabbar Omelets": {"Egg": 145, "Cheese": 35, "Pepper": 148},
    "Kindling Kit": {"Small Log": 175, "Coal": 124, "Cotton": 70},
    "Lush Fibers": {"Wool": 110, "Emerald Spores": 300, "Jucy Roots": 285, "Feather": 25},
    "Margrove Ale Ingredients": {"Wheat": 400, "Acorn": 12, "Pumpkin": 45},
    "Moisture Aging": {"Juicy Roots": 400, "Dry Stem": 170, "Shank": 50, "Onion": 43},
    "Necrobane Kit": {"Bloody Bud": 250, "Brightday": 275, "Feather": 48},
    "Noble Delicacies": {"Moonberry": 175, "Acorn": 15, "Pepper": 70},
    "Oceanic Stimulants": {"Fungal Dust": 380, "Pirates Bliss": 290, "Tin Ore": 160},
    "Pickled Vegetables": {"Cabbage": 238, "Carrot": 300, "Salt": 12},
    "Pie Making Kit": {"Apple": 56, "Sunberry": 65, "Cherry": 25, "Ground Flour": 60},
    "Pirates Anesthetic": {"Numbing Thorns": 245, "Pirates Cap": 280, "Juicy Stem": 280},
    "Poisoners Kit": {"Toxic Stem": 120, "Thin Roots": 240, "Hogthorn": 150, "Thorny Roots": 150},
    "Ravencrest Finest Wears": {"Cotton": 125, "Wool": 78, "Hide": 50},
    "Ravencrest Greens": {"Brocolli": 128, "Pea": 112, "Cabbage": 160}
}

# Lista única de ingredientes
all_ingredients = sorted(list(set(ing for pack in tradepacks.values() for ing in pack.keys())))

# ========== FUNCIONES ==========
def calcular_puntuacion(tradepost, porcentaje, referencia, bartering1, bartering2, plunder):
    # Bonificaciones sumadas (5% + 10% + 10% = 25% máximo)
    multiplicador = 1.0 + (0.05 if bartering1 else 0) + (0.10 if bartering2 else 0) + (0.10 if plunder else 0)
    valor_base = 35000 * multiplicador * (porcentaje / 100)
    distancia = distancias_dras_ashar.get(tradepost, 0) if referencia == "Dras Ashar" else distancias_gilead.get(tradepost, 0)
    return valor_base + (distancia * 8.5)

def calcular_coste_tradepack(pack_name, prices):
    return sum(qty * prices.get(ing, 0) for ing, qty in tradepacks[pack_name].items())

# ========== INTERFAZ ==========
st.title("TradeMaster Pro 🚢")
tab1, tab2 = st.tabs(["🏆 Cálculo de Rutas", "💰 Coste de TradePacks"])

with tab1:
    st.header("Optimización de Rutas")
    referencia = st.selectbox("Punto de referencia:", ["Dras Ashar", "Gilead"])
    
    # Bonificaciones
    c1, c2, c3 = st.columns(3)
    with c1: bartering1 = st.checkbox("Bartering 1 (+5%)")
    with c2: bartering2 = st.checkbox("Bartering 2 (+10%)")
    with c3: plunder = st.checkbox("Plunder (+10%)")
    
    # Porcentajes (0-500%)
    st.subheader("Porcentajes por TradePost (0-500%)")
    porcentajes = {tp: st.slider(f"{tp}", 0, 500, 50, key=f"slider_{tp}") for tp in tradeposts}
    
    # Calcular y mostrar resultados
    if st.button("Calcular Rutas Óptimas"):
        puntuaciones = {tp: calcular_puntuacion(tp, porcentajes[tp], referencia, bartering1, bartering2, plunder) for tp in tradeposts}
        resultados = sorted(puntuaciones.items(), key=lambda x: -x[1])
        
        st.success("**Rutas ordenadas (mayor a menor puntuación):**")
        for tp, punt in resultados:
            distancia = distancias_dras_ashar.get(tp, 0) if referencia == "Dras Ashar" else distancias_gilead.get(tp, 0)
            st.write(f"📍 **{tp}**: {punt:,.2f} pts (Distancia: {distancia} km)")

with tab2:
    st.header("Análisis de Costes")
    
    # Input de precios
    st.subheader("Precios de Ingredientes")
    prices = {}
    cols = st.columns(4)
    for i, ing in enumerate(all_ingredients):
        with cols[i % 4]:
            prices[ing] = st.number_input(f"{ing}", min_value=0, value=10, key=f"price_{ing}")
    
    # Calcular costes
    costs = {pack: calcular_coste_tradepack(pack, prices) for pack in tradepacks}
    df = pd.DataFrame(sorted(costs.items(), key=lambda x: x[1]), columns=["TradePack", "Coste Total"])
    
    # Mostrar resultados
    st.subheader("TradePacks por Coste (de menor a mayor)")
    st.dataframe(df, hide_index=True, use_container_width=True)
    
    # Detalle de un tradepack
    selected = st.selectbox("Detalles del TradePack:", list(tradepacks.keys()))
    st.write(f"**Ingredientes para {selected}:**")
    for ing, qty in tradepacks[selected].items():
        st.write(f"- {ing}: {qty} × {prices.get(ing, 0)} = {qty * prices.get(ing, 0)}")
