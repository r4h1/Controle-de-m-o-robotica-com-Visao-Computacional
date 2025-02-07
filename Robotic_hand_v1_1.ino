#define NUM_LEDS 5  // Number of LEDs
int ledPins[NUM_LEDS] = {3, 5, 6, 8, 9};  // Define the LED pins

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < NUM_LEDS; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available() > 0) {  // Check for serial communication
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.startsWith("ON")) {
      int ledIndex = command.substring(2).toInt();
      // Check if ledIndex is valid and within bounds
      if (ledIndex >= 0 && ledIndex < NUM_LEDS) {
        digitalWrite(ledPins[ledIndex], HIGH);
        Serial.print("LED ");
        Serial.print(ledIndex + 1);
        Serial.println(" turned ON");
      } else {
        Serial.println("Invalid LED index");
      }
    } 
    else if (command.startsWith("OFF")) {
      int ledIndex = command.substring(3).toInt();
      // Check if ledIndex is valid and within bounds
      if (ledIndex >= 0 && ledIndex < NUM_LEDS) {
        digitalWrite(ledPins[ledIndex], LOW);
        Serial.print("LED ");
        Serial.print(ledIndex + 1);
        Serial.println(" turned OFF");
      } else {
        Serial.println("Invalid LED index");
      }
    }
  }
}
