 


import serial
import time
import rtmidi
import sys


contato = 'COM4'
if len(sys.argv) > 1:
    contato = 'COM' + sys.argv[1]

serialPort = serial.Serial(port = contato, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialString = ''

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
port = midiout.open_port(3)

#Variaveis do sensor
gyro = 0
accel = 0
touch = 0

#Variaveis 
note = ('a',0)
last_note = 0
notes = [40,41,43,45,48,50]
notes_delay = [0] * len(notes)
lastDebounceTime = 0.1 
noteHold = 0.1
soundEffectDuration = 1
previousSoundEffect = 1 
soundeEffectInterval = 0.5
previousSoundEffectActiv = 0.1

def assignTimes(note):
    
    for i in range(len(notes)):
        if(note == notes[i]):
            notes_delay[i] == time.time()

while(1):

    if(serialPort.in_waiting > 0):

        serialString = serialPort.readline()

        sensorData = (serialString.decode('utf-8')).split('/')

        #print(serialString) 
        id = float(sensorData[0])
        gyro = float(sensorData[1])
        accel = float(sensorData[2])
        touch = float(sensorData[3])
        print('gyro:', gyro, 'acc:', accel, 't:', touch) 
    
    if(-102 <= gyro <= -62):
        note = ('B5',notes[4])
    elif(-61 <= gyro <= -21):
        note = ('A5',notes[3])
    elif(-20 <= gyro <= 20):
        note = ('G5',notes[2])
    elif(21 <= gyro <= 41):
        note = ('F5',notes[1])
    elif(42 <= gyro <= 102):
        note = ('E5',notes[0])


    can = (note == last_note) and (time.time() - lastDebounceTime > 0.1)
    
    if(touch == 1):
        lastDebounceTime = time.time()
        if(note != last_note):
            assignTimes(note[1])
            last_note = note
            midiout.send_message([0x90,note[1],30])
            #print("MIDI ON" + str(time.time()))
        else:
            if(can == True):
                last_note = note
                assignTimes(note[1])
                midiout.send_message([0x90,note[1],30])
                #print("MIDI ON"+ str(time.time()))
    
    for i in range(len(notes)):
        if((time.time() - notes_delay[i] > noteHold)):
           #print(f"Off + " + str(note))
            if(notes[i] != note[1]):
                midiout.send_message([0x80,notes[i],30])
                pass
            elif(touch !=1):
                midiout.send_message([0x80,note[1],30])
                pass

    
    if(6000 > accel > 2000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        #print("ACCEL DETECTED")
        midiout.send_message([0x91,notes[5],50]) 

    elif(-4000 > accel > -8000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        #print("ACCEL DETECTED")
        midiout.send_message([0x91,notes[5],50])
    
    if(time.time() - previousSoundEffectActiv >= soundeEffectInterval):
        previousSoundEffect = time.time()
        #print("ACCEL SOUND EFFECT OFF")
        midiout.send_message([0x81,notes[5],50]) 