#include <DHT.h>

// === Pines ===
const int pinLM35 = A0;
const int pinDHT = 2;
const int pinTrig = 3;
const int pinEcho = 4;

// === DHT11 ===
#define DHTTYPE DHT11
DHT dht(pinDHT, DHTTYPE);

// === Setup ===
void setup() {
  Serial.begin(9600);
  dht.begin();

  pinMode(pinTrig, OUTPUT);
  pinMode(pinEcho, INPUT);
  Serial.println("Iniciando mediciones...");
}

// === Loop ===
void loop() {
  // === LM35 ===
  int valLM35 = analogRead(pinLM35);
  float tempLM35 = valLM35 * (5.0 / 1023.0) * 100.0;

  // === DHT11 ===
  float tempDHT = dht.readTemperature();
  float humDHT = dht.readHumidity();

  // === HC-SR04 ===
  digitalWrite(pinTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);
  long duracion = pulseIn(pinEcho, HIGH);
  float distancia = duracion * 0.034 / 2;

  // Filtrar valores fuera de rango o ruidosos
  if (distancia <= 0 || distancia > 400) {
    distancia = 0; // o puedes usar -1 para indicar "sin lectura"
  }

  // === Mostrar resultados en Serial Monitor (en vertical) ===
  Serial.println("---------------");
  Serial.print("LM35 (°C): ");
  Serial.println(tempLM35, 2);

  Serial.print("DHT11 Temp (°C): ");
  Serial.println(tempDHT);

  Serial.print("Humedad (%): ");
  Serial.println(humDHT);

  Serial.print("Distancia (cm): ");
  Serial.println(distancia, 2);

  Serial.println("---------------\n");

  delay(2000); // espera 2 segundos
}






