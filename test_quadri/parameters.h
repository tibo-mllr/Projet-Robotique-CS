#ifndef PARAMETERS_H
#define PARAMETERS_H

#define SERIAL_BAUD 115200
#define SPEED_LEFT 6
#define DIRECTION_LEFT 7
// A définir
#define SPEED_DOWN_LEFT 10
#define DIRECTION_DOWN_LEFT 13

#define SPEED_RIGHT 5
#define DIRECTION_RIGHT 4
// A définir
#define SPEED_DOWN_RIGHT 11
#define DIRECTION_DOWN_RIGHT 12
//#define MOTOR_PIN 3
//#define DIRECTION_PIN 4
//#define SERVOMOTOR_PIN 6
#define interruptA 2
#define interruptB 3

/*
const byte interruptA = 2;
const byte interruptB = 3;
volatile byte state = LOW;
*/
unsigned long Time;

// Initial angle of the servomotor
#define INITIAL_THETA 110
// Min and max values for motors
#define THETA_MIN 60
#define THETA_MAX 150
#define SPEED_MAX 200
// If DEBUG is set to true, the arduino will send back all the received messages
#define DEBUG false

#endif
