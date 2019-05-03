float temp;

float relayPin =3;
int relayState = HIGH;

void setup() {
  Serial.begin(9600);
  temp = analogRead(A0);
  pinMode(relayPin, OUTPUT);
  digitalWrite (relayPin, relayState);

}

//void getTemp(){
  
//}

void loop() {
  // put your main code here, to run repeatedly:
  temp=temp*0.48828125;
  Serial.print("TEMPRETURE: ");
  Serial.print(temp);
  Serial.print("*C\n");

  if (temp < 23.00){
    if(relayState == LOW)
      Serial.println("Switching FAN off");
    relayState = HIGH;
  }
  else{
    if(relayState == HIGH)
      Serial.println("Switching FAN on");
    relayState = LOW;
  }
  digitalWrite(relayPin, relayState);

  Serial.println();
  
}
