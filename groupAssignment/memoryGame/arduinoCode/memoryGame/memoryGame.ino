// reference : https://www.pjrc.com/teensy/td_libs_IRremote.html

/*##########################################################
#####    Install IRremote library by Ken Sheriff &     #####
#####    SevSeg library. See github wiki for list of   #####
#####    known bugs.                                   #####
###########################################################*/


#include <IRremote.h> // Include IR remote Library
#include "SevSeg.h" // LED segment display library

SevSeg sevseg;
int IR_pin = 13;
int buzzer = 12;
int repeat;
int next_level = 0; // boolean value for 3 correct answers

//#define REPEAT random(10) // randomise beeps 1 - 10
#define TONE random(1000) // randomize tone

// Define IR receive and results objects
IRrecv irrecv(IR_pin);
decode_results results;


void setup() {
  Serial.begin(9600);
  //Enable IR receiver
  irrecv.enableIRIn();
  pinMode(buzzer, OUTPUT);
  // if analog input pin 0 is unconnected, random analog
  // noise will cause the call to randomSeed() to generate
  // different seed numbers each time the sketch runs.
  // randomSeed() will then shuffle the random function
  randomSeed(analogRead(0));

  //LED display
  byte numDigits = 1;
  byte digitPins[] = {};
  byte segmentPins[] = {2, 3, 4, 5, 6, 7, 8 ,9};
  bool resistorsOnSegments = true;
  byte hardwareConfig = COMMON_ANODE;
  sevseg.begin(hardwareConfig, numDigits, digitPins, segmentPins, resistorsOnSegments);
  sevseg.setBrightness(90);
}


// Memory game level 1
void level_1() 
{
  repeat = random(10);
  for (int i = 0; i < repeat; i++)
  {
    tone(buzzer, TONE);
    delay(500);
    noTone(buzzer);
    delay(750);
  }
 
  Serial.println(repeat); // send answer to pi
  //get_input();
  delay(5000);
  sevseg.setNumber(repeat); // show answer on LED display
  sevseg.refreshDisplay();
  delay(1000);
  
}

// shorter delays
void level_2()
{
   repeat = random(10);
  for (int i = 0; i < repeat; i++)
  {
    tone(buzzer, TONE);
    delay(250);
    noTone(buzzer);
    delay(250);
  }
  Serial.println(repeat);
  delay(5000);
  sevseg.setNumber(repeat);
  sevseg.refreshDisplay();
  delay(1000);
}

// random tone length and delay
void level_3() 
{
   repeat = random(10);
  for (int i = 0; i < repeat; i++)
  {
    tone(buzzer, TONE);
    delay(random(500));
    noTone(buzzer);
    delay(random(500));
  }
  Serial.println(repeat);
  delay(5000);
  sevseg.setNumber(repeat);
  sevseg.refreshDisplay();
  delay(1000);
  
}

// change level when signal from pi received
void level_up(int current_level)
{
}

void loop() 
{
   if (Serial.available())
  {
    next_level = Serial.read() - '0';  
  }
  if (next_level == 1)
  {
    level_up(current_level);
  }

  // what button pressed on remote
  if (irrecv.decode(&results))
  {
      switch(results.value)
      {
        case 0xFFFFFF: // button held down
        noTone(buzzer);
        break;
        
        case 0xFD00FF: // Power button 
        Serial.println("Let's go...");
        delay(1000);
      // start game
        level_1();
        break;
        
        case 0xFD30CF: // 0
        Serial.println("0");
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
