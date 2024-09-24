# This Python code is an extension script for the Air Mouse using Arduino and MPU6050.
# Visit the Github page for the Arduino code and other information related to the project.
# https://github.com/rupava/Air-Mouse-Using-Arduino-and-MPU6050
# -By Rupava Baruah


import math
import serial
from serial import Serial
from pynput.mouse import Button, Controller

mouse = Controller()
mult = 0.25
accx = 0
accy = 0

try:
  ser = serial.Serial('COM16',baudrate = 115200)       # Setting Serial port number and baudrate
except Exception as e:
  print("Mouse not found or disconnected.", e)
  k=input("Press any key to exit.")
  
while 1:                                            # While loop to continuesly scan and read data from serial port and execute
    dump = ser.readline()                           # Reading Serial port
    dump = str(dump)                                # Converting byte data into string
    dump = dump[2:-5]                               # Cleaning up the raw data recieved from serial port
    data = dump.split(',')                          # Spliting up the data to individual items in a list. the first item being the data identifier
    # print(data)
    
    xfract, xint = math.modf(int(data[1])*mult)
    yfract, yint = math.modf(int(data[2])*mult)
    accx+=xfract
    accy+=yfract
    xchange = xint
    if abs(accx) >=1:
      xchange+=accx; accx = 0
    ychange = yint
    if abs(accy) >=1:
      ychange+=accy; accy = 0
      
    print(f"break: {xfract:+4.3f} {xint:+4.3f} | {yfract:+4.3f} {yint:+4.3f} | {xchange:+4.3f} {ychange:+4.3f} | {data}")
    
    if data[0] == "DATAL" and 1:                          # Checking if the identifier is "DATAL" which the Arduino sends the data as the gyro X, Y and Z values
      mouse.move(-xchange, ychange)        # Moving the mouse by using the X and Y values after converting them into integer
      
    # if data[0] == "DATAB":                          # Checking if the identifier is "DATAB" which the Arduino sends the values for Left/Right button
    #       if data[1] == 'L' :                       # If the Left button is pressed
    #         mouse.press(Button.left)                # The corresponding button is pressed and released
    #         mouse.release(Button.left)
    #       if data[1] == 'R' :                       # If the Right button is pressed
    #               mouse.press(Button.right)         # The corresponding button is pressed and released
    #               mouse.release(Button.right)
