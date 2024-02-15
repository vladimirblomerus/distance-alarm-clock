import RPi.GPIO as GPIO
import time

# Constants
SPEED_OF_SOUND = 34300  # cm/s
MAX_DISTANCE = 300      # Maximum distance you expect to measure
SPIKE_FILTER = 50       # Maximum jump in distance for spike detection

# Set GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

tid = 5

# Set GPIO Pins
GPIO_TRIGGER = 27
GPIO_ECHO = 22

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # Set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # Set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # Save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # Save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # Time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # Multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * SPEED_OF_SOUND) / 2

    return distance

def filtered_distance(previous_distance):
    current_distance = distance()
    # Simple spike filter
    if current_distance > MAX_DISTANCE:
        #print("Spike detected, using previous value.")
        return previous_distance
    return current_distance

if __name__ == '__main__':
    try:
        last_distance = distance()
        while True:
            last_distance = distance()
             
            print("Measured Distance = %.1f cm" % last_distance)
            time.sleep(1)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()                                                 