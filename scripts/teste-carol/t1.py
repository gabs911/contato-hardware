
import serial
import time
import rtmidi
import sys

#Alterar port de acordo com a saída bluetooth do contato
#Modificação para alternar porta bluetooh fora do scrpt direto ao rodar pelo terminal

contato = 'COM22'
if len(sys.argv) > 1:
    contato = 'COM' + sys.argv[1]

serialPort = serial.Serial(port = contato, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialString = ''

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
port = midiout.open_port(1)

#Sensor variables
gyro = 0
accel = 0
touch = 0

#variables
note = ('a',0)
last_note = 32
notes = [69,74, 76, 77, 78,79]
notes_delay = [0] * len(notes)
lastDebounceTime = 0  
debounceDelay = 0.1
noteHold = 0.2
soundEffectDuration = 2
previousSoundEffect = 3
soundeEffectInterval = 2
previousSoundEffectActiv = 0
angle = 35 #distancia entre os angulos ((gyro//angle) == -2):

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
    
    if(-90 <= gyro <= -61):
        note = ('B5',notes[0])
    elif(-60 <= gyro <= -31):
        note = ('B5',notes[1])
    elif(-30 <= gyro <= -1):
        note = ('B5',notes[2])
    elif(0 <= gyro <= 30):
        note = ('B5',notes[3])
    elif(31 <= gyro <= 60):
        note = ('B5',notes[4])
    elif(61 <= gyro <= 90):
        note = ('B5',notes[5])
  

    can = (note == last_note) and (time.time() - lastDebounceTime > 0.1)
    
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
    
    for i in range(len(notes)):
        if((time.time() - notes_delay[i] > noteHold)):
           #print(f"Off + " + str(note))
            if(notes[i] != note[1]):
                midiout.send_message([0x80,notes[i],100])
                pass
            elif(touch !=1):
                midiout.send_message([0x80,note[1],100])
                pass

    #Mudar o valor para configurar a sensibilidade do acelerometro 
    
    if(accel > 4000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        print("ACCEL DETECTED")
        midiout.send_message([0x91,notes[0],120]) #parametro da nota segundo numero do midiout.sed_message
    
    if(time.time() - previousSoundEffectActiv >= soundEffectDuration):
        previousSoundEffect = time.time()
        #print("ACCEL SOUND EFFECT OFF")

        midiout.send_message([0x81,notes[0],120]) #nota tem que ta igual nos dois midiout.sed_message do accel