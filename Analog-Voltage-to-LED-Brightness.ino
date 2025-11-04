/*
  ReadAnalogVoltage

  Reads an analog input on pin 0, converts it to voltage, and prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://docs.arduino.cc/built-in-examples/basics/ReadAnalogVoltage/
*/

const int analogInPin = A0; // Analog input pin for potentiometer
const int pwmPin = 9;       // PWM output pin for LED (must have '~')

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 115200 bits per second:
  Serial.begin(115200);

  // // initialize digital pin LED_BUILTIN as an output.
  // pinMode(LED_BUILTIN, OUTPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  // Read the analog voltage from the potentiometer (0-1023)
  int sensorValue = analogRead(analogInPin);

  // Map the 0-1023 value to the 0-255 PWM range
  int brightness = map(sensorValue, 0, 1023, 0, 255);

  analogWrite(pwmPin, brightness);

  // Optional: Print values to the Serial Monitor for debugging
  // Serial.print("Analog sensor value (0-1023): ");
  // Serial.print(sensorValue);
  // Serial.print(", LED Brightness (0-255): ");
  // Serial.println(brightness);

  delay(1); // Small delay for stability
}
