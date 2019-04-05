int ledPinGreen = 7;
int ledPinYellow = 6;
int ledPinRed = 5;
int pedG = 6;
int pedR = 5;
int buttonA = 2;
int incomingByte = 0;
bool mode = true;


void setup() {
  // put your setup code here, to run once:
  pinMode(ledPinGreen, OUTPUT);
  pinMode(ledPinRed, OUTPUT);
  pinMode(ledPinYellow, OUTPUT);
  pinMode(pedR, OUTPUT);
  pinMode(pedG, OUTPUT);
  pinMode(buttonA, INPUT);
  Serial.begin(9600); 
}

void normal_mode()
{
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

void flash_mode()
{
    digitalWrite(ledPinYellow, HIGH);
    delay(250);
    digitalWrite(ledPinYellow, LOW);
    delay(250);
}

void loop() {
  // put your main code here, to run repeatedly:
 
  if (mode)
  {
    normal_mode();
  }
  else
  {
    flash_mode();
  }
  // send data only when you receive data:
        if (Serial.available() > 0) 
        {
                // read the incoming byte:
                incomingByte = Serial.read();
                if (incomingByte)
                {
                  mode = false;
                }

//                // say what you got:
//                Serial.print("I received: ");
//                Serial.println(incomingByte, DEC);
        }

  // send to pi
   Serial.write(45);
   

 }
  
