from datetime import datetime
import serial
import time
import rtmidi

serialPort = serial.Serial(port = "COM8", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
prev = 0


def getGyro(serialPort):
    serialString=''
    if(serialPort.in_waiting > 0):
            serialString = serialPort.readline()
    return serialString


while(1):
    
    if(serialPort.in_waiting > 0):
            serialString = serialPort.readline()
            print(serialString)



