import oracledb
import time
import random

# --- 1. Configurações de Conexão ---
USER = "RM566599"       
PASSWORD = "200705"   
DSN = "oracle.fiap.com.br/ORCL"

# --- 2. Conectando ---
try:
    print("Conectando ao Oracle...")
    connection = oracledb.connect(user=USER, password=PASSWORD, dsn=DSN)
    cursor = connection.cursor()
    print("Conectado com sucesso!")
except Exception as e:
    print("Erro ao conectar:", e)
    exit()

# --- 3. O Loop Infinito (Simulação IoT) ---
try:
    while True:
        # 3.1 Gerar dados aleatórios para TODAS as colunas
        n = random.randint(0, 100)
        p = random.randint(0, 100)
        k = random.randint(0, 100)
        temp = round(random.uniform(20.0, 35.0), 2)
        umid = round(random.uniform(30.0, 90.0), 2)
        ph = round(random.uniform(4.0, 9.0), 2)
        chuva = round(random.uniform(0.0, 200.0), 2)
        cultura = random.choice(['Milho', 'Soja', 'Trigo', 'Cafe'])
        produtividade = round(random.uniform(2.0, 8.0), 2) # Toneladas
        irrigacao = round(random.uniform(0.0, 50.0), 2)    # Litros
        
        print(f"Enviando: {cultura} | N={n} P={p} K={k} | pH={ph}...")

        # 3.2 O COMANDO SQL (INSERT)
        sql_insert = """
            INSERT INTO FARMTECH_FASE4 
            (n_sensor, p_sensor, k_sensor, temperatura, umidade, ph, chuva, cultura_label, produtividade_estimada, irrigacao_necessaria)
            VALUES 
            (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)
        """
        
        # 3.3 Executar e Salvar (Commit)
        valores = [n, p, k, temp, umid, ph, chuva, cultura, produtividade, irrigacao]
        cursor.execute(sql_insert, valores)
        connection.commit() # <--- O PULO DO GATO! Sem isso, nada é salvo.
        
        print("--> Dados inseridos no Banco com sucesso!")
        time.sleep(5) # Espera 5 segundos

except KeyboardInterrupt:
    print("\nSimulação parada pelo usuário.")
    cursor.close()
    connection.close()