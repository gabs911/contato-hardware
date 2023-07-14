#bibliotecas 
import serial
import time
import rtmidi
import sys
 

contato = 'COM5'
if len(sys.argv) > 1:
    contato = 'COM' + sys.argv[1]
#Modificação para alternar porta bluetooh fora do script direto ao rodar pelo terminal

serialPort = serial.Serial(port = contato, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialString = ''

#imprime a lista de portas MIDI 
midiout = rtmidi.MidiOut()
print(midiout.get_ports())
port = midiout.open_port(1) #seleciona port MIDI

#Variaveis do sensor 
gyro = 0 
accel = 0
touch = 0

#Variaveis 
mapNotas = { 
    "C4": 48, "C#4": 49, "D4": 50, "D#4": 51, "E4": 52, "F4": 53, "F#4": 54, "G4": 55, "G#4": 56, "A4": 57, "A#4": 58, "B4": 59,
    "C5": 60, "C#5": 61, "D5": 62, "D#5": 63, "E5": 64, "F5": 65, "F#5": 66, "G5": 67, "G#5": 68, "A5": 69, "A#5": 70, "B5": 71,
    "C6": 72, "C#6": 73, "D6": 74, "D#6": 75, "E6": 76, "F6": 77, "F#6": 78, "G6": 79, "G#6": 80, "A6": 81, "A#6": 82, "B6": 83,
    "C7": 84, "C#7": 85, "D7": 86, "D#7": 87, "E7": 88, "F7": 89, "F#7": 90, "G7": 91, "G#7": 92, "A7": 93, "A#7": 94, "B7": 95
} 
notes = []
note = (0) 
last_note = 0
notes_delay = [0] * len(notes) #nota do momento grava seu horario
lastDebounceTime = 0  
noteHold = 0.2 #tempo da nota seg
soundEffectDuration = 0.2 #tempo duração 
previousSoundEffect = 3 #ult toque 
soundeEffectInterval = 2 #temp minimo entro acionamentos sucessivos do acc 
previousSoundEffectActiv = 0

while(1):

    #gyro, accel, touch = getSensorData()
    if(serialPort.in_waiting > 0):

        #Leia os dados do buffer até que return/new line seja encontrado
        serialString = serialPort.readline() 
        sensorData = (serialString.decode('utf-8')).split('/')

        #Print do conteudo do serial data
        id = float(sensorData[0])
        gyro = float(sensorData[1])
        accel = float(sensorData[2])
        touch = float(sensorData[3])

        print('gyro:', gyro, 'acc:', accel, 't:', touch) 
    
    if(-90 <= gyro <= -65):
        notes.append(mapNotas["C5"])
        note = (notes[0])

    elif(-64 <= gyro <= -39):
        notes.append(mapNotas["C6"])
        note = (notes[0])

    elif(-38 <= gyro <= -13):
        notes.append(mapNotas["C7"])
        note = (notes[0])

    elif(-12 <= gyro <= 13):
        notes.append(mapNotas["C4"])
        note = (notes[0])

    elif(14 <= gyro <= 39):
        notes.append(mapNotas["D4"])
        note = (notes[0])

    elif(40 <= gyro <= 65):
        notes.append(mapNotas["D5"])
        note = (notes[0])

    elif(66 <= gyro <= 90):
        notes.append(mapNotas["D6"])
        note = (notes[0])



def assignTimes(note):
    
    for i in range(len(notes)):
        if(note == notes[i]):
            notes_delay[i] == time.time()

    can = (note == last_note) and (time.time() - lastDebounceTime > 0.1)
    
    if(touch == 1):
        print(notes)
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
    
    if(6000 > accel > 4000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        print("ACCEL DETECTED")
        midiout.send_message([0x91,notes['B5'],100]) #parametro da nota segundo numero do midiout.sed_message
        
    elif(-6000 > accel > -4000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        print("ACCEL DETECTED")
        midiout.send_message([0x91,notes['B5'],100]) #parametro da nota segundo numero do midiout.sed_message
    
    if(time.time() - previousSoundEffectActiv >= soundEffectDuration):
        previousSoundEffect = time.time()
        #print("ACCEL SOUND EFFECT OFF")
        midiout.send_message([0x81,notes['B5'],100]) #nota tem que ta igual nos dois midiout.sed_message do accel
