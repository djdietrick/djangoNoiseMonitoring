#include "nRF24L01.h"
#include <RF24_config.h>
#include "RF24.h"
#include <SPI.h>
#include <string.h>

RF24 radio(9,10);
int msg[1];

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(1, 0xE8E8F0F0E1LL);
  radio.startListening();
}

void loop(){
  if(radio.available()){
    String reading = "";
    radio.read(msg, 1);
    char rec[1];
    rec[0] = msg[0];
    if(msg[0] == 1){
      bool done = false;
      while(!done){
       radio.read(msg, 1);
       rec[0] = msg[0];
       if(msg[0] == 2)
         done = true;
       else
         reading += rec[0]; 
      }
      Serial.println(reading);
    }
  } 
}
