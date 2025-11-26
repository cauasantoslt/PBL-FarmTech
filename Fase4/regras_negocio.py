# regras_negocio.py
def sugerir_irrigacao(umidade_solo, chuva_prevista, cultura):
    if umidade_solo < 40 and chuva_prevista < 10:
        return f"⚠️ CRÍTICO: Ligar irrigação (45 min) para {cultura}."
    elif umidade_solo < 60 and chuva_prevista < 20:
        return f"💧 ATENÇÃO: Irrigação leve (20 min) para {cultura}."
    elif chuva_prevista > 50:
        return "🌧️ ALERTA DE CHUVA: Drenagem ativa. Não irrigar."
    else:
        return "✅ IDEAL: Solo com umidade adequada."

def sugerir_fertilizacao(n, p, k):
    sugestoes = []
    if n < 50: sugestoes.append("Ureia (N)")
    if p < 40: sugestoes.append("Fósforo (P)")
    if k < 30: sugestoes.append("Potássio (K)")
    
    if not sugestoes: return "✅ Nutrientes adequados."
    return "🚜 APLICAR: " + " + ".join(sugestoes)

def corrigir_ph(ph):
    if ph < 5.5: return "🧪 SOLO ÁCIDO: Aplicar Calcário."
    if ph > 7.5: return "🧪 SOLO ALCALINO: Aplicar Gesso."
    return "✅ pH Estável."