#define NUM_LEDS 5  // Numero de LEDs
int ledPins[NUM_LEDS] = {3, 5, 6, 8, 9};  // Define os Pinos dos LEDS

void setup() {
  Serial.begin(9600);
  for (int i = 0; i <= NUM_LEDS; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available() > 0) {                     // Checa a comunicação serial
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.startsWith("ON")) {
      int ledIndex = command.substring(2).toInt();
      if (ledIndex >= 0 && ledIndex < NUM_LEDS) {
        digitalWrite(ledPins[ledIndex], HIGH);
        Serial.print("LED ");
        Serial.print(ledIndex + 1);
        Serial.println(" turned ON");
      }
    } 
    else if (command.startsWith("OFF")) {
      int ledIndex = command.substring(3).toInt();
      if (ledIndex >= 0 && ledIndex <= NUM_LEDS) {
        digitalWrite(ledPins[ledIndex], LOW);
        Serial.print("LED ");
        Serial.print(ledIndex + 1);
        Serial.println(" turned OFF");
      }
    }
  }
}
