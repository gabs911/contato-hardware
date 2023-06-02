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