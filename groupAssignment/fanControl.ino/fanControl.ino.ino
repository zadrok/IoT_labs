//Variables
int buttonPin = 2;
float relayPin = 3;
int relayState = HIGH;
int buttonState = 0;    //current button state
int lastButtonState = LOW;  //record last bounce state
long lastDebounceTime = 0;
long debounceDelay = 50;

void setup() {
  // put your setup code here, to run once:
  pinMode(relayPin, OUTPUT);
  pinMode (buttonPin, INPUT);
  digitalWrite (relayPin, relayState);  //configure the initial state of relay
}

void loop() {
  // put your main code here, to run repeatedly:
  int reading = digitalRead(buttonPin);

  if(reading != lastButtonState){
    lastDebounceTime = millis();
  }
  
  if ((millis() - lastDebounceTime) > debounceDelay) {
      if (reading != buttonState) {
        buttonState = reading;
        if (buttonState == HIGH){
          relayState = !relayState;
        }
      }
   }
    digitalWrite(relayPin, relayState);

    lastButtonState = reading;
  }
