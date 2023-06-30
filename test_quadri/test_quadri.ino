//résultats de la dernière fois : vitesse = 0.5m/s avec oscillo ; rpm = 204 avec tachometre -> 0.5m/s aussi

// Code using Robust Arduino Serial Protocol: https://github.com/araffin/arduino-robust-serial
#include <Arduino.h>

#include "order.h"
#include "slave.h"
#include "parameters.h"
#include <Metro.h>

int pos = 60;
int t = 0;
float v = 0;
int signe = 1;

//int URPWM = 11; // PWM Output 0－25000US，Every 50US represent 1cm
//int URTRIG= 10; // PWM trigger pin
uint8_t EnPwmCmd[4]={0x44,0x02,0xbb,0x01};    // distance measure command


bool is_connected = false; ///< True if the connection with the master is available
int8_t motor_speed_right = 0;
int8_t motor_speed_left = 0;
int8_t motor_speed_down_right = 0;
int8_t motor_speed_down_left = 0;


void setup()
{
  int t = 0;
  float v = 0;
  Time = millis();
  // Init Serial
  Serial.begin(SERIAL_BAUD);
  
  //SensorSetup();

  // Init Motor
  pinMode(SPEED_LEFT, OUTPUT);
  pinMode(SPEED_RIGHT, OUTPUT);
  pinMode(DIRECTION_LEFT, OUTPUT);
  pinMode(DIRECTION_RIGHT, OUTPUT);
  pinMode(SPEED_DOWN_LEFT, OUTPUT);
  pinMode(SPEED_DOWN_RIGHT, OUTPUT);
  pinMode(DIRECTION_DOWN_LEFT, OUTPUT);
  pinMode(DIRECTION_DOWN_RIGHT, OUTPUT);
  pinMode(interruptA, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptA), speedA, CHANGE);
  pinMode(interruptB, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptB), speedB, RISING);
  
  // Stop the car
  stop();


  // Wait until the arduino is connected to master
  while(!is_connected)
  {
    write_order(HELLO);
    wait_for_bytes(1, 1000);
    get_messages_from_serial();
  }
}

/*void SensorSetup(){
  pinMode(URTRIG,OUTPUT);                     // A low pull on pin COMP/TRIG
  digitalWrite(URTRIG,HIGH);                  // Set to HIGH
  pinMode(URPWM, INPUT);                      // Sending Enable PWM mode command
  for(int i=0;i<4;i++){
      Serial.write(EnPwmCmd[i]);
   }
}*/

void loop()
{
  get_messages_from_serial();
  update_motors_orders();
  
  if (millis() - Time > 431)
  {
    v=0;
  }
}

void update_motors_orders()
{

  motor_speed_right = constrain(motor_speed_right, -SPEED_MAX, SPEED_MAX);
  motor_speed_left = constrain(motor_speed_left, -SPEED_MAX, SPEED_MAX);
  motor_speed_down_right = constrain(motor_speed_down_right, -SPEED_MAX, SPEED_MAX);
  motor_speed_down_left = constrain(motor_speed_down_left, -SPEED_MAX, SPEED_MAX);
  // Send motor speed order

  if (motor_speed_left >= 0)
  {
    digitalWrite(DIRECTION_LEFT, LOW);
  }
  else
  {
    digitalWrite(DIRECTION_LEFT, HIGH);
  }
  
  if (motor_speed_right < 0)
  {
    digitalWrite(DIRECTION_RIGHT, HIGH);
  }
  else
  {
       digitalWrite(DIRECTION_RIGHT, LOW);
  }
  
  if (motor_speed_down_left >= 0)
  {
    digitalWrite(DIRECTION_DOWN_LEFT, LOW);
  }
  else
  {
    digitalWrite(DIRECTION_DOWN_LEFT, HIGH);
  }
  
  if (motor_speed_down_right < 0)
  {
    digitalWrite(DIRECTION_DOWN_RIGHT, HIGH);
  }
  else
  {
       digitalWrite(DIRECTION_DOWN_RIGHT, LOW);
  }
  
  analogWrite(SPEED_LEFT, convert_to_pwm(float(motor_speed_left)));
  analogWrite(SPEED_RIGHT, convert_to_pwm(float(motor_speed_right)));
  analogWrite(SPEED_DOWN_LEFT, convert_to_pwm(float(motor_speed_down_left)));
  analogWrite(SPEED_DOWN_RIGHT, convert_to_pwm(float(motor_speed_down_right)));
}

void stop()
{

  analogWrite(SPEED_LEFT, 0);
  digitalWrite(DIRECTION_LEFT, LOW);
  analogWrite(SPEED_RIGHT, 0);
  digitalWrite(DIRECTION_RIGHT, LOW);
  analogWrite(SPEED_DOWN_LEFT, 0);
  digitalWrite(DIRECTION_DOWN_LEFT, LOW);
  analogWrite(SPEED_DOWN_RIGHT, 0);
  digitalWrite(DIRECTION_DOWN_RIGHT, LOW);
}

int convert_to_pwm(float motor_speed)
{
  // TODO: compensate the non-linear dependency speed = f(PWM_Value)
  return (int) round(abs(motor_speed)*(255./100.));
}

void get_messages_from_serial()
{
  if(Serial.available() > 0)
  {
    // The first byte received is the instruction
    Order order_received = read_order();
    
    

    if(order_received == HELLO)
    {
      // If the cards haven't say hello, check the connection
      if(!is_connected)
      {
        is_connected = true;
        write_order(HELLO);
//        Serial.println("hello aller-retour");
      }
      else
      {
        // If we are already connected do not send "hello" to avoid infinite loop
        write_order(ALREADY_CONNECTED);
//        Serial.println("deja conneecte");
      }
    }
    else if(order_received == ALREADY_CONNECTED)
    {
      is_connected = true;
    }
    else
    {
      // Serial.print(order_received);
      switch(order_received)
      {
        case STOP:
        {
          //motor_speed = 0;
          motor_speed_left = 0;
          motor_speed_right = 0;
          motor_speed_down_left = 0;
          motor_speed_down_right = 0;
          stop();
          if(DEBUG)
          {
            write_order(STOP);
          }
          break;
        }
        
        case READENCODER:
        {
          //vitesse();
          break;
        }
        
        case ResetENCODER:
        {
          setup();
        }
        
        case MOTOR:
        {
          motor_speed_left = read_i8();
          if(DEBUG)
          {
            write_order(MOTOR);
            write_i8(motor_speed_left);
          }
          motor_speed_right = read_i8();
          if(DEBUG)
          {
            write_order(MOTOR);
            write_i8(motor_speed_right);
          }
          motor_speed_down_left = read_i8();
          if(DEBUG)
          {
            write_order(MOTOR);
            write_i8(motor_speed_down_left);
          }
          motor_speed_down_right = read_i8();
          if(DEBUG)
          {
            write_order(MOTOR);
            write_i8(motor_speed_down_right);
          }
          break;
        }        
        

    // Unknown order
    default:
          //write_order(ERROR);
          //write_i32(404);
          // write_i16(2000);
      return;
      }
    }
  //  write_order(RECEIVED); // Confirm the reception
  }
}


void speedA()
{
  /*write_order(HELLO);
  t = millis() - Time;
  Time = millis();*/
}

void speedB()
{
  /*if (digitalRead(interruptA) == HIGH)
  {
    signe = -1;
    write_order(HELLO);
  }
  
  else
  {
    signe = 1;
  }*/
}

void vitesse()
{
  /*if (millis() - Time <= 431)
  {
    v = 32.5*((2*3.1415)/468.6)/t; // t en ms, 32.5 rayon en mm
  }
  write_i16(signe*v*100); // affiche des cm/s*/
}


Order read_order()
{
  return (Order) Serial.read();
}

void wait_for_bytes(int num_bytes, unsigned long timeout)
{
  unsigned long startTime = millis();
  //Wait for incoming bytes or exit if timeout
  while ((Serial.available() < num_bytes) && (millis() - startTime < timeout)){}
}

// NOTE : Serial.readBytes is SLOW
// this one is much faster, but has no timeout
void read_signed_bytes(int8_t* buffer, size_t n)
{
  size_t i = 0;
  int c;
  while (i < n)
  {
    c = Serial.read();
    if (c < 0) break;
    *buffer++ = (int8_t) c; // buffer[i] = (int8_t)c;
    i++;
  }
}

int8_t read_i8()
{
  wait_for_bytes(1, 100); // Wait for 1 byte with a timeout of 100 ms
  return (int8_t) Serial.read();
}

/*int16_t read_i16()
{
  int8_t buffer[2];
  wait_for_bytes(2, 200); // Wait for 2 bytes with a timeout of 100 ms
  read_signed_bytes(buffer, 2);
  return (((int16_t) buffer[0]) & 0xff) | (((int16_t) buffer[1]) << 8 & 0xff00);
}*/

/*int32_t read_i32()
{
  int8_t buffer[4];
  wait_for_bytes(4, 400); // Wait for 4 bytes with a timeout of 200 ms
  read_signed_bytes(buffer, 4);
  return (((int32_t) buffer[0]) & 0xff) | (((int32_t) buffer[1]) << 8 & 0xff00) | (((int32_t) buffer[2]) << 16 & 0xff0000) | (((int32_t) buffer[3]) << 24 & 0xff000000);
}*/

void write_order(enum Order myOrder)
{
  uint8_t* Order = (uint8_t*) &myOrder;
  Serial.write(Order, sizeof(uint8_t));
}

void write_i8(int8_t num)
{
  Serial.write(num);
}

void write_i16(int16_t num)
{
  int8_t buffer[2] = {(int8_t) (num & 0xff), (int8_t) (num >> 8)};
  Serial.write((uint8_t*)&buffer, 2*sizeof(int8_t));
}

/*void write_i32(int32_t num)
{
  int8_t buffer[4] = {(int8_t) (num & 0xff), (int8_t) (num >> 8 & 0xff), (int8_t) (num >> 16 & 0xff), (int8_t) (num >> 24 & 0xff)};
  Serial.write((uint8_t*)&buffer, 4*sizeof(int8_t));
}*/
