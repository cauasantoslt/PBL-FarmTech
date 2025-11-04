import requests
import random
import time

api_key = "/api.key"
cidade = "barueri,br"
url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric"

ph_min = 6.0
ph_max = 6.8
hum_on = 60.0
hum_off = 70.0

bomba_ligada = False

def ler_chuva():
    try:
        resposta = requests.get(url)
        dados = resposta.json()
        if "rain" in dados:
            chuva = dados["rain"].get("1h", 0)
        else:
            chuva = 0
    except:
        chuva = 0
    return chuva

def ler_ph():
    return round(random.uniform(5.5, 7.5), 2)

def ler_umidade():
    return round(random.uniform(40, 80), 1)

def decidir_irrigacao(umidade, ph, chuva):
    global bomba_ligada
    ph_ok = ph_min <= ph <= ph_max
    if bomba_ligada:
        if umidade > hum_off or not ph_ok or chuva >= 1.0:
            bomba_ligada = False
    else:
        if umidade < hum_on and ph_ok and chuva < 1.0:
            bomba_ligada = True

print("irrigacao inteligente – integracao python + api publica")

while True:
    umidade = ler_umidade()
    ph = ler_ph()
    chuva = ler_chuva()
    decidir_irrigacao(umidade, ph, chuva)
    print(f"umidade: {umidade:.1f}% | ph: {ph:.2f} | chuva prevista: {chuva:.1f} mm/h | bomba: {'ligada' if bomba_ligada else 'desligada'}")
    time.sleep(5)