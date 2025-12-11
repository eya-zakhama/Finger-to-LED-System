int ledPins[5] = { 3, 5, 6, 9, 10 };  // PWM pins
String controller = "00000";

void setup() {
  Serial.begin(9600);
  delay(1000);  // Wait for serial to stabilize
  
  // Initialize all LED pins
  for (int ledPin : ledPins) {
    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, LOW);
  }
  
  // Test sequence
  Serial.println("Arduino Started!");
  for (int ledPin : ledPins) {
    digitalWrite(ledPin, HIGH);
    delay(250);
    digitalWrite(ledPin, LOW);
  }
  
  delay(500);
  Serial.println("Ready to receive finger data...");
}

void loop() {
  // Read serial data from Python
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    
    // Remove all whitespace and carriage returns
    data.replace("\r", "");
    data.replace("\n", "");
    data.trim();
    
    // Validate we got exactly 5 digits
    if (data.length() == 5 && isValidFingerData(data)) {
      controller = data;
      Serial.print("Received: ");
      Serial.println(controller);
      
      // Update LEDs based on finger status
      updateLEDs();
    }
  }
  
  delay(10);
}

// Validate that all characters are '0' or '1'
bool isValidFingerData(String data) {
  for (int i = 0; i < 5; i++) {
    if (data[i] != '0' && data[i] != '1') {
      return false;
    }
  }
  return true;
}

// Update LED pins based on controller string
void updateLEDs() {
  for (int i = 0; i < 5; i++) {
    if (controller[i] == '1') {
      digitalWrite(ledPins[i], HIGH);
    } else {
      digitalWrite(ledPins[i], LOW);
    }
  }
}

