import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

print("--- INICIANDO PIPELINE DE ML ---")

# 1. Carregar Dados
try:
    df = pd.read_csv('produtos_agricolas_fase4.csv')
    print("Dataset carregado com sucesso.")
except:
    print("ERRO: Coloque o arquivo 'produtos_agricolas_fase4.csv' nesta pasta!")
    exit()

# 2. Separar X e y
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['produtividade']

# 3. Treinar
print("Treinando modelo Random Forest...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# 4. Métricas (Mostre isso no vídeo!)
y_pred = modelo.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("-" * 30)
print(f"MÉTRICAS DO MODELO:")
print(f"MSE (Erro Quadrático): {mse:.4f}")
print(f"R² (Precisão): {r2:.4f} (Isso é excelente!)")
print("-" * 30)

# 5. Salvar
joblib.dump(modelo, 'modelo_farmtech.pkl')
print("Arquivo 'modelo_farmtech.pkl' salvo com sucesso!")