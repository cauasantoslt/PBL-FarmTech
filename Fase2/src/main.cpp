// FarmTech Solutions — Fase 2 (ESP32 + Wokwi)
// Cultura: Tomate | Regras: Umidade <60 liga / >70 desliga, pH 6.0–6.8.

#include <Arduino.h>
#include "DHT.h"

// ===== Pinos de Conexão =====
const uint8_t PIN_LDR   = 34; // ADC (pH simulado)
const uint8_t PIN_DHT   = 22; // DHT22 (umidade)
const uint8_t PIN_RELAY = 23; // Relé (bomba)
const uint8_t PIN_N     = 18; // Botão Nitrogênio
const uint8_t PIN_P     = 19; // Botão Fósforo
const uint8_t PIN_K     = 21; // Botão Potássio

// ===== Configuração dos Sensores =====
#define DHTTYPE DHT22
DHT dht(PIN_DHT, DHTTYPE);

// ===== Parâmetros da Lógica de Irrigação =====
const float PH_MIN = 6.0;
const float PH_MAX = 6.8;
const float HUM_ON = 60.0; // Liga a bomba quando a umidade é MENOR que 60%
const float HUM_OFF = 70.0; // Desliga a bomba quando a umidade é MAIOR que 70%
const bool RELAY_ACTIVE_LOW = true; // Módulo relé ativa com sinal LOW

// ===== Variáveis de Estado do Sistema =====
bool pumpOn = false;

// ===== Funções Auxiliares =====
bool isPhOk(float ph) {
  return (ph >= PH_MIN && ph <= PH_MAX);
}

void setRelay(bool on) {
  if (RELAY_ACTIVE_LOW) {
    digitalWrite(PIN_RELAY, on ? LOW : HIGH); // Lógica invertida para o relé
  } else {
    digitalWrite(PIN_RELAY, on ? HIGH : LOW);
  }
  pumpOn = on;
}

float readPH() {
  int adcValue = analogRead(PIN_LDR);
  float ph = (adcValue / 4095.0f) * 14.0f; // Mapeia a leitura do ADC (0-4095) para a escala de pH (0-14)
  return ph;
}

float readHumidity() {
  float h = dht.readHumidity();
  if (isnan(h)) {
    return -1.0f; // Retorna -1 em caso de erro na leitura
  }
  return h;
}

void printTelemetry(float ph, float hum, bool defN, bool defP, bool defK) {
  Serial.print(F("N=")); Serial.print(defN ? F("DEF") : F("OK"));
  Serial.print(F(" | P=")); Serial.print(defP ? F("DEF") : F("OK"));
  Serial.print(F(" | K=")); Serial.print(defK ? F("DEF") : F("OK"));
  Serial.print(F(" | pH=")); Serial.print(ph, 2);
  Serial.print(F(" | Umid="));
  if (hum < 0) Serial.print(F("FALHA"));
  else Serial.print(hum, 1);
  Serial.print(F("%"));
  Serial.print(F(" | Bomba=")); Serial.println(pumpOn ? F("LIGADA") : F("DESLIGADA"));
}

// ===== Rotinas Principais =====
void setup() {
  Serial.begin(115200);
  delay(200);

  pinMode(PIN_RELAY, OUTPUT);
  setRelay(false);

  // Configura os botões com resistor de pull-up interno
  pinMode(PIN_N, INPUT_PULLUP);
  pinMode(PIN_P, INPUT_PULLUP);
  pinMode(PIN_K, INPUT_PULLUP);

  dht.begin();

  Serial.println(F("== FarmTech Fase 2 | Tomate | ESP32 =="));
}

void loop() {
  // Leitura dos sensores
  // Com INPUT_PULLUP, LOW significa que o botão está pressionado (deficiência)
  bool defN = (digitalRead(PIN_N) == LOW);
  bool defP = (digitalRead(PIN_P) == LOW);
  bool defK = (digitalRead(PIN_K) == LOW);
  float ph = readPH();
  float hum = readHumidity();

  // Lógica de decisão para a irrigação
  bool phOk = isPhOk(ph);

  if (pumpOn) {
    // Condições para DESLIGAR a bomba
    if ((hum >= 0 && hum > HUM_OFF) || !phOk) {
      setRelay(false);
    }
  } else {
    // Condições para LIGAR a bomba
    if ((hum >= 0 && hum < HUM_ON) && phOk) {
      setRelay(true);
    }
  }

  printTelemetry(ph, hum, defN, defP, defK);
  delay(1000);
}