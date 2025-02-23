#include <TimerOne.h>



float sinal_seno = 0;
unsigned long millisTask = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {

  if((millis() >= millisTask)){
    // Serial.print(0); Serial.print(" "); Serial.println(int(sin(n)*100));
    int t = (int)(sin(radians(sinal_seno))*100);
    int x = 0;
    Serial.write((byte*)&t, sizeof(t));
    Serial.write((byte*)&x, sizeof(x));

    sinal_seno += 15;
    millisTask = millisTask + 1000UL;
  }
}

