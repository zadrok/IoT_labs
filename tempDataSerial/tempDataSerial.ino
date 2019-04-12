int tempPin = A0;
float val;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  val = analogRead(tempPin);
  float celVal = (val/1024.0)*500;
//  Serial.write( celVal );
  Serial.print( celVal );
  Serial.println();
  delay(1000);
}
