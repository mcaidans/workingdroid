#include <Servo.h>

// manager.ino
// Griffith Droid Racer 2018
#include "Groid.h"

Groid *myGroid;  
int angle, power;
char command;
int onFor = 300;
int offFor = 700;
bool isOn = false;
unsigned long long time_now;
void setup()
{
  myGroid = new Groid();
  Serial.println("Program Start\n");
  time_now = millis();
}

void loop()
{
  if(power > 0){
    //Serial.println("PowerOn");
    if(!isOn && millis() > time_now + offFor)
    {
      time_now = millis();
      
      isOn = true;
      Serial.println("on");
      //Serial.println(time_now);
      int actualPower = myGroid->setPower(100);
    }
    if(isOn && millis() > time_now + onFor)
    {
      isOn = false;
      Serial.println("off");
      //Serial.println(time_now);
      time_now = millis();
      int actualPower = myGroid->setPower(0);
    }
    
  }
  else if(isOn)
  {
    int actualPower = myGroid->setPower(0);
    Serial.println("ARRGH");
    isOn = false;
  }
  
  /*
  if(power > 0)
  {
    if(count == 300)
    {
      int actualPower = myGroid->setPower(100);       
    }
    if(count == 400)
    {
      int actualPower = myGroid->setPower(0);
      count = 0;
    }
    count++;
  }
  else
  {
      int actualPower = myGroid->setPower(0);
  }
*/
 
  String input = "";
  delay(1);

  while(Serial.available() > 0)
  {
    command = (byte) Serial.read();
    if(command == ':')
    {
      break;
    }
    else
    {
      input += command;
    }
    delay(10);
  }

  if(input.length() > 0)
  {
    int commaIndex = input.indexOf(",");
    angle = input.substring(0, commaIndex).toInt();
    power = commaIndex > 0 ? (input.substring(commaIndex + 1).toInt()) : power;

    int actualAngle = myGroid->setSteeringAngle(angle);
    //int actualPower = myGroid->setPower(power);
    //time_now = millis();

    Serial.print("Angle: ");
    Serial.print(actualAngle);
    Serial.print(", power: ");
    Serial.print(power);
    Serial.println(".");
  }
}


