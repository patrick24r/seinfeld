#include <wiringPi.h>

#define PIN_TRIG 0
#define PIN_ECH0 1

int main(void)
{
    auto distance;

    // Initialize wiring pi interface
    wiringPiSetup();
    // Initialize trigger and echo pins
    pinMode(PIN_TRIG, OUTPUT);
    pinMode(PIN_ECH0, INPUT);

    // Main Loop
    while(1) {
        distance = getUltrasonicDistance(PIN_TRIG, PIN_ECH0);

        // Try again for an invalid distance
        if (distance < 0) continue;

        // Search for a pattern of decreasing distances

    }

}

// Get the distance from the ultrasonic distance sensor in centimeters
double getUltrasonicDistance(triggerPin, echoPin)
{
    double timeout = 1e-3;
    double timeStart, timeStop;

    // Send 10 uS trigger signal to the sensor
    digitalWrite(triggerPin, HIGH);
    delay_us(10);
    digitalWrite(triggerPin, LOW);

    // Wait for echo signal to go high
    while (digitalRead(echoPin) == LOW) {
        if (time > timeout) return -1.0;
    }
    
    // Time the trigger pulse
    timeStart = getDateTime();
    while(digitalRead(echoPin) == HIGH) {
        if (time > timeout) return -2.0;
    }
    timeStop = getDateTime();

    // uS / 58 = cm 
    return (timeStop - timeStart) / 58;
}