
import serial
import time
import rtmidi

serialPort = serial.Serial(port = "COM11", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
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
notes = [43,47,48,50,54]
notes_delay = [0] * len(notes)
lastDebounceTime = 0  
debounceDelay = 0.1
noteHold = 0.2
soundEffectDuration = 2
previousSoundEffect = 3
soundeEffectInterval = 2
previousSoundEffectActiv = 0
angle = 38.60 #descobrir como calcular esse angulo

print(notes_delay)

def assignTimes(note):
    
    for i in range(len(notes)):
        if(note == notes[i]):
            notes_delay[i] == time.time()

while(1):

    #gyro, accel, touch = getSensorData()
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        sensorData = (serialString.decode('utf-8')).split('/')

        #print(serialString)

        # Print the contents of the serial data
        id = float(sensorData[0])
        gyro = float(sensorData[1])
        accel = float(sensorData[2])
        touch = float(sensorData[3])
        print('gyro:', gyro, 'acc:', accel, 't:', touch)
    
    #print(accel)
    
    if((gyro//38.6) == -3):
        note = ('G4',55)
    elif((gyro//38.6) == -2):
        note = ('A4',59)
    elif((gyro//38.6) == -1):
        note = ('B4',48)
    elif((gyro//38.6) == 0):
        note = ('D5', 50)
    elif((gyro//38.6) == 1):
        note = ('D5', 54)

    
    can = (note == last_note) and (time.time() - lastDebounceTime > 0.1)
    #print(touch)

    if(touch == 1):
        lastDebounceTime = time.time()
        if(note != last_note):
            assignTimes(note[1])
            last_note = note
            midiout.send_message([0x92,note[1],100])
            print("MIDI ON" + str(time.time()))
        else:
            if(can == True):
                last_note = note
                assignTimes(note[1])
                midiout.send_message([0x92,note[1],100])
                print("MIDI ON"+ str(time.time()))
    
    for i in range(len(notes)):
        if((time.time() - notes_delay[i] > noteHold)):
           #print(f"Off + " + str(note))
            if(notes[i] != note[1]):
                midiout.send_message([0x82,notes[i],100])
                pass
            elif(touch !=1):
                midiout.send_message([0x82,note[1],100])
                pass

    
    if(accel > 8000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        print("ACCEL DETECTED")
        #midiout.send_message([0x91,82,120])
    
    if(time.time() - previousSoundEffectActiv >= soundEffectDuration):
        previousSoundEffect = time.time()
        #print("ACCEL SOUND EFFECT OFF")
        #midiout.send_message([0x81,82,120])

