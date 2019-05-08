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
byte next_level; 
int current_level = 1;

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


// Memory game levels
int level_1(int current_level) 
{
  //Serial.println(String(current_level));
  repeat = random(10);
  if (current_level == 1)
  {
    for (int i = 0; i < repeat; i++)
      {
        tone(buzzer, TONE);
        delay(500);
        noTone(buzzer);
        delay(750);
      }
  }

  // LEVEL 2 - SHORTER DELAYS
  if (current_level == 2)
  {
    for (int i = 0; i < repeat; i++)
      {
        tone(buzzer, TONE);
        delay(250);
        noTone(buzzer);
        delay(250);
      }
  }

  // LEVEL 3 - RANDOM DELAYS
  if (current_level == 3)
  {
    for (int i = 0; i < repeat; i++)
      {
        tone(buzzer, TONE);
        delay(random(500));
        noTone(buzzer);
        delay(random(500));
      }
  }

  return repeat;
}


void loop() 
{
    int answer;
    //int current_level = 1;
    
    if (Serial.available() > 0)
    {
      next_level = Serial.read(); 
    }
    if (next_level == 'y')
    {
      current_level++;
      //Serial.println(String(current_level));
    }
    // what button pressed on remote
    if (irrecv.decode(&results))

    {
      switch(results.value)
      {
        case 0xFFFFFF: // button held down, turn off
        Serial.println("Goodbye...");
        noTone(buzzer);

        break;
        
        case 0xFD00FF: // Power button 
        Serial.println("Let's go...");
        answer = level_1(current_level);
        Serial.println(String(answer));
        sevseg.setNumber(answer); // show answer on LED display
        sevseg.refreshDisplay();
        delay(1000);
        
        break;
        
        case 0xFD30CF: // 0
        Serial.println(String(0));
        break;
        
        case 0xFD08F7: // 1
        Serial.println(String(1));
        break;
       
        case 0xFD8877: // 2
        Serial.println(String(2));
        break;
      
        case 0xFD48B7: // 3
        Serial.println(String(3));
        return 3;
        
        case 0xFD28D7: // 4
        Serial.println(String(4));
        break;
        
        case 0xFDA857: // 5
        Serial.println(String(5));
        break;
        
        case 0xFD6897: // 6
        Serial.println(String(6));
        break;
        
        case 0xFD18E7: // 7
        Serial.println(String(7));
        break;
        
        case 0xFD9867: // 8
        Serial.println(String(8));
        break;
        
        case 0xFD58A7: // 9
        Serial.println(String(9));
        break;
    }
    irrecv.resume();
    
  }
  
  
}
