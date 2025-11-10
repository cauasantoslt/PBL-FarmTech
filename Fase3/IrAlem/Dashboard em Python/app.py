import streamlit as st
import pandas as pd
import numpy as np
import requests
import datetime
import random
import math
import schedule
import threading
import time

st.set_page_config(page_title="Dashboard Irrigação", layout="wide")

# -------------------------
# Dados e estado compartilhado
# -------------------------
CURRENT_STATE = {}  # dicionário usado pelo agendador em background

# -------------------------
# Funções simples
# -------------------------
def gerar_dados(horas=48):
    """Gera dados de exemplo para testar o dashboard."""
    agora = datetime.datetime.now()
    tempos = [agora - datetime.timedelta(hours=i) for i in reversed(range(horas))]
    umidade = np.clip(np.random.normal(35, 8, horas), 5, 95)
    P = np.clip(np.random.normal(20, 5, horas), 1, 100)
    K = np.clip(np.random.normal(30, 7, horas), 1, 120)
    ph = np.clip(np.random.normal(6.5, 0.4, horas), 3.5, 9.0)
    df = pd.DataFrame({"hora": tempos, "umidade": umidade, "P": P, "K": K, "pH": ph})
    return df

def simular_sensor_umidade(base=35):
    """Simula uma leitura de sensor de umidade com padrão dia/noite."""
    now = datetime.datetime.now()
    hour = now.hour
    diurnal = 6 * math.cos((hour / 24.0) * 2 * math.pi)  # sobe à noite, cai de dia
    evap = random.uniform(0, 4)  # evaporação
    ruido = random.normalvariate(0, 1.2)
    valor = base - evap + diurnal + ruido
    valor = max(0.0, min(100.0, valor))
    return round(valor, 1)

def buscar_clima(api_key, cidade, pais_codigo):
    """Busca clima real via OpenWeatherMap (geocoding + onecall).
       Se não tiver chave ou der erro, retorna clima simulado."""
    def simulado():
        return {"temp": round(random.uniform(16, 32), 1),
                "chuva": random.randint(0, 80),
                "hum": random.randint(30, 90)}
    if not api_key or not cidade:
        return simulado()
    try:
        q = cidade + ("," + pais_codigo if pais_codigo else "")
        geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        geo_res = requests.get(geo_url, params={"q": q, "limit": 1, "appid": api_key}, timeout=6)
        geo_res.raise_for_status()
        geo = geo_res.json()
        if not geo:
            return simulado()
        lat = geo[0]["lat"]; lon = geo[0]["lon"]
        one_url = "https://api.openweathermap.org/data/2.5/onecall"
        one_res = requests.get(one_url, params={
            "lat": lat, "lon": lon, "exclude": "minutely,hourly,alerts",
            "units": "metric", "appid": api_key
        }, timeout=6)
        one_res.raise_for_status()
        data = one_res.json()
        current = data.get("current", {})
        daily = data.get("daily", [{}])[0]
        weather = {
            "temp": current.get("temp"),
            "chuva": int(daily.get("pop", 0) * 100),
            "hum": current.get("humidity")
        }
        return weather
    except Exception:
        return simulado()

# Targets padrão para milho e trigo (faixas ideais)
CROP_TARGETS = {
    "milho": {"umidade": (45, 65), "pH": (5.8, 7.0), "P": (20, 40), "K": (30, 50)},
    "trigo": {"umidade": (35, 55), "pH": (6.0, 7.5), "P": (18, 35), "K": (25, 45)}
}

def status_cultura(nome, umidade, pH, P, K, targets):
    """Gera uma frase curta com o status da cultura comparando com targets."""
    t = targets[nome]
    msgs = []
    if umidade < t["umidade"][0]:
        msgs.append("umidade baixa")
    elif umidade > t["umidade"][1]:
        msgs.append("umidade alta")
    else:
        msgs.append("umidade OK")
    if pH < t["pH"][0] or pH > t["pH"][1]:
        msgs.append("pH fora do ideal")
    else:
        msgs.append("pH OK")
    if P < t["P"]["0"]:
        msgs.append("P baixo")
    elif P > t["P"][1]:
        msgs.append("P alto")
    else:
        msgs.append("P OK")
    if K < t["K"][0]:
        msgs.append("K baixo")
    elif K > t["K"][1]:
        msgs.append("K alto")
    else:
        msgs.append("K OK")
    return f"{nome.capitalize()}: " + "; ".join(msgs)

def sugestoes(clima, umidade, ph, P, K):
    """Regras simples para sugerir irrigação e correções."""
    s = []
    if umidade == 0:
        s.append("Comando manual 0 detectado: irrigação de emergência ligada")
    elif clima["chuva"] > 40:
        s.append("Adiar irrigação: previsão de chuva alta")
    else:
        if umidade < 25:
            s.append("Irrigar agora: solo muito seco")
        elif umidade < 40:
            s.append("Irrigar moderado: umidade baixa")
        else:
            s.append("Não irrigar: umidade ok")
    if clima.get("temp") and clima["temp"] > 30 and clima.get("hum") and clima["hum"] < 40:
        s.append("Aumentar frequência por calor seco")
    if ph < 5.5:
        s.append("Solo ácido: avaliar correção de pH")
    if ph > 7.5:
        s.append("Solo alcalino: avaliar correção de pH")
    if P < 15:
        s.append("P baixo: considerar adubo fosfatado")
    if K < 20:
        s.append("K baixo: considerar adubo potássico")
    return s

def enviar_telegram(bot_token, chat_id, texto):
    """Envia mensagem para Telegram. Retorna True se ok."""
    if not bot_token or not chat_id:
        return False
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        resp = requests.post(url, data={"chat_id": chat_id, "text": texto}, timeout=6)
        return resp.status_code == 200
    except Exception:
        return False

def alerta_diario(bot_token, chat_id, cidade, clima, umidade_val, pH_val, P_val, K_val):
    """Monta e envia o alerta diário para milho e trigo."""
    t1 = status_cultura("milho", umidade_val, pH_val, P_val, K_val, CROP_TARGETS)
    t2 = status_cultura("trigo", umidade_val, pH_val, P_val, K_val, CROP_TARGETS)
    texto = f"Alerta diário ({cidade})\nClima: {clima.get('temp')}°C, chuva {clima.get('chuva')}%\n{t1}\n{t2}"
    enviar_telegram(bot_token, chat_id, texto)

def start_scheduler(bot_token, chat_id, cidade):
    """Inicia agendador que envia alertas às 09:00 e 19:00.
       Usa CURRENT_STATE para pegar valores atuais."""
    if not bot_token or not chat_id:
        return False
    # limpar agendamentos anteriores
    schedule.clear()
    # agendar 09:00 e 19:00
    schedule.every().day.at("09:00").do(lambda: alerta_diario(
        bot_token, chat_id, cidade,
        CURRENT_STATE.get("clima", {"temp": None, "chuva": None}),
        CURRENT_STATE.get("umidade", 0),
        CURRENT_STATE.get("pH", 0),
        CURRENT_STATE.get("P", 0),
        CURRENT_STATE.get("K", 0)
    ))
    schedule.every().day.at("19:00").do(lambda: alerta_diario(
        bot_token, chat_id, cidade,
        CURRENT_STATE.get("clima", {"temp": None, "chuva": None}),
        CURRENT_STATE.get("umidade", 0),
        CURRENT_STATE.get("pH", 0),
        CURRENT_STATE.get("P", 0),
        CURRENT_STATE.get("K", 0)
    ))
    # roda em thread daemon para não bloquear o Streamlit
    def run_scheduler():
        while True:
            try:
                schedule.run_pending()
            except Exception:
                pass
            time.sleep(30)
    t = threading.Thread(target=run_scheduler, daemon=True)
    t.start()
    return True

# -------------------------
# Interface (simples)
# -------------------------
st.title("Dashboard de Irrigação e Qualidade do Solo")
st.write("Versão simples. Escolha cidade, insira chaves se quiser clima real e alertas Telegram.")

# dados de exemplo
df = gerar_dados(48)
ultimo = df.iloc[-1]

# Sidebar: clima e localização
st.sidebar.header("Clima e localização")
api_key = st.sidebar.text_input("OpenWeatherMap API Key (opcional)", type="password")
# mapa simples de países para facilitar
country_map = {"Brasil": "BR", "Portugal": "PT", "Espanha": "ES", "México": "MX", "Estados Unidos": "US"}
country = st.sidebar.selectbox("País", options=list(country_map.keys()))
city = st.sidebar.text_input("Cidade (ex: Santos)", value="Santos")
country_code = country_map.get(country, "")

# Sidebar: Telegram
st.sidebar.header("Alertas Telegram")
telegram_token = st.sidebar.text_input("Telegram Bot Token (opcional)", type="password")
telegram_chat = st.sidebar.text_input("Telegram Chat ID (opcional)")

# Sidebar: valores manuais para P K pH
st.sidebar.header("Valores manuais P K pH")
usar_manual_pkph = st.sidebar.checkbox("Usar valores manuais para P K pH")
if usar_manual_pkph:
    manual_P = st.sidebar.number_input("P (fósforo)", min_value=0.0, max_value=200.0, value=float(round(ultimo["P"],1)), step=0.1)
    manual_K = st.sidebar.number_input("K (potássio)", min_value=0.0, max_value=200.0, value=float(round(ultimo["K"],1)), step=0.1)
    manual_pH = st.sidebar.number_input("pH", min_value=0.0, max_value=14.0, value=float(round(ultimo["pH"],2)), step=0.1)
else:
    manual_P = None; manual_K = None; manual_pH = None

# Sidebar: umidade manual ou sensor
st.sidebar.header("Umidade do solo")
usar_manual_umidade = st.sidebar.checkbox("Usar umidade manual")
if usar_manual_umidade:
    manual_umidade = st.sidebar.number_input("Umidade (%) - digite 0 para emergência", min_value=0.0, max_value=100.0, value=float(round(ultimo["umidade"],1)), step=0.1)
else:
    manual_umidade = None
conferir_sensor = st.sidebar.checkbox("Conferir com sensor (simulação realista)")

# Sidebar: auto controle para manter culturas saudáveis
st.sidebar.header("Controle automático")
auto_control = st.sidebar.checkbox("Ativar controle automático (ajusta valores simulados)")

# Sidebar: ajustar targets (opcional)
st.sidebar.header("Ajustar alvos das culturas (opcional)")
# milho
st.sidebar.subheader("Milho")
m_moist_min, m_moist_max = st.sidebar.slider("Umidade milho (%)", 20, 80, (45, 65), step=1)
m_ph_min, m_ph_max = st.sidebar.slider("pH milho", 4, 9, (6, 7), step=1)
m_P_min, m_P_max = st.sidebar.slider("P milho", 5, 80, (20, 40), step=1)
m_K_min, m_K_max = st.sidebar.slider("K milho", 5, 100, (30, 50), step=1)
# trigo
st.sidebar.subheader("Trigo")
t_moist_min, t_moist_max = st.sidebar.slider("Umidade trigo (%)", 15, 80, (35, 55), step=1)
t_ph_min, t_ph_max = st.sidebar.slider("pH trigo", 4, 9, (6, 7), step=1)
t_P_min, t_P_max = st.sidebar.slider("P trigo", 5, 80, (18, 35), step=1)
t_K_min, t_K_max = st.sidebar.slider("K trigo", 5, 100, (25, 45), step=1)

# atualiza CROP_TARGETS com valores escolhidos
CROP_TARGETS["milho"] = {"umidade": (m_moist_min, m_moist_max), "pH": (m_ph_min, m_ph_max), "P": (m_P_min, m_P_max), "K": (m_K_min, m_K_max)}
CROP_TARGETS["trigo"] = {"umidade": (t_moist_min, t_moist_max), "pH": (t_ph_min, t_ph_max), "P": (t_P_min, t_P_max), "K": (t_K_min, t_K_max)}

# Buscar clima (real ou simulado)
clima = buscar_clima(api_key.strip() or None, city.strip() or None, country_code)

# Decidir valor final de umidade
if usar_manual_umidade and manual_umidade is not None:
    umidade_val = float(manual_umidade)
elif conferir_sensor:
    umidade_val = simular_sensor_umidade(base=float(round(ultimo["umidade"],1)))
else:
    umidade_val = float(round(ultimo["umidade"],1))

# Se usuário digitou 0, obedecer comando e ligar irrigação
if usar_manual_umidade and manual_umidade == 0.0:
    if "irrigation_on" not in st.session_state:
        st.session_state.irrigation_on = True
    else:
        st.session_state.irrigation_on = True
    st.sidebar.warning("Comando recebido: umidade 0 -> irrigação ligada")

# Estado da irrigação (persistente na sessão)
if "irrigation_on" not in st.session_state:
    st.session_state.irrigation_on = False

# Botão manual ligar/desligar
if st.button("Ligar/Desligar Irrigação"):
    st.session_state.irrigation_on = not st.session_state.irrigation_on

# Controle automático simples: tenta manter milho e trigo nas faixas
P_val = manual_P if usar_manual_pkph else float(round(ultimo["P"],1))
K_val = manual_K if usar_manual_pkph else float(round(ultimo["K"],1))
pH_val = manual_pH if usar_manual_pkph else float(round(ultimo["pH"],2))

if auto_control:
    # se umidade abaixo do mínimo de qualquer cultura, liga irrigação
    min_needed = min(CROP_TARGETS["milho"]["umidade"][0], CROP_TARGETS["trigo"]["umidade"][0])
    max_allowed = max(CROP_TARGETS["milho"]["umidade"][1], CROP_TARGETS["trigo"]["umidade"][1])
    if umidade_val < min_needed:
        st.session_state.irrigation_on = True
    elif umidade_val > max_allowed:
        st.session_state.irrigation_on = False
    # simular efeito da irrigação no valor atual (apenas visual)
    if st.session_state.irrigation_on:
        umidade_val = min(100.0, umidade_val + random.uniform(4.0, 10.0))
    else:
        umidade_val = max(0.0, umidade_val - random.uniform(0.5, 2.5))
    # ajustar P, K, pH lentamente para ficar dentro das faixas (simulação)
    # se P abaixo do mínimo de ambas culturas, aumentar um pouco (simula adubação automática)
    target_P_min = min(CROP_TARGETS["milho"]["P"][0], CROP_TARGETS["trigo"]["P"][0])
    if P_val < target_P_min:
        P_val = min(200.0, P_val + random.uniform(0.5, 2.5))
    target_K_min = min(CROP_TARGETS["milho"]["K"][0], CROP_TARGETS["trigo"]["K"][0])
    if K_val < target_K_min:
        K_val = min(200.0, K_val + random.uniform(0.5, 2.5))
    # pH: mover lentamente em direção à faixa média
    avg_ph_target = ( (CROP_TARGETS["milho"]["pH"][0] + CROP_TARGETS["milho"]["pH"][1]) / 2 +
                      (CROP_TARGETS["trigo"]["pH"][0] + CROP_TARGETS["trigo"]["pH"][1]) / 2 ) / 2
    if abs(pH_val - avg_ph_target) > 0.05:
        pH_val = pH_val + (0.05 if avg_ph_target > pH_val else -0.05)
    # arredonda
    umidade_val = round(float(umidade_val), 1)
    P_val = round(float(P_val), 1)
    K_val = round(float(K_val), 1)
    pH_val = round(float(pH_val), 2)

# Atualiza CURRENT_STATE para o agendador ler
CURRENT_STATE["clima"] = clima
CURRENT_STATE["umidade"] = umidade_val
CURRENT_STATE["pH"] = pH_val
CURRENT_STATE["P"] = P_val
CURRENT_STATE["K"] = K_val

# Mostrar métricas principais
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Umidade do solo", f"{umidade_val:.1f} %")
    st.metric("pH", f"{pH_val:.2f}")
with col2:
    st.metric("Fósforo P", f"{P_val:.1f}")
    st.metric("Potássio K", f"{K_val:.1f}")
with col3:
    st.metric("Local", f"{city}, {country}")
    st.metric("Temp (°C)", f"{clima.get('temp')}")
    st.metric("Prob. chuva (%)", f"{clima.get('chuva')}")

# Mostrar status da irrigação
st.markdown("---")
st.subheader("Status da Irrigação")
if st.session_state.irrigation_on:
    st.success("Irrigação: ATIVA")
else:
    st.info("Irrigação: INATIVA")
st.write("Última leitura:", ultimo["hora"].strftime("%Y-%m-%d %H:%M"))

# Atualizar gráfico com valores atuais (substitui último ponto)
df_plot = df.copy()
df_plot.at[df_plot.index[-1], "umidade"] = umidade_val
df_plot.at[df_plot.index[-1], "P"] = P_val
df_plot.at[df_plot.index[-1], "K"] = K_val
df_plot.at[df_plot.index[-1], "pH"] = pH_val

st.markdown("---")
st.subheader("Gráficos")
st.line_chart(df_plot.set_index("hora")[["umidade", "pH"]])
st.bar_chart(df_plot.set_index("hora")[["P", "K"]])

# Sugestões e status das culturas
st.markdown("---")
st.subheader("Sugestões e status das culturas")
for item in sugestoes(clima, umidade_val, pH_val, P_val, K_val):
    st.write("- " + item)

st.write(status_cultura("milho", umidade_val, pH_val, P_val, K_val, CROP_TARGETS))
st.write(status_cultura("trigo", umidade_val, pH_val, P_val, K_val, CROP_TARGETS))

# -------------------------
# Agendador de alertas Telegram
# -------------------------
# Inicia o agendador automaticamente se token e chat id foram preenchidos e ainda não iniciado
if telegram_token and telegram_chat:
    if "scheduler_started" not in st.session_state or not st.session_state.scheduler_started:
        ok = start_scheduler(telegram_token.strip(), telegram_chat.strip(), city or "local")
        st.session_state.scheduler_started = ok
        if ok:
            st.sidebar.success("Agendador Telegram iniciado (09:00 e 19:00).")
        else:
            st.sidebar.error("Falha ao iniciar agendador Telegram.")
else:
    st.sidebar.info("Para receber alertas, preencha Telegram Bot Token e Chat ID.")

# Se quiser enviar um alerta manual agora (botão)
if st.sidebar.button("Enviar alerta Telegram agora"):
    sent = enviar_telegram(telegram_token.strip(), telegram_chat.strip(),
                           f"Alerta manual ({city})\nClima: {clima.get('temp')}°C, chuva {clima.get('chuva')}%\n"
                           + status_cultura("milho", umidade_val, pH_val, P_val, K_val, CROP_TARGETS)
                           + "\n" + status_cultura("trigo", umidade_val, pH_val, P_val, K_val, CROP_TARGETS))
    if sent:
        st.sidebar.success("Alerta enviado.")
    else:
        st.sidebar.error("Falha ao enviar alerta. Verifique token/chat id.")

# -------------------------
# Instruções simples
# -------------------------
st.markdown("---")
st.subheader("Como usar (passo a passo simples)")
st.write("- Salve este arquivo como **dashboard.py**.")
st.write("- Instale dependências: `pip install streamlit pandas numpy requests schedule`.")
st.write("- Rode: `streamlit run dashboard.py`.")
st.write("- Na barra lateral você pode: escolher cidade, colocar OpenWeatherMap API Key (opcional),")
st.write("  preencher Telegram Bot Token e Chat ID para receber alertas às 09:00 e 19:00.")
st.write("- Use **Usar valores manuais** para P K pH ou **Usar umidade manual** para forçar umidade.")
st.write("- Digite **0** na umidade para comando de emergência: o sistema liga a irrigação automaticamente.")
st.write("- Ative **Controle automático** para que o dashboard simule ações que mantêm milho e trigo nas faixas saudáveis.")