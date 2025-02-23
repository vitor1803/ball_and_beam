#include "Adafruit_VL53L0X.h"
#include "Servo.h"


// Sinais de controle
float sinal_ctrl = 0;
float sinal_ref = 0;
float sinal_measure = 0;

// Timing control
unsigned long millisTask = 0;

// Sensor
Adafruit_VL53L0X lox = Adafruit_VL53L0X();

// Atuador 
Servo myservo; 

void setup() {
  // put your setup code here, to run once:

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  // Setup Serial
  Serial.begin(9600);
  while (! Serial) {}

  // Setup Sensor
  while (!lox.begin()) {};
  lox.startRangeContinuous();

  // Setup Servo
  myservo.attach(9);
  myservo.write(0);

  digitalWrite(LED_BUILTIN, LOW);

}

void loop() {
  if (Serial.available() > 0) sinal_ref = (float) Serial.read();

  if(millis() >= millisTask){
    // Leitura sincrona do sensor
    sinal_measure += 15;
    if (sinal_measure >= 360) sinal_measure = 0;

    // Controle
    sinal_ctrl = map(sin(radians(sinal_measure))*100, -100, 100, 0, 179);

    // Ativacao do motor
    myservo.write(sinal_ctrl);

    // Tratamento de dados
    int t = (int)sinal_measure;
    int x = (int)sinal_ctrl;
    int y = (int)sinal_ref;
    Serial.write((byte*)&t, sizeof(t));
    Serial.write((byte*)&x, sizeof(x));
    Serial.write((byte*)&y, sizeof(y));

    // Necessary auxiliar methods
    millisTask = millisTask + 1000UL;
  }
}

