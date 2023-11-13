#Musica: Descontato 
#Mão direita 

import serial
import time
import rtmidi
import sys

contato = 'COM13'
if len(sys.argv) > 1:
    contato = 'COM' + sys.argv[1]

serialPort = serial.Serial(port = contato, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE, rtscts=True)
serialString = ''

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
port = midiout.open_port(4)

#Variaveis do sensor
gyro = 0
accel = 0
touch = 0

#Variaveis 
note = ('a',0)
last_note = 0
notes = [86,87,89,93,94] 
notes_delay = [0] * len(notes)
lastDebounceTime = 0.1 
noteHold = 0.2
soundEffectDuration = 0.2
previousSoundEffect = 1
soundeEffectInterval = 1
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

        # Print do conteudo do serial data
        id = float(sensorData[0])
        gyro = float(sensorData[1])
        accel = float(sensorData[2])
        touch = float(sensorData[3])
        print(int(id), 'gyro:', gyro, 'acc:', accel, 't:', int(touch))
    
    #print(accel)   
    if(-90 <= gyro <= -55):
        note = ('a',notes[4])
    elif(-56 <= gyro <= -21):
        note = ('a',notes[3])
    elif(-20 <= gyro <= 15):
        note = ('a',notes[2])
    elif(16 <= gyro <= 51):
        note = ('a',notes[1])
    elif(52 <= gyro <= 90):
        note = ('a',notes[0])
 

    can = (note == last_note) and (time.time() - lastDebounceTime > 0.1)  

    if(touch == 1):
        lastDebounceTime = time.time()
        if(note != last_note):
            assignTimes(note[1])
            last_note = note
            midiout.send_message([0x90,note[1],100])
            #print("MIDI ON" + str(time.time()))
        else:
            if(can == True):
                last_note = note
                assignTimes(note[1])
                midiout.send_message([0x90,note[1],100])
                #print("MIDI ON"+ str(time.time()))
    
    for i in range(len(notes)):
        if((time.time() - notes_delay[i] > noteHold)):
           #print(f"Off + " + str(note))
            if(notes[i] != note[1]):
                midiout.send_message([0x80,notes[i],100])
                pass
            elif(touch !=1):
                midiout.send_message([0x80,note[1],100])
                pass
    
   #if e else do acelerômetro - para frente
    if(7000 > accel > 10000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        #print("ACCEL DETECTED")
        midiout.send_message([0x91,notes[0],50])

   #if e else do acelerômetro - para trás 
    elif(-7000 > accel > -10000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        #print("ACCEL DETECTED")
        midiout.send_message([0x91,notes[0],50]) 
    
    #duração da nota
    if(time.time() - previousSoundEffectActiv >= soundEffectDuration):
        previousSoundEffect = time.time()
        #print("ACCEL SOUND EFFECT OFF")
        midiout.send_message([0x81,notes[0],50])