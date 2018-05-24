from decimal import Decimal
import RPi.GPIO as GPIO
import PCF8591 as ADC
import math
import time
import LCD1602 as LCD

tempPin = 11  # temperature D0 pin
GPIO.setmode(GPIO.BOARD)  # reference pins using BOARD numbers


# *****Initialize Pins*****#
def setup():
    ADC.setup(0x48)  # set up analog converter
    GPIO.setup(tempPin, GPIO.IN)  # set pin to input
    LCD.init(0x27, 1)  # init(slave address, background light)


def loop():
    while True:
        analogVal = ADC.read(0)  # read temperature sensor value
        # Calculations to convert to Celsius, from SunFounder
        Vr = 5 * float(analogVal) / 255
        Rt = 10000 * Vr / (5 - Vr)
        temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
        temp = Decimal(temp - 273.15)  # convert to Decimal Type
        temp = round(temp, 1)  # round to 1 decimal point
        LCD.write(0, 0, 'Temp: {} C'.format(temp))  # write to top row and farthest left column of LCD
        time.sleep(1)  # update every second

# *****MAIN*****#
if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        pass
