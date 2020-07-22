/* Code to turn the RGB components of an RGB LED on or off depending on received serial commands. Modified from Arduino examples. */

int incomingByte; // variable to read serial data into

int redPin = 12;
int greenPin = 8;
int bluePin = 11;

#define COMMON_ANODE // uncomment this line if using a common anode

void setup() {
  
  // initialize serial communication
  Serial.begin(9600);

  // set LED pins as outputs
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT); 

  setColor(0, 0, 255);  // initialize to blue
}

void loop() {
  
  // check if there's incoming data
  if (Serial.available() > 0) {

    // read the oldest byte in the buffer:
    incomingByte = Serial.read();

    if (incomingByte == 'G') {
      setColor(0, 255, 0);  // green
    }
    
    if (incomingByte == 'R') {
      setColor(255, 0, 0);  // red
    }
    
    if (incomingByte == 'B') {
      setColor(0, 0, 255);  // blue
    }
  }
}

/* Function to set the color of the LED*/
void setColor(int red, int green, int blue)
{
  #ifdef COMMON_ANODE // if the LED has a common anode we must drive the pins to GND to create the voltage difference that lights it up
    red = 255 - red;
    green = 255 - green;
    blue = 255 - blue;
  #endif
  
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);  
}
