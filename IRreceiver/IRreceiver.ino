// reference : https://www.pjrc.com/teensy/td_libs_IRremote.html
// Include IR remote Library
#include <IRremote.h>

int IR_pin = 11;
int button_pressed;

// Define IR receive and results objects
IRrecv irrecv(IR_pin);
decode_results results;


void setup() {
  Serial.begin(9600);
  //Enable IR receiver
  irrecv.enableIRIn();

}

void loop() {
  if (irrecv.decode(&results))
  {

    switch(results.value)
    {
      case 0xFD00FF: // Power button 
      Serial.println("Goodbye...");
      // turn off game
      break;
      case 0xFD807F: // Vol+
      Serial.println("This does nothing");
      break;
      case 0xFD40BF: // Func/Stop
      Serial.println("Wrong button!");
      break;
      case 0xFD20DF: // <<
      Serial.println("Wrong button!");
      break;
      case 0xFDA05F: // Play/pause
      Serial.println("Wrong button!");
      break;
      case 0xFD609F: // >>
      Serial.println("Try again!");
      break;
      case 0xFD10EF: // down
      Serial.println("This doesn't do anything");
      break;
      case 0xFD906F: // Vol-
      Serial.println("Keep trying..");
      break;
      case 0xFD50AF: // up
      Serial.println("No");
      break;
      case 0xFD30CF: // 0
      Serial.println("0");
      break;
      case 0xFDB04F: // EQ
      break;
      case 0xFD708F: // ST/RPT
      break;
      case 0xFD08F7: // 1
      Serial.println("1");
      break;
      case 0xFD8877: // 2
      Serial.println("2");
      break;
      case 0xFD48B7: // 3
      Serial.println("3");
      break;
      case 0xFD28D7: // 4
      Serial.println("4");
      break;
      case 0xFDA857: // 5
      Serial.println("5");
      break;
      case 0xFD6897: // 6
      Serial.println("6");
      break;
      case 0xFD18E7: // 7
      Serial.println("7");
      break;
      case 0xFD9867: // 8
      Serial.println("8");
      break;
      case 0xFD58A7: // 9
      Serial.println("9");
      break; 
  }
    
    irrecv.resume();
  }
}
