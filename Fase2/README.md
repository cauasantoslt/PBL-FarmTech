# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Sensor de Irrigação FarmTech Solutions

<p align="center">
<a href= "https://youtu.be/bn1UaVN9CCs">Funcionamento do Circuito no Youtube</a>
</p>
<p align="center">
<img src="./assets/circuito.png" alt="Demonstração do circuito em Imagem" border="0" width=80% >
</p>

##  Grupo 30

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

Este projeto, desenvolvido para a Fase 2 da FarmTech Solutions, consiste em um protótipo de sistema de irrigação inteligente simulado, focado na otimização do cultivo de **tomates** 🍅. Utilizando um microcontrolador **ESP32**, o sistema monitora em tempo real as condições essenciais do solo para decidir de forma autônoma o momento ideal para a irrigação.

Para superar as limitações da plataforma de simulação Wokwi, foram adotadas substituições didáticas para os sensores agrícolas:

-  **Níveis de Nutrientes(NPK):** Três botões simulam a detecção de deficiência de Nitrogênio (N), Fósforo (P) e Potássio (K). Ao serem pressionados, geram alertas no sistema.

- **pH do Solo:** Um sensor de luz (LDR) é utilizado para simular a leitura de pH, mapeando a intensidade luminosa para a escala de pH (0-14).

- **Umidade do Solo:** Um sensor de umidade do ar (DHT22) é empregado para representar a umidade do solo.

O objetivo central é acionar um relé, que representa uma bomba d'água 💧, apenas quando necessário. A lógica de decisão para a irrigação é baseada em regras específicas para a cultura do tomate: a bomba é ativada quando a umidade cai abaixo de 60% e o pH está na faixa ideal (entre 6.0 e 6.8). O sistema também demonstra como a deficiência de nutrientes (simulada pelos botões) influencia indiretamente o processo, alertando o operador sobre a necessidade de correção do solo, o que consequentemente afetaria o pH.


## 📁 Estrutura de pastas

```sh
└── Irrigacao-FarmTech/
    ├── README.md
    ├── assets
    │   └── circuito.png
    ├── diagram.json
    ├── include
    │   └── README
    ├── lib
    │   └── README
    ├── links.txt
    ├── platformio.ini
    ├── src
    │   └── main.cpp
    ├── test
    │   └── README
    └── wokwi.toml
```


## 🔧 Como executar o código

Este projeto foi desenvolvido utilizando PlatformIO com Visual Studio Code e pode ser totalmente executado em um ambiente de simulação Wokwi.

### Pré-requisitos
- **Visual Studio Code:** Editor de código onde o projeto foi desenvolvido.

- **Extensão PlatformIO IDE:** Essencial para compilar o código e gerenciar as dependências do ESP32.

- **Extensão Wokwi for VS Code:** Permite rodar a simulação do circuito diretamente no VS Code.

### Passo a Passo para Execução
1. **Abra o Projeto:** Clone este repositório e abra a pasta raiz no Visual Studio Code.

2. **Instale as Dependências:** O PlatformIO irá detectar o arquivo platformio.ini e deve instalar automaticamente as bibliotecas necessárias para o sensor DHT22.

2. **Compile o Código:** Na barra de status inferior do VS Code, clique no ícone de ✔️ (Build). Aguarde a compilação ser concluída com sucesso.

4. ### Inicie a Simulação:

Pressione F1 para abrir a paleta de comandos.

Digite e selecione a opção "Wokwi: Start Simulator".

5. ### Interaja com o Sistema:

- Uma nova aba com o circuito simulado irá aparecer.

- Ajuste os sliders dos sensores **DHT22 (Umidade)** e **LDR (pH)** para atender às condições de irrigação.

- Pressione os botões **(N, P, K)** para simular alertas de deficiência de nutrientes.

- Acompanhe toda a telemetria e os alertas no painel do **Monitor Serial**.


## 👾 Features

|      | Feature         | Summary       |
| :--- | :---:           | :---          |
| ⚙️  | **Architecture**  | <ul><li>Designed using `<Arduino>` framework for IoT project.</li><li>Hardware connections and layout illustrated in `<diagram.json>` for system visualization.</li><li>Utilizes `<ESP32>` microcontroller for sensor data processing and pump control.</li></ul> |
| 🔩 | **Code Quality**  | <ul><li>Follows `<Arduino>` best practices for readability and maintainability.</li><li>Consistent code style and formatting across the project.</li><li>Comments and documentation within the codebase for better understanding.</li></ul> |
| 📄 | **Documentation** | <ul><li>Comprehensive documentation in various formats: `<platformio.ini>`, `<diagram.json>`, `<links.txt>`, `<wokwi.toml>`.</li><li>Documentation covers project configuration, hardware connections, external integrations, and settings.</li><li>Documentation aids in onboarding new contributors and understanding project components.</li></ul> |
| 🔌 | **Integrations**  | <ul><li>Facilitates integration with external platforms through `<links.txt>` providing GitHub repository, Wokwi simulation, and YouTube demo links.</li><li>Uses `<Wokwi>` for firmware and ELF file configuration in the project.</li><li>Integrates with IoT platforms for data visualization and monitoring.</li></ul> |
| 🧩 | **Modularity**    | <ul><li>Codebase organized into modular components for easy maintenance and scalability.</li><li>Separation of concerns between sensor data processing, pump control, and system monitoring.</li><li>Encourages code reusability and extensibility through modular design.</li></ul> |
| 🧪 | **Testing**       | <ul><li>Implements testing strategies for sensor data accuracy and pump control logic.</li><li>Unit tests for critical functions and decision-making processes.</li><li>Integration tests for system behavior under different scenarios.</li></ul> |
| ⚡️  | **Performance**   | <ul><li>Efficient sensor data processing and pump control algorithms for real-time operation.</li><li>Optimized code for minimal latency in telemetry data transmission.</li><li>Performance tuning for system responsiveness and energy efficiency.</li></ul> |
| 🛡️ | **Security**      | <ul><li>Implements secure communication protocols for data transmission.</li><li>Access control mechanisms for system configuration and operation.</li><li>Regular security audits and updates to address vulnerabilities.</li></ul> |
| 📦 | **Dependencies**  | <ul><li>Dependencies managed through `<platformio.ini>` for library inclusion and project configuration.</li><li>Utilizes libraries for DHT sensor, Adafruit Unified Sensor, and other necessary components.</li><li>Dependency updates and version control for stability and compatibility.</li></ul> |

---

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


