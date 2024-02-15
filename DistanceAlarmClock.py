#Libraries
import RPi.GPIO as GPIO
import asyncio
import time

#Disable warnings (optional)
GPIO.setwarnings(False)
#Select GPIO mode
GPIO.setmode(GPIO.BCM)

#set up buzzer
buzzer=17
GPIO.setup(buzzer,GPIO.OUT)

#set up snoozeButton
snoozeButton=2
GPIO.setup(snoozeButton,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#Set up distance sensor
# Set GPIO Pins
GPIO_TRIGGER = 27
GPIO_ECHO = 22

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
    
# Distance sensor constants
SPEED_OF_SOUND = 34300  # cm/s
MAX_DISTANCE = 300      # Maximum distance you expect to measure

mode = 1 #0 before alarms, 1 during alarms, 2 when snoozing, 3 when guarding after alarms

snoozeDuration = 5 #seconds
snoozeEndTime = 0

def distance():
    waitIterations = 0
    print("calculating distance")
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
        if StartTime - StopTime > 0.1:
            print("ECHO == 0 timed out")
            break
    waitIterations = 0
    # Save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        if StopTime - StartTime > 0.1:
            print("ECHO == 0 timed out")
            break
    # Time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # Multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * SPEED_OF_SOUND) / 2
    print("calculated distance")
    return distance

def filtered_distance(previous_distance):
    current_distance = distance()
    # Simple spike filter
    if current_distance > MAX_DISTANCE:
        #print("Spike detected, using previous value.")
        return previous_distance
    return current_distance                                                 
last_distance = 0
async def distance_loop():
    if last_distance == 0:
        last_distance = distance()
    last_distance = filtered_distance(last_distance)
    print("Measured Distance = %.1f cm" % last_distance)
    await asyncio.sleep(0.5)
        
        
async def main_loop():
    global mode
    while True:
        if mode == 0:
            continue
        elif mode == 1:
            continue
        elif mode == 2:
            #if is_snooze_up() == True:
                #mode = 1
            continue
        else:
            print("Invalid mode detected")
        await asyncio.sleep(0.5)
        

async def main():
    tasks = [
        asyncio.create_task(distance_loop())
        ]
    await asyncio.gather(*tasks)
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()