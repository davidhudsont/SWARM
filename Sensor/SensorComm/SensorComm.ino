#include <SparkFunCCS811.h>

#define CCS811_ADDR 0x5B //Default I2C Address
//#define CCS811_ADDR 0x5A //Alternate I2C Address

CCS811 myCCS811(CCS811_ADDR);

void setup()
{
    myCCS811.begin(); // Begin communicating with CCS811
    Serial.begin(115200); // Open serial connection to USB Serial port (connect to your computer)
    Serial1.begin(57600); // Open internal serial connection to MT7688 (MPU)
}
void loop()
{
  if (myCCS811.dataAvailable())
  {
    myCCS811.readAlgorithmResults();
    int tempCO2 = myCCS811.getCO2();
    Serial1.println(tempCO2); // Print to MT7688
    Serial.println(1);        // Print to USB Serial
    //int tempVOC = myCCS811.gettVOC();
  }
  else if (myCCS811.checkForStatusError())
  {
    while(1);
  }

  delay(1000); //Wait for next reading
}
