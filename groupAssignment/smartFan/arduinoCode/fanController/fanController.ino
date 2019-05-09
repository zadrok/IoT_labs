float tempMultiplier;

float temp;
bool fanStatus;
float threshold;

float relayPin = 3;
int relayState = LOW;

void setup() {
  Serial.begin(9600);
  tempMultiplier = 0.48828125;
  temp = 0.0;
  fanStatus = false;
  threshold = 27.0;
  pinMode(relayPin, OUTPUT);
}

void loop() {
  temp = analogRead(A0);
  temp = temp * tempMultiplier;

  String msg = "temp:" + String(temp) + ", fanStatus:" + String(fanStatus) + ", threshold:" + String(threshold);
  Serial.println(msg);

  if (Serial.available() > 0)
  {
    String data = Serial.readString();
  // Serial.println(data);
    threshold = data.toFloat();
  }

  // fan
  if (temp < threshold)
  {
    // Serial.println("Switching FAN off");
    fanStatus = false;
    relayState = HIGH;
  }
  else
  {
    // Serial.println("Switching FAN on");
    fanStatus = true;
    relayState = LOW;
  }
  digitalWrite(relayPin, relayState);

  delay(1000);
}
