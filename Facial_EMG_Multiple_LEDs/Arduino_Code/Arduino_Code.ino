/* Code to turn the LEDS on or off depending on received serial commands. Modified from Arduino examples. */

int incomingByte; // variable to read serial data into

int redPin = 12;
int yellowPin = 8;
int bluePin = 11;

void setup() {
  
  // initialize serial communication
  Serial.begin(9600);

  // set LED pins as outputs
  pinMode(redPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(bluePin, OUTPUT); 

  digitalWrite(bluePin, HIGH);  // initialize to blue
}

void loop() {
  
  // check if there's incoming data
  if (Serial.available() > 0) {

    // read the oldest byte in the buffer:
    incomingByte = Serial.read();

    if (incomingByte == 'Y') {
      digitalWrite(yellowPin, HIGH);  // yellow
      digitalWrite(redPin, LOW);
      digitalWrite(bluePin, LOW);
    }
    
    if (incomingByte == 'R') {
      digitalWrite(redPin, HIGH); // red
      digitalWrite(bluePin, LOW); 
      digitalWrite(yellowPin, LOW); 
    }
    
    if (incomingByte == 'B') {
      digitalWrite(bluePin, HIGH); // blue
      digitalWrite(redPin, LOW); 
      digitalWrite(yellowPin, LOW); 
    }
  }
}
