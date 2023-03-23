#include <IRremote.h>
#include <Servo.h>

Servo top;
Servo bot;
int topPin = 4;
int botPin = 5;

int RECV_PIN = 2;
IRrecv irrecv(RECV_PIN);
decode_results results;

const unsigned long buttonR = 0xFFC23D;
const unsigned long buttonL = 0xFF22DD;
const unsigned long buttonU = 0xFF906F;
const unsigned long buttonD = 0xFFE01F;
const unsigned long buttonP = 0xFF02FD;

int topAngle = 155, botAngle = 90;
int botAngleInc = 45;
int topAngleInc = 15;

void setup()
{
  Serial.begin(38400);
  irrecv.enableIRIn(); // Start the receiver
  pinMode(RECV_PIN, INPUT);
  top.attach(topPin);
  bot.attach(botPin);
  top.write(topAngle);
  bot.write(botAngle);
}

unsigned long int a, b=0, validButtons[] = {buttonU, buttonD, buttonL, buttonR, buttonP};

enum State{
  nothing, animation
} cur;




// topA, botA, duration
double d = 0.5;
double anime[][3] = 

// HEAD BOB
{{180, 90, 0}, {112, 110, d}, {64.8, 130, d}, {28.8, 150, d}, {7.2, 130, d}, {0, 110, d}, {7.2, 90, d}, {28.8, 70, d}, {64.8, 50, d}, {112, 70, d}, {180, 90, d}};

// {{}};

int n = sizeof(anime) / sizeof(anime[0]);

double startTime;
int curFrame;

void loop() {

  a = getIRRemoteButton();
  if (a == -1) a = b;

  // update variables, including state
  switch (cur){
    case nothing:
      switch(a) {
        case buttonU:
          topAngle = constrain(topAngle - topAngleInc, 0 , 180);
          break;
        case buttonD:
          topAngle = constrain(topAngle + topAngleInc, 0 , 180);
          break;
        case buttonL:
          botAngle = constrain(botAngle + botAngleInc, 0 , 180);
          break;
        case buttonR:
          botAngle = constrain(botAngle - botAngleInc, 0 , 180);
          break;
        case buttonP:
          cur = animation;
          curFrame = 0;
          startTime = millis();
          break;
      }
      break;
      
    case animation:
      switch(a) {
        case buttonP:
          cur = nothing;
          break;
      }
      break;
  }
  
  // run code based on state and variables
  switch (cur){
    case nothing:
      switch(a){
        case buttonU:
        case buttonD:
        case buttonL:
        case buttonR:
          break;
      }
      top.write(topAngle);
      bot.write(botAngle);
      break;
      
    case animation:

      if (curFrame == 0) {
        top.write(anime[curFrame][0]);
        bot.write(anime[curFrame][1]);
        curFrame = 1;
      }

      else {
        double elapsed = (millis() - startTime) / 1000;
        double tt = elapsed / (double) anime[curFrame][2];
        top.write(bet(anime[curFrame-1][0], anime[curFrame][0], tt));
        bot.write(bet(anime[curFrame-1][1], anime[curFrame][1], tt));
  
        if (elapsed > anime[curFrame][2]){
          curFrame = (curFrame+1) % n;
          startTime = millis();
        }
        
      }
      
      break;
  }
}

double bet(double a, double b, double per){
  return (b - a) * per + a;
}

bool valid(unsigned long x){
  for (int i=0; i<sizeof(validButtons)/sizeof(validButtons[0]); i++)
    if (x == validButtons[i])
      return true;
  return false;
}

// read button from IR receiver
// 0 means no button pressed
// -1 means repeat button
unsigned long getIRRemoteButton() {
  decode_results results; 
  const int decodeType                = 3; // NEC
  results.value = 0;
  if (irrecv.decode(&results)) {
    // if not right type, ignore
    if (results.decode_type != decodeType) 
      results.value = 0;
    // enable the ir receiver to continue decoding
    irrecv.resume();  
  }
  return results.value;
}
