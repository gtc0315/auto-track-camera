#include <Servo.h>
Servo tilt;
Servo pan;
int rx = A1; //x pin for joystick
int ry = A0; //y pin for joystick
int rz = 8; //switch pin for joystick
int green = 7; //green pin for led
int red = 4; //red pin for led
int button = 9;//button pin
int facetrack = 0; //status
int buttonVal = 1; //previous button value
double posX = 1500; //initial pan servo position
double posY = 1600; //initial tilt servo position
double dx,dy; //servo steps
// GPIO from Raspberry Pi
int a = 13; //motor direction pin
int b = 12; //motor direction pin
int c = 11; //pan speed
int d = 10; //pan speed
int e = 3; //pan speed
int f = 2; // interrupt pin
int g = A3; //tilt speed
int h = A4; //tilt speed
int i = A5; //tilt speed
volatile boolean state = false;
unsigned long prevTime = 0;
unsigned long durTime;

//initialize all pins
void setup() {
  tilt.attach(5);
  pan.attach(6);
  pinMode(a,INPUT);
  pinMode(b,INPUT);
  pinMode(c,INPUT);
  pinMode(d,INPUT);
  pinMode(e,INPUT);
  pinMode(f,INPUT);
  pinMode(g,INPUT);
  pinMode(h,INPUT);
  pinMode(i,INPUT);  
  pinMode(rx,INPUT);
  pinMode(ry,INPUT);
  pinMode(rz, INPUT_PULLUP);
  pinMode(red,OUTPUT);
  pinMode(green,OUTPUT);
  pinMode(button,INPUT_PULLUP);
  analogWrite(green,0);
  attachInterrupt(digitalPinToInterrupt(f),pinChange,CHANGE);
  Serial.begin(9600);
}

//set the state to true if signal toggles
void pinChange(){
  //calculateTimeInterval();
  state = true;
}

//change mode between auto track and manual control
void buttonControl(){
  int b;
  b = digitalRead(button);
  if (buttonVal==1 & b==0){
    if (facetrack==0){
      facetrack = 1;
    }else{
      facetrack = 0;
    }
  }
  buttonVal = b;  
}

//control servo
void motorControl(int x,int y){
  pan.writeMicroseconds(x);
  tilt.writeMicroseconds(y);  
}

//calculate elapsed time from last call
void calculateTimeInterval(){
      unsigned long curTime = micros();
      durTime = curTime - prevTime;
      prevTime = curTime;   
}

//update the servo position by decoding the servo steps
void posCalculation(){
  int x, y, z, x1, y1;
  if (facetrack==1){
    analogWrite(red,255);

    //decode the servo step based on the 2rd order linear quantization
    if (digitalRead(c)==1 && digitalRead(d)==1 && digitalRead(e)==1){
      dx = 0;
    }else if (digitalRead(c)==1 && digitalRead(d)==1 && digitalRead(e)==0){
      dx = 14.4;
    }else if (digitalRead(c)==1 && digitalRead(d)==0 && digitalRead(e)==1){
      dx = 6.4;
    }else if (digitalRead(c)==1 && digitalRead(d)==0 && digitalRead(e)==0){
      dx = 2.5;
    }else if (digitalRead(c)==0 && digitalRead(d)==1 && digitalRead(e)==1){
      dx = 0.9;
    }else if (digitalRead(c)==0 && digitalRead(d)==1 && digitalRead(e)==0){
      dx = 0.225;
    }else if (digitalRead(c)==0 && digitalRead(d)==0 && digitalRead(e)==1){
      dx = 0.025;
    }else{
      dx = 0;
    }
    
    //decode the servo step based on the 2rd order linear quantization
    if (digitalRead(g)==1 && digitalRead(h)==1 && digitalRead(i)==1){
      dy = 0;
    }else if (digitalRead(g)==1 && digitalRead(h)==1 && digitalRead(i)==0){
      dy = 14.4;
    }else if (digitalRead(g)==1 && digitalRead(h)==0 && digitalRead(i)==1){
      dy = 6.4;
    }else if (digitalRead(g)==1 && digitalRead(h)==0 && digitalRead(i)==0){
      dy = 2.5;
    }else if (digitalRead(g)==0 && digitalRead(h)==1 && digitalRead(i)==1){
      dy = 0.9;
    }else if (digitalRead(g)==0 && digitalRead(h)==1 && digitalRead(i)==0){
      dy = 0.225;
    }else if (digitalRead(g)==0 && digitalRead(h)==0 && digitalRead(i)==1){
      dy = 0.025;
    }else{
      dy = 0;      
    }

    //update the servo positions based on the encoded servo direction signal from Raspberry pi
    if (state==true){     
      state==false;
      if (digitalRead(a)==0 && digitalRead(b)==0){
        posX = posX + dx;
        posY = posY + dy;
      }else if (digitalRead(a)==0 && digitalRead(b)==1){
        posX = posX + dx;
        posY = posY - dy;
      }else if (digitalRead(a)==1 && digitalRead(b)==0){
        posX = posX - dx;
        posY = posY + dy;
      }else if (digitalRead(a)==1 && digitalRead(b)==1){
        posX = posX - dx;
        posY = posY - dy;
      }      
    }

    // set a limited range for the servo
    if (posX>2300){
      posX=2300;
    }
    if (posX<700){
      posX=700;
    }
    if (posY>2300){
      posY=2300;
    }
    if (posY<700){
      posY=700;
    }           
  }else{
    //read the joystick value
    analogWrite(red,0);
    x = analogRead(rx);
    y = analogRead(ry);
    z = digitalRead(rz);
    x1 = map(x,0,1023,1250,2250);
    y1 = map(y,0,1023,2000,1000);
    //update the servo position using the joystick value
    if (z==0){  
      posX = x1;
      posY = y1;
      delay(100);
    }
  }  
}

//main loop
void loop() {
  buttonControl();
  posCalculation();
  motorControl(posX,posY);
//  Serial.println(durTime);
  delay(25);
}
