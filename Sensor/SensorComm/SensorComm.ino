#include <SparkFunCCS811.h>

#define CCS811_ADDR 0x5B //Default I2C Address
//#define CCS811_ADDR 0x5A //Alternate I2C Address

CCS811 myCCS811(CCS811_ADDR);

void setup()
{
    myCCS811.begin();
    Serial.begin(115200); // Open up communication between
    Serial1.begin(57600); // Send Data for Linkit
}
void loop()
{
  if (myCCS811.dataAvailable())
  {
    myCCS811.readAlgorithmResults();
    int tempCO2 = myCCS811.getCO2();
    Serial1.println(tempCO2);
    Serial.println(1);
    //int tempVOC = myCCS811.gettVOC();
  }
  else if (myCCS811.checkForStatusError())
  {
    while(1);
  }

  delay(1000); //Wait for next reading
}
