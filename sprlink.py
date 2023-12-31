import RPi.GPIO as GPIO
import time

channel = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)


def motor_on(pin):
	GPIO.output(pin, GPIO.HIGH)


def notor_off(pin):
	GPIO.output(pin, GPIO.LOW)


if __name__ == '__main__':
	try:
		motor_on(channel)
		time.sleep(1)
		motor_off(channel)
		time.sleep(1)
		GPIO.cleanup()
	except:
		GPIO.cleanup()
		print('error!')
