#include "Adafruit_VL53L0X.h"
#include "Servo.h"


// Sinais de controle
float sinal_ctrl = 0;
float sinal_ref = 0;
float sinal_measure = 0;

// Timing control
unsigned long millisTask = 0;

// Timing aux
int num_of_measures = 0;
int servo_aux = 0;

// Sensor
Adafruit_VL53L0X lox = Adafruit_VL53L0X();

// Atuador 
Servo myservo; 
int servo_reference = 65;


// Função de filtro passa-baixa 
float alpha = 0.385870;
float y_prev = 0.0;

float lox_filter(float x) {
    float y = alpha * x + (1 - alpha) * y_prev;
    y_prev = y;
    return y;
}

void setup() {
  // put your setup code here, to run once:

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  // Setup Serial
  Serial.begin(9600);
  while (! Serial) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);

  }

  // Setup Sensor
  while (!lox.begin()) {
    digitalWrite(LED_BUILTIN, HIGH);
  };
  lox.startRangeContinuous();

  // Setup Servo
  myservo.attach(9);
  myservo.write(0);

  digitalWrite(LED_BUILTIN, LOW);

}

void loop() {
  if (Serial.available() > 0) {
    sinal_ref = (float) Serial.read();
  }

  if (lox.isRangeComplete()) { // ((millis() >= (millisTask-5UL)) && (lox.isRangeComplete()))
    // Leitura assincrona do sensor
    sinal_measure = float(lox.readRange());
    sinal_measure = lox_filter(sinal_measure);
  }

  if(millis() >= millisTask){
    // Leitura sincrona do sensor
    servo_aux += 15;
    if (servo_aux >= 360) servo_aux = 0;

    // Controle
    sinal_ctrl = map(sin(radians(servo_aux))*100, -100, 100, -65, 65);

    // Ativacao do motor
    if (sinal_ref) myservo.write(sinal_ctrl + servo_reference);

    // Tratamento de dados
    int t = (int)sinal_measure;
    int x = (int)sinal_ctrl;
    int y = (int)sinal_ref;
    Serial.write((byte*)&t, sizeof(t));
    Serial.write((byte*)&x, sizeof(x));
    Serial.write((byte*)&y, sizeof(y));

    // Necessary auxiliar methods
    millisTask = millisTask + 100UL;
  }
}

