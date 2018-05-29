#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <SparkFunCCS811.h>
#include <ArduinoJson.h>

#define CCS811_ADDR 0x5B //Default I2C Address
/*This sample sketch demonstrates the normal use of a TinyGPS++ (TinyGPSPlus) object.   
It requires the use of SoftwareSerial, and assumes that you have a 9600-baud serial 
GPS device hooked up on pins 9(rx) and 10(tx).*/

/*
 *  Version 1.0 of the Sensor Unit Sketch
 * 
 *  Authors : David Hudson, David Vercillo
 *  
 *  This sketch is designed to read from 2 sensors
 *  the SparkFunCCS811 and the SparkFun GPS module
 *  the data is then sent to the serial port of the
 *  linkit smart duo mpu for further data processing
 *  and data publishing.
 *  
 */

// Serial Configuration
static const int RXPin = 9, TXPin = 10;
static const uint32_t GPSBaud = 9600;

// The TinyGPS++ object
TinyGPSPlus gps;

// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);

// Air Quality Sensor Object
CCS811 myCCS811(CCS811_ADDR);

// Global lat and lon.
double latitude;
double longitude;

void setup(){
  Serial.begin(115200);
  myCCS811.begin();
  ss.begin(GPSBaud);
  pinMode(RXPin, INPUT);
  pinMode(TXPin, OUTPUT);
  Serial1.begin(57600); // Send Data for Linkit  
}

void loop() {
  // This sketch displays information every time a new sentence is correctly encoded.
  while (ss.available() > 0)
    if (gps.encode(ss.read()))
      displayInfo();
  if (millis() > 5000 && gps.charsProcessed() < 10) {
    Serial.println(F("No GPS detected: check wiring."));
    while(true);
  }
}

void displayInfo() {
  if (gps.location.isValid()) {
    Serial.print(F("Location: ")); 
    latitude = gps.location.lat();
    longitude = gps.location.lng();
    Serial.print(gps.location.lat(), 6);
    Serial.print(F(","));
    Serial.print(gps.location.lng(), 6);
    Sensor();
    delay(1000);
  }
  else {
    Serial.print(F("No Satellite Lock"));
    Serial.println();
    latitude = 47.244580;
    longitude = -122.437618;
    Sensor();
    delay(1000);
  }  
  Serial.println();
}
void Sensor() {
if (myCCS811.dataAvailable()) {
    StaticJsonBuffer<200> jsonBuffer;
    JsonObject& root = jsonBuffer.createObject();
    myCCS811.readAlgorithmResults();
    String data="";
    root["co2"] = myCCS811.getCO2();
    root["voc"] = myCCS811.getTVOC();
    root["lat"] = latitude;
    root["lon"] = longitude;
    root.printTo(data); 
    Serial.println(data);
    Serial1.println(data);
  }
  else if ( myCCS811.checkForStatusError() ) {
    while (1) {
      Serial.println(F("Error"));
      Serial1.println(F("Error"));
    }
  }
}
