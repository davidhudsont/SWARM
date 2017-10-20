
var arDrone = require('ar-drone');
var client = arDrone.createClient();
var keypress = require('keypress');
var flight_state = false;
// make `process.stdin` begin emitting "keypress" events 
keypress(process.stdin);
 
// listen for the "keypress" event 
process.stdin.on('keypress', function (ch, key) {
  //console.log('got "keypress"', key);
  //console.log('got "key.name"', key.name);
  //client.stop();
  
  //console.log('Stop');
  if (key.name == 'space') {
	  console.log('Stop');
	  client.stop();
  }
  if (key.name == 'w') {
	console.log('Go forward');
	client.front(0.10);
  }
  if (key.name == 'a') {
	console.log('Go left');
	client.left(0.10);
  }
  if (key.name == 'd') {
	console.log('Go right');
	client.right(0.10);
  }
  if (key.name == 's') {
	console.log('Go backwards');
	client.back(0.10)
  }
  if (key.name == 'k') {
	console.log('Go down');
	client.down(0.10);
  }
  if (key.name == 'j') {
	console.log('Go up');
	client.up(0.10);
  }
  if (key.name == "e") {
	console.log('Turn left');
	client.clockwise(0.10);
  }
  if (key.name == 'q') {
	console.log('Turn right');
	client.counterClockwise(0.10)
  }
  if (key.name == 'l') {
	if (flight_state == false) {
		client.takeoff();
		flight_state = true;
		console.log('Lift off flight_state =',flight_state);
	}	
	else {
		client.land();
		flight_state = false;
		console.log('Landing flight_state =',flight_state);
	}
  }
  if (key && key.ctrl && key.name == 'c') {
	if (flight_state == true) {
		client.land();
		flight_state = false;
	}
	console.log('End');
    process.stdin.pause();
  }
  
});

process.stdin.setRawMode(true);
process.stdin.resume();
