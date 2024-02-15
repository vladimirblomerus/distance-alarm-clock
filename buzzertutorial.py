#Libraries
import RPi.GPIO as GPIO
import threading
from time import sleep
#Disable warnings (optional)
GPIO.setwarnings(False)
#Select GPIO mode
GPIO.setmode(GPIO.BCM)

buzzer=17
cancelButton=2
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(cancelButton,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

shouldBeep = True

def beep_loop():
    global shouldBeep
    while True:
        for _ in range(4):
            if shouldBeep:
                GPIO.output(buzzer,GPIO.HIGH)
                print ("Beep")
                sleep(0.05) # Delay in seconds
                GPIO.output(buzzer,GPIO.LOW)
                sleep(0.1) # Delay in seconds
        sleep(0.6)
        
def button_loop():
    global shouldBeep
    while True:
        if GPIO.input(cancelButton) == GPIO.LOW and shouldBeep:
            shouldBeep = False
            print("button")
            break
    print("God morgon")
        

def main():
    buzzer_thread = threading.Thread(target=beep_loop)
    button_thread = threading.Thread(target=button_loop)
    
    buzzer_thread.start()
    button_thread.start()
    
if __name__ == "__main__":
    main()