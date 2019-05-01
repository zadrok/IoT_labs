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

  String msg = "temp:" + String(temp) + ", fanStatus:" + String(fanStatus) + ", threshold:" + String(threshold);
  Serial.println(msg);

  if (Serial.available() > 0)
  {
    String data = Serial.readString();
    Serial.println(data);
    threshold = data.toFloat();
  }

  delay(1000);
}
