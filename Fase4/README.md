# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# FarmTech Solutions - Fase 4: Assistente Agrícola Inteligente

<p align="center">
<a href= "">Vídeo de Apresentação no Youtube</a>
</p>

##  Grupo 25

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/amanda-damasceno-martins/">566598 - Amanda Damasceno Martins</a>
- <a href="https://www.linkedin.com/in/cauasantoslt">566599 - Cauã Santos</a>
- <a href="https://www.linkedin.com/in/fabio-baldo-7959a22a/">567851 - Fabio Baldo</a> 
- <a href="https://www.linkedin.com/in/giovanna-gomes-82b993372/">567169 - Giovanna Gomes Oliveira</a> 
- <a href="https://www.linkedin.com/in/roberto-alvares-785059215/">568265 - Roberto Almeida Alvares</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/sabrina-otoni-22525519b/">Sabrina Otoni</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi</a>


## 📜 Descrição

Esta entrega marca a consolidação do projeto FarmTech Solutions, aplicando **Inteligência Artificial (Machine Learning)** sobre os dados agrícolas para gerar previsões e automatizar a tomada de decisão.

O projeto consiste em um **Assistente Agrícola Inteligente** que opera em três camadas:
1.  **Modelo Preditivo (Backend):** Um algoritmo de Regressão (**Random Forest**) treinado para prever a produtividade da safra (ton/ha) com base em 7 variáveis de solo e clima (N, P, K, pH, Temperatura, Umidade e Chuva).
2.  **Lógica de Negócio (Automação):** Algoritmos que analisam as previsões e sugerem ações automáticas de manejo (ex: "Ligar Irrigação", "Aplicar Calcário").
3.  **Dashboard Interativo (Frontend):** Uma interface web desenvolvida em **Streamlit** para visualização de dados e interação com o gestor.

### **Programa "Ir Além":**

Além da entrega obrigatória, implementamos o **Ir Além 1 - Integração de Dados IoT com Banco de Dados**.
* Desenvolvemos um script em Python (`sensor_iot.py`) que simula sensores em campo gerando dados em tempo real.
* Esses dados são enviados automaticamente para o **Banco de Dados Oracle** da FIAP, garantindo a persistência histórica das leituras de produtividade e irrigação.

## 📁 Estrutura de pastas

```sh
└── PBL-FarmTech/
    ├── Fase1
    ├── Fase2
    ├── Fase3
    ├── Fase4
    │   ├── assets
    │   │   └── logo-fiap.png
    │   │   
    │   ├── IrAlem
    │   │   └── Integração dos Dados como o Banco de Dados 
    │   │       ├── script.sql
    │   │       └── sensor_iot.py
    │   │  
    │   ├── app.py
    │   ├── links.txt
    │   ├── modelo_farmtech.pkl
    │   ├── regras_negocio.py 
    │   ├── treinar_modelo.py
    │   └── README.md
    │
    └── README.md
```



## 🔧 Como executar o código

Para rodar o projeto localmente, siga os passos abaixo:

1. Pré-requisitos
Certifique-se de ter o Python instalado e instale as dependências necessárias:

```bash
pip install pandas numpy scikit-learn streamlit joblib matplotlib seaborn oracledb
```
2. Treinar a Inteligência Artificial
Antes de abrir o dashboard, é necessário treinar o modelo e gerar o arquivo .pkl. No terminal, dentro da pasta Fase4, execute:

```bash
python treinar_modelo.py
```
Isso irá gerar o arquivo modelo_farmtech.pkl.

3. Executar o Dashboard (Streamlit)
Com o modelo treinado, inicie a aplicação web:

```bash
streamlit run app.py
```
O navegador abrirá automaticamente com o Assistente Inteligente.

4. Executar o Ir Além (Banco de Dados)
Para testar a ingestão de dados no Oracle:

Abra o arquivo IrAlem/Integração.../sensor_iot.py e insira suas credenciais Oracle.

Execute o script:

```bash
python sensor_iot.py
```

## 🗃 Histórico de lançamentos

* 0.4.0 - 26/11/2025
    * FASE 4: Machine Learning (Regressão), Dashboard Streamlit e Integração IoT/Oracle.
* 0.3.0 - 12/11/2025
    * FASE 3: Banco de Dados Estruturado (CDS)
* 0.2.0 - 15/10/2025
    * FASE 2: IoT e Automação Inteligente (AICSS)
* 0.1.0 - 19/09/2025
    * FASE 1: Base de Dados Inicial (Python)

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


