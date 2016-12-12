#include "nRF24L01.h"
#include <RF24_config.h>
#include "RF24.h"
#include <SPI.h>
#include <math.h>
#include <string.h>
const int sampleWindow = 1000;
unsigned int sample;
String location = "basement";
RF24 radio(9,10);
int msg[1];

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(0xE8E8F0F0E1LL);
}

void loop() {
  unsigned long startMillis = millis();
  unsigned int signalMax = 0;
  
  while(millis()-startMillis < sampleWindow){
    sample = analogRead(1);
    if(sample > signalMax){
      signalMax = sample; 
    }
  }
  double voltsMAX = (signalMax * 5.0)/1024;
  double db = 20*log10(voltsMAX/0.775);
  double mult = pow(10, (db/20));
  int dbReading = db * 6;
  
  
  String reading =  "#" + location + ":" + dbReading + "$";
  int length = reading.length();
  msg[0] = 1;
  radio.write(msg,1);
  for(int i = 0; i < length; i++){
    char charToSend[1];
    charToSend[0] = reading.charAt(i);
    radio.write(charToSend,1);
  }
  
  msg[0] = 2;
  radio.write(msg,1);
  radio.powerDown();
  delay(5000);
  radio.powerUp();
}
