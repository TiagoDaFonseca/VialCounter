# import RPi.GPIO as gpio
# import time
#
# gpio.setmode(gpio.BCM)
# gpio.setup(18, gpio.OUT)
# gpio.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#
# while True:
#     gpio.output(18, gpio.HIGH)
#     passcode = raw_input("What is pi?: ")
#
#     if passcode == "Awesome":
#         gpio.output(18, gpio.LOW)
#         time.sleep(4)
#
# else:
#     gpio.output(18, gpio.HIGH)
#     print("Wrong Password!")e = raw_input("What is pi?: ")
# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
# GPIO.add_event_detect(4, GPIO.BOTH)
# def my_callback():
#     GPIO.output(25, GPIO.input(4))
# GPIO.add_event_callback(4, my_callback)