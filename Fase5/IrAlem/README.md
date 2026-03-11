# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# FarmTech Solutions - Fase 5 (Ir Além): Sistema IoT de Coleta de Dados com ESP32

<p align="center">
<a href="LINK_VIDEO_IR_ALEM_AQUI">🤖 Clique aqui para ver o Vídeo Demonstrativo do Sistema IoT funcionando</a>
</p>

## Grupo 10

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/amanda-damasceno-martins/">566598 - Amanda Damasceno Martins</a>
- <a href="https://www.linkedin.com/in/cauasantoslt">566599 - Cauã Santos</a>
- <a href="https://www.linkedin.com/in/fabio-baldo-7959a22a/">567851 - Fabio Baldo</a> 
- <a href="https://www.linkedin.com/in/giovanna-gomes-82b993372/">567169 - Giovanna Gomes Oliveira</a> 


---

## 📜 Sobre o Projeto "Ir Além"

Este subprojeto atende aos requisitos da **Primeira Opção do desafio "Ir Além"**. Desenvolvemos um sistema físico de Internet das Coisas (IoT) focado na coleta de dados em tempo real no campo para enriquecer a base de dados da nossa startup, FarmTech Solutions.

### 🎯 Objetivo e Justificativa Tecnológica
Durante o desenvolvimento dos nossos modelos de Machine Learning (Entrega 1 da Fase 5), comprovamos matematicamente que apenas dados climáticos abertos (chuva e temperatura do ar) não são suficientes para prever o rendimento da safra com precisão. 

Para resolver essa limitação, nossa equipe de engenharia projetou esta estação de monitoramento utilizando um **microcontrolador ESP32**. O objetivo é coletar dados granulares diretamente do solo e do microclima da plantação, enviando-os via Wi-Fi para um dashboard. No futuro, esses dados alimentarão a nossa Inteligência Artificial, fechando a lacuna de informações e aumentando a precisão das nossas previsões.

### 🔌 Sensores Escolhidos
1. **Sensor de Umidade do Solo (Higrômetro):** Crucial para entender a real disponibilidade de água para as raízes, indo além da simples medição de chuva.
2. **Sensor DHT11/DHT22 (Temperatura e Umidade):** Para capturar o microclima exato no nível da folhagem da plantação, que muitas vezes difere das estações meteorológicas regionais.

---

## 🏗️ Arquitetura do Circuito

Abaixo está o diagrama da nossa arquitetura de hardware, demonstrando a ligação do ESP32 com os sensores.

<p align="center">
<img src="../assets/logo-fiap.png" alt="Demonstração do circuito em Imagem" border="0" width=80% >
</p>


---

## 📡 Conectividade e Fluxo de Dados

O código-fonte desenvolvido em **C++** (disponível no arquivo `main.cpp` nesta mesma pasta) realiza as seguintes operações:
1. Faz a leitura analógica e digital dos sensores conectados aos pinos do ESP32.
2. Estabelece conexão com a rede Wi-Fi local.
3. Formata os dados coletados e os publica através de um **Broker MQTT** (ou envia via requisição HTTP para nosso banco de dados), permitindo a visualização remota das condições da fazenda em tempo real.

---

## 🔧 Como testar a simulação

Para reproduzir nosso circuito virtualmente sem precisar do hardware físico:

1. Acesse a plataforma [Wokwi](https://wokwi.com/).
2. Crie um novo projeto com a placa **ESP32**.
3. Copie o código do nosso arquivo `main.cpp` e cole no editor principal do simulador.
4. Adicione os sensores (DHT22 e Potenciômetro simulando a Umidade do Solo) conforme a imagem da nossa arquitetura.
5. Inicie a simulação e observe os dados sendo impressos no terminal Serial e enviados para a nuvem.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>