int ledPinGreen = 4;
int ledPinYellow = 3;
int ledPinRed = 2;
int pedG = 6;
int pedR = 5;


void setup() {
  // put your setup code here, to run once:
  pinMode(ledPinGreen, OUTPUT);
  pinMode(ledPinRed, OUTPUT);
  pinMode(ledPinYellow, OUTPUT);
  pinMode(pedR, OUTPUT);
  pinMode(pedG, OUTPUT);
}


void loop() {
  // put your main code here, to run repeatedly:

  // GREEN LIGHT
  digitalWrite(ledPinRed, LOW);
  digitalWrite(ledPinGreen, HIGH);
  delay(2000);
  digitalWrite(ledPinGreen, LOW);

  // YELLOW LIGHT
  digitalWrite(ledPinYellow, HIGH);
  delay(1000);
  digitalWrite(ledPinYellow, LOW);

  // RED LIGHT
  digitalWrite(ledPinRed, HIGH);
  delay(500);


// PEDESTRIAN LIGHTS
  digitalWrite(pedG,HIGH);
  digitalWrite(pedR,LOW);
  delay(1000);
  digitalWrite(pedG,LOW);
// red flash
  int flashes = 5;
  //tone(10, 0);
  //digitalWrite(pedG,HIGH);
  for(int i=0; i<flashes; i++)
  {
    digitalWrite(pedR, HIGH);
    delay(500);
    digitalWrite(pedR, LOW);
    delay(500);
  }
  digitalWrite(pedR, HIGH);
 }
  
