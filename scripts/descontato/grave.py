#Mão esquerda

import serial
import time
import rtmidi
import sys

contato = 'COM5'
if len(sys.argv) > 1:
    contato = 'COM' + sys.argv[1]

serialPort = serial.Serial(port = contato, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE, rtscts=True)
serialString = ''

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
port = midiout.open_port(2)

#Variaveis do sensor
gyro = 0
accel = 0
touch = 0

#Variaveis 
note = ('a',0)
last_note = 0
notes = [50,53,54]
notes_delay = [0] * len(notes)
lastDebounceTime = 2 
noteHold = 2
soundEffectDuration = 0.2
previousSoundEffect = 1
soundeEffectInterval = 2
previousSoundEffectActiv = 0.1


print(notes_delay)

def assignTimes(note):
    
    for i in range(len(notes)):
        if(note == notes[i]):
            notes_delay[i] == time.time()

while(1):

    #gyro, accel, touch = getSensorData()
    if(serialPort.in_waiting > 0):
        
        serialString = serialPort.readline()
        sensorData = (serialString.decode('utf-8')).split('/')
        #print(serialString) 

        id = float(sensorData[0])
        gyro = float(sensorData[1])
        accel = float(sensorData[2])
        touch = float(sensorData[3])
        print(int(id), 'gyro:', gyro, 'acc:', accel, 't:', int(touch))
 
    if(-120 <= gyro <= -30):
        note = ('C5',notes[2])
    elif(-31 <= gyro <= 29):
        note = ('D5',notes[1])
    elif(30 <= gyro <= 120):
        note = ('E5',notes[0])


    can = (note == last_note) and (time.time() - lastDebounceTime > 0.1)  

    if(touch == 1):
        lastDebounceTime = time.time()
        if(note != last_note):
            assignTimes(note[1])
            last_note = note
            midiout.send_message([0x90,note[1],50])
            #print("MIDI ON" + str(time.time()))
        else:
            if(can == True):
                last_note = note
                assignTimes(note[1])
                midiout.send_message([0x90,note[1],50])
                #print("MIDI ON"+ str(time.time()))
    
    for i in range(len(notes)):
        if((time.time() - notes_delay[i] > noteHold)):
           #print(f"Off + " + str(note))
            if(notes[i] != note[1]):
                midiout.send_message([0x80,notes[i],50])
                pass
            elif(touch !=1):
                midiout.send_message([0x80,note[1],50])
                pass

    
    if(12000 > accel > 8000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        #print("ACCEL DETECTED")
        midiout.send_message([0x91,notes[1],50]) 

    elif(-8000 > accel > -12000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        #print("ACCEL DETECTED")
        midiout.send_message([0x91,notes[1],50])
    
    if(time.time() - previousSoundEffectActiv >= noteHold):
        previousSoundEffect = time.time()
        #print("ACCEL SOUND EFFECT OFF")
        midiout.send_message([0x81,notes[1],50]) 