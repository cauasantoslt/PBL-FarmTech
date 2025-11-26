# app.py
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from regras_negocio import sugerir_irrigacao, sugerir_fertilizacao, corrigir_ph

st.set_page_config(page_title="FarmTech Fase 4", layout="wide")

# Tentar carregar o modelo
try:
    modelo = joblib.load('modelo_farmtech.pkl')
    modelo_carregado = True
except:
    modelo_carregado = False

# --- HEADER ---
st.title("🚜 FarmTech Solutions: Assistente Agrícola Inteligente")
st.markdown("Monitoramento de Safra e Previsão de Produtividade (Regressão)")

# --- SIDEBAR (INPUTS) ---
st.sidebar.header("📡 Dados do Sensor")
cultura = st.sidebar.selectbox("Cultura", ["Milho", "Soja", "Café", "Trigo"])

st.sidebar.subheader("Nutrientes")
n = st.sidebar.number_input("Nitrogênio (N)", 0, 140, 60)
p = st.sidebar.number_input("Fósforo (P)", 0, 145, 50)
k = st.sidebar.number_input("Potássio (K)", 0, 205, 40)

st.sidebar.subheader("Clima e Solo")
temp = st.sidebar.slider("Temperatura (°C)", 10.0, 40.0, 26.0)
hum = st.sidebar.slider("Umidade (%)", 10.0, 100.0, 55.0)
ph = st.sidebar.slider("pH", 3.0, 9.0, 6.5)
rain = st.sidebar.slider("Chuva (mm)", 0.0, 300.0, 120.0)

# --- CORPO PRINCIPAL ---
if st.sidebar.button("🤖 Gerar Diagnóstico"):
    if modelo_carregado:
        # 1. Previsão
        entrada = pd.DataFrame([[n, p, k, temp, hum, ph, rain]], 
                             columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
        predicao = modelo.predict(entrada)[0]
        
        # 2. Exibição das Métricas
        col1, col2, col3 = st.columns(3)
        col1.metric("Produtividade Estimada", f"{predicao:.2f} ton/ha")
        col2.metric("Status Irrigação", "Monitorando", delta_color="off")
        col3.metric("Clima", f"{temp}°C")
        
        st.divider()
        
        # 3. Sugestões de Manejo (Sua parte!)
        st.subheader("📋 Plano de Ação (IA Generativa)")
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"**Irrigação:** {sugerir_irrigacao(hum, rain, cultura)}")
            st.info(f"**Solo:** {corrigir_ph(ph)}")
        with c2:
            st.warning(f"**Fertilização:** {sugerir_fertilizacao(n, p, k)}")
            
    else:
        st.error("ERRO: Modelo não encontrado. Execute 'treinar_modelo.py' primeiro!")

# --- IR ALÉM 2 (GRÁFICOS) ---
st.divider()
st.subheader("📈 Análise de Tendências (Ir Além 2)")

try:
    df = pd.read_csv('produtos_agricolas_fase4.csv')
    tab1, tab2 = st.tabs(["Dispersão (Scatter)", "Correlação (Heatmap)"])
    
    with tab1:
        st.write("Relação: Chuva vs Produtividade")
        fig, ax = plt.subplots(figsize=(8,4))
        sns.scatterplot(data=df, x='rainfall', y='produtividade', hue='label', alpha=0.6, ax=ax)
        st.pyplot(fig)
        
    with tab2:
        st.write("Mapa de Calor: O que afeta a produtividade?")
        fig2, ax2 = plt.subplots(figsize=(8,4))
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        sns.heatmap(numeric_df.corr()[['produtividade']].sort_values(by='produtividade', ascending=False), 
                    annot=True, cmap='coolwarm', ax=ax2)
        st.pyplot(fig2)

except:
    st.warning("Carregue o CSV para ver os gráficos.")