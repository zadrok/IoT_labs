float tempMultiplier;

float temp;
bool fanStatus;
float threshold;

void setup() {
  Serial.begin(9600);
  tempMultiplier = 0.48828125;
  temp = 0.0;
  fanStatus = false;
  threshold = 20.0;
}

void loop() {
  temp = analogRead(A0);
  temp = temp * tempMultiplier;

  msg = "temp:" + String(temp) + ", fanStatus:" + String(fanStatus) + ", threshold:" + String(threshold);
  Serial.println(msg);

  delay(1000);
}
