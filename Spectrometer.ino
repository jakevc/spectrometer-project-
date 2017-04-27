/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO 
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino model, check
  the Technical Specs of your board  at https://www.arduino.cc/en/Main/Products
  
  This example code is in the public domain.

  modified 8 May 2014
  by Scott Fitzgerald
  
  modified 2 Sep 2016
  by Arturo Guadalupi
  
  modified 8 Sep 2016
  by Colby Newman
*/
const int ledR = 2; // can control red LED from pin 2 
const int ledG = 3; // can control green LED from pin 3 

 // a variable to read incoming serial data into
int incomingByte; 

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin ledG, ledR as outputs.
  Serial.begin(9600); // initialize serial communication at 9600 bits per second baudrate:
  pinMode(ledG, OUTPUT);
  pinMode(ledR, OUTPUT);
}

// the loop function can be controlled with bytewise input through serial port
void loop() {
//int sensorValue = analogRead(A0); // read the input on analog pin 0:

  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer
    incomingByte = Serial.read();
    
    // if it's a capital R turn on the red LED
    if (incomingByte == 'R') {
      digitalWrite(ledR, LOW);
    }
     // if it's a capital G turn on the green LED 
     if (incomingByte == 'G') {
      digitalWrite(ledG, LOW);
     }
    
    // if it's an F turn off any LED that is on
    if (incomingByte == 'F') {
      digitalWrite(ledG, HIGH);
      digitalWrite(ledR, HIGH);
    }
    
     // if it's a capital M, print the value of the sensor
    if (incomingByte == 'M') {
      int sensorValue = analogRead(A0); // read the input on analog pin 0:
      Serial.println(sensorValue); // print out the value you read
    
    }
  }
}
