#*****LCDTemp.py*****#
from decimal import Decimal
import RPi.GPIO as GPIO
import PCF8591 as ADC
import math
import time
import LCD1602 as LCD
import requests, json, base64, datetime

tempPin = 11  # temperature D0 pin
GPIO.setmode(GPIO.BOARD)  # reference pins using BOARD numbers
key = ''  # Consumer Key
secret = ''  # Consumer Secret


# *****Initialize Pins*****#
def setup():
    ADC.setup(0x48)  # set up analog converter
    GPIO.setup(tempPin, GPIO.IN)  # set pin to input
    LCD.init(0x27, 1)  # init(slave address, background light)


# *****Main Loop, sets temperatures*****#
def loop():
    currDay = 0  # use currDay as variable to keep track of last numeric day
    while True:
        now = datetime.datetime.now()  # create datetime object called now
        if currDay == now.day:  # if currDay and now.day are equal, only update ambient temperature
            analogVal = ADC.read(0)  # read temperature sensor value
            # Calculations to convert to Celsius, from SunFounder
            Vr = 5 * float(analogVal) / 255
            Rt = 10000 * Vr / (5 - Vr)
            temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
            temp = Decimal(temp - 273.15)  # convert to Decimal Type
            temp = round(temp, 1)  # round to 1 decimal point
            LCD.write(0, 0, 'Temp: {} C'.format(temp))  # write to top row and farthest left column of LCD
            time.sleep(1)  # update every second

        else:  # if date has changed
            avgTemp = getHistTemp(now.strftime('%m-%d'))  # get average historical temperature for that day
            avgTemp = round(Decimal(avgTemp), 1)  # convert to decimal and round
            LCD.write(0, 1, 'Avg Temp: ' + str(avgTemp) + ' C')  # write to second row of lcd
            currDay = now.day  # update current day


# *****Get aWhere security token*****#
def getToken():
    combination = key + ':' + secret.encode()
    auth = base64.b64encode(combination).decode('utf8')

    credential = auth
    response = requests.post('https://api.awhere.com/oauth/token',
                             data='grant_type=client_credentials',
                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                      'Authorization': 'Basic {}'.format(credential)}).json()

    if 'access_token' and 'expires_in' in response.keys():  # if response contains access token
        print(response['access_token'])
        return response['access_token']  # return access token
    else:
        raise ValueError(response)


# ***** use aWhere to get historical temperature for certain day*****#
def getHistTemp(date):
    token = getToken()
    headers = {"Authorization": "Bearer " + token,
               "Content-Type": "application/json"}
    response = requests.get('https://api.awhere.com/v2/weather/fields/Toronto/norms/' + date, headers=headers)
    data = response.json()
    return (data['meanTemp']['average'])


# *****MAIN*****#
if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        pass
