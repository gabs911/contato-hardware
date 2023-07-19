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
note = ('a',0)
last_note = 0
notes = [60,62,64,65,67,69,71]
notes_delay = [0] * len(notes)
lastDebounceTime = 0.1 #ultimo salto 
noteHold = 0.3 #tempo para segurar a nota  
soundEffectDuration = 0.2 #tempo limite para acionamento de disparo, caso for necessario deixar accel com tempo diferente do gyro
previousSoundEffect = 1 #tempo para acionamento do accel
soundeEffectInterval = 2 #intervalo entre os acionamentos do accel
previousSoundEffectActiv = 0.1

#Variaveis antigas:
    #debounceDelay = 0.1
    #angle = 30 #distancia entre os angulos ((gyro//angle) == -2): 

print(notes_delay)

def assignTimes(note):
    
    for i in range(len(notes)):
        if(note == notes[i]):
            notes_delay[i] == time.time()

while(1):

    #gyro, accel, touch = getSensorData()
    if(serialPort.in_waiting > 0):

        #Leia os dados do buffer até que return/new line seja encontrado
        serialString = serialPort.readline()

        sensorData = (serialString.decode('utf-8')).split('/')
        #print(serialString) 

        #Print do conteudo do serial data
        id = float(sensorData[0])
        gyro = float(sensorData[1])
        accel = float(sensorData[2])
        touch = float(sensorData[3])
        print('gyro:', gyro, 'acc:', accel, 't:', touch) 
    
    if(-90 <= gyro <= -65):
        note = ('B5',notes[0])
    elif(-64 <= gyro <= -39):
        note = ('B5',notes[1])
    elif(-38 <= gyro <= -13):
        note = ('B5',notes[2])
    elif(-12 <= gyro <= 13):
        note = ('B5',notes[3])
    elif(14 <= gyro <= 39):
        note = ('B5',notes[4])
    elif(40 <= gyro <= 65):
        note = ('B5',notes[5])
    elif(66 <= gyro <= 90):
        note = ('B5',notes[6])


    can = (note == last_note) and (time.time() - lastDebounceTime > 0.1)
    
    if(touch == 1):
        lastDebounceTime = time.time()
        if(note != last_note):
            assignTimes(note[1])
            last_note = note
            midiout.send_message([0x90,note[1],50])
            print("MIDI ON" + str(time.time()))
        else:
            if(can == True):
                last_note = note
                assignTimes(note[1])
                midiout.send_message([0x90,note[1],50])
                print("MIDI ON"+ str(time.time()))
    
    for i in range(len(notes)):
        if((time.time() - notes_delay[i] > noteHold)):
           #print(f"Off + " + str(note))
            if(notes[i] != note[1]):
                midiout.send_message([0x80,notes[i],50])
                pass
            elif(touch !=1):
                midiout.send_message([0x80,note[1],50]) #0x80 desligar a nota, 100 velocidade do MiDi
                pass

    #Para mudar a sensibilidade do acelerometro alterar os limites (10000 > accel > 8000)
    
    if(10000 > accel > 8000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        print("ACCEL DETECTED")
        midiout.send_message([0x91,notes[5],50]) #parametro da nota segundo numero do midiout.sed_message
    
    if(time.time() - previousSoundEffectActiv >= noteHold): 
        previousSoundEffect = time.time()
        #print("ACCEL SOUND EFFECT OFF")
        midiout.send_message([0x81,notes[5],50]) #nota tem que ta igual nos dois midiout.sed_message do accel