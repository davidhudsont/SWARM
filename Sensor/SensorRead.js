
const mraa = require('mraa'); 
console.log('MRAA Version: '+mraa.getVersion());
var i2cDevice = new mraa.I2c(0,false);

i2cDevice.address(0x5A);

for (int i=0; i<20; i++) {
	var C02 = i2cDevice.read(0x02,2);
	console.log('C02: %d\n',C02);
	sleep(200);
}
