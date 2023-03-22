from datetime import datetime
import serial
import time
import rtmidi

serialPort = serial.Serial(port = "COM4", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialString = ''

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
port = midiout.open_port(1)

#Sensor variables
gyro = 0
accel = 0
touch = 0

#variables
note = (0,'a')
last_note = 32
notes = [67,68,72]
notes_delay = [0] * len(notes)
lastDebounceTime = 0  
debounceDelay = 0.1
noteHold = 0.2
soundEffectDuration = 0.7
previousSoundEffect = 0
soundeEffectInterval = 1
previousSoundEffectActiv = 0
angle = 180
prev = 0
lastAccel = 0

print(notes_delay)

def assignTimes(note):
    
    for i in range(len(notes)):
        if(note == notes[i]):
            notes_delay[i] == time.time()

while(1):
    #if(time.time() - prev >= 0.02):
        prev = time.time()

        #gyro, accel, touch = getSensorData()
        if(serialPort.in_waiting > 0):

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()
            sensorData = (serialString.decode('utf-8')).split('/')

            print(serialString)
            

            id = float(sensorData[0])
            gyro = float(sensorData[1])
            accel = float(sensorData[2])
            touch = float(sensorData[3])
            #print(gyro,accel,touch)
            #print(accel-lastAccel)
            lastAccel = accel
           
        
        
        if((gyro//60) == -1):
            note = ('G4',67)
        elif((gyro//60) == 0):
            note = ('A4',68)
        elif((gyro//60) == 1):
            note = ('B4',72)

    

        can = (note == last_note) and (time.time() - lastDebounceTime > 0.1)
        #print(touch)
        if(touch <55):
            touch = 1

        if(touch == 1):
            lastDebounceTime = time.time()
            if(note != last_note):
                assignTimes(note[1])
                last_note = note
                midiout.send_message([0x90,note[1],100])
                print("MIDI ON" + str(time.time()))
            else:
                if(can == True):
                    last_note = note
                    assignTimes(note[1])
                    midiout.send_message([0x90,note[1],100])
                    print("MIDI ON"+ str(time.time()))
        #print('off')
        for i in range(len(notes)):
            
            if((time.time() - notes_delay[i] > noteHold)):
            #print(f"Off + " + str(note))
                if(notes[i] != note[1]):
                    midiout.send_message([0x80,notes[i],100])
                elif(touch !=1):
                    midiout.send_message([0x80,note[1],100])
        if(accel > 8000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
            previousSoundEffectActiv = time.time()
            print("ACCEL DETECTED")
            midiout.send_message([0x91,82,120])
        
        if(time.time() - previousSoundEffectActiv >= soundEffectDuration):
            previousSoundEffect = time.time()
            #print("ACCEL SOUND EFFECT OFF")
            midiout.send_message([0x81,82,120])