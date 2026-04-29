# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# FarmTech Solutions - Fase 5: Machine Learning e Computação em Nuvem

<p align="center">
<a href="LINK_DO_SEU_VIDEO_DO_PBL_AQUI">🎥 Vídeo 1: Apresentação YOLOv5 e CNN do Zero</a> &nbsp; | &nbsp;
<a href="LINK_DO_SEU_VIDEO_DO_IR_ALEM_AQUI">🤖 Vídeo 2: Projeto Ir Além (Transfer Learning e Segmentação)</a>
</p>

## Grupo 40

## 👨‍🎓 Integrantes: 

- <a href="https://www.linkedin.com/in/cauasantoslt">566599 - Cauã Santos</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/sabrina-otoni-22525519b/">Sabrina Otoni</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi</a>

---

## 📜 Descrição do Projeto

Nesta Fase 6, a **FarmTech Solutions** expande seus horizontes para além dos dados tabulares e entra no mundo da **Visão Computacional**. O objetivo é criar sistemas inteligentes aplicáveis à segurança patrimonial, controle de acesso e monitoramento de ativos. O projeto está estruturado em duas entregas principais:

1. **Detecção de Objetos com YOLOv5 (Entrega 1):** Criamos um dataset autoral contendo 80 imagens de dois objetos com características físicas contrastantes (um Limpador e um Boné). As imagens foram rotuladas manualmente e divididas em pastas de treino, validação e teste. Realizamos o treinamento customizado de uma rede **YOLOv5** variando os hiperparâmetros (30 e 60 épocas) para avaliar a evolução do aprendizado, melhora do *Recall* e precisão na detecção das *bounding boxes*.
2. **Comparação de Abordagens (Entrega 2):** Para validar a eficácia da nossa solução, comparamos a performance da YOLO customizada com outras duas abordagens:
   * **YOLOv5 Padrão:** Utilização dos pesos originais (dataset COCO), que se mostrou ineficaz por não conhecer nossas classes específicas.
   * **CNN Treinada do Zero:** Construção de uma Rede Neural Convolucional no Keras/TensorFlow. O modelo atuou como um classificador rápido de imagens (atingindo 100% de acurácia), mas falhou em fornecer o contexto de localização espacial (coordenadas do objeto) que a YOLO entrega.

### 🚀 Programa "Ir Além" (Opção 2)
Implementamos técnicas avançadas de Visão Computacional para avaliar o impacto de grandes redes e do pré-processamento de imagens:
* **Transfer Learning e Fine Tuning:** Utilizamos a arquitetura **MobileNetV2** (pré-treinada na ImageNet), congelando suas camadas iniciais para extração de características e realizando o ajuste fino (*Fine Tuning*) com *learning rate* reduzido.
* **Segmentação de Imagem:** Aplicamos o modelo **YOLOv8-Seg** para gerar máscaras binárias e recortar o background das fotos originais. O experimento revelou comportamentos fascinantes da IA, comprovando a necessidade de treinar segmentadores específicos em vez de depender de soluções genéricas de prateleira.

---

## 📁 Estrutura de pastas

```sh
└── PBL-FarmTech/
    ├── Fase1
    ├── Fase2
    ├── Fase3
    ├── Fase4
    ├── Fase5
    ├── Fase6
    │   ├── assets
    │   │   └── logo-fiap.png
    │   │   
    │   ├── IrAlem
    │   │   └── CauaSantos_rm566599_IrAlem_Fase6.ipynb
    │   │
    │   ├── dataset/
    │   │   ├── images/ (train, val, test)
    │   │   └── labels/ (train, val, test)
    │   │
    │   ├── data.yaml
    │   ├── CauaSantos_rm566599_pbl_fase6.ipynb
    │   └── README.md
    │
    └── README.md
```

### 🔧 Como executar o código
Devido ao alto custo computacional do treinamento de Redes Neurais, a execução deste projeto foi adaptada para rodar em nuvem. Siga os passos abaixo:

1. Preparação dos Dados:
Faça o upload da pasta `dataset` (contendo as imagens e rótulos) e do arquivo de configuração `data.yaml` para o seu Google Drive.

2. Ambiente de Execução (Google Colab):

Abra os arquivos `.ipynb` no Google Colab. Antes de executar qualquer célula, vá em ``Ambiente de Execução > Alterar o tipo de ambiente de execução` e ative a aceleração via *GPU (T4)*.


3. Reproduzir os Treinamentos:

Execute a primeira célula do notebook para montar o disco (`drive.mount('/content/drive')`). Em seguida, rode as células sequencialmente. O notebook está programado para clonar automaticamente os repositórios da Ultralytics e baixar todas as dependências necessárias via `pip install`.


## 🗃 Histórico de lançamentos
* 0.6.0 - 28/04/2026
    * FASE 6: Visão Computacional (YOLOv5, CNN do Zero, Transfer Learning com MobileNetV2 e Segmentação com YOLOv8-Seg).
    
* 0.5.0 - 10/03/2026
    * FASE 5: Machine Learning (Clusterização e Regressão) e Planejamento de Custos na Nuvem (AWS).

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
