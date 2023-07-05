
# inclui  " I2Cdev.h "
# inclui  " BluetoothSerial.h "

# inclua  " MPU6050_6Axis_MotionApps20.h "

# se I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    # inclui  " Wire.h "
#endif _


MPU6050 mpu;
BluetoothSerial SerialBT;


# define  INTERRUPT_PIN  2   // usa o pino 2 no Arduino Uno e na maioria das placas
# define  LED_PIN  13  // (Arduino é 13, Teensy é 11, Teensy++ é 6)
bool blinkState = false ;

// MPU control/status vars
bool dmpReady = false ;  // define true se a inicialização do DMP foi bem-sucedida
uint8_t mpuIntStatus;   // mantém o byte de status de interrupção real do MPU
uint8_t devStatus;      // retorna o status após cada operação do dispositivo (0 = sucesso, !0 = erro)
uint16_t tamanho do pacote;    // tamanho esperado do pacote DMP (o padrão é 42 bytes)
uint16_t fifoCount;     // contagem de todos os bytes atualmente em FIFO
uint8_t fifoBuffer[ 64 ]; // buffer de armazenamento FIFO

// variáveis ​​de orientação/movimento
Quatérnio q;           // [w, x, y, z] recipiente de quaternion
VectorInt16 aa;         // [x, y, z] acelera as medições do sensor
VectorInt16 aaReal;     // [x, y, z] medições do sensor de aceleração sem gravidade
VectorInt16 aaMundo;    // [x, y, z] medições do sensor de aceleração de quadro mundial
VectorFluat gravidade;    // [x, y, z] vetor gravidade
flutuar euler[ 3 ];         // [psi, theta, phi] Contêiner do ângulo de Euler
flutuar ypr[ 3 ];           // [yaw, pitch, roll] guinada/pitch/roll contêiner e vetor de gravidade
float ypr_mod = 0 ;
int mediaAccel;
int pressionado = 0 ;


volátil  bool mpuInterrupt = false ;     // indica se o pino de interrupção do MPU está alto
void  dmpDataReady () {
    mpuInterrupção = verdadeiro ;
}



// ================================================ ================
// === CONFIGURAÇÃO INICIAL ===
// ================================================ ================

 configuração nula () {
    // junta-se ao barramento I2C (a biblioteca I2Cdev não faz isso automaticamente)
    # se I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Arame. começar ();
        Arame. setClock ( 400000 ); // Relógio I2C de 400kHz. Comente esta linha se tiver dificuldades de compilação
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup ( 400 , verdadeiro );
    #endif _

    // inicializa a comunicação serial
    // (115200 escolhido porque é necessário para a saída Teapot Demo, mas é
    // realmente depende de você, dependendo do seu projeto)
    SerialBT. begin ( " Contato-Performance - SIAC 1 " );
    Serial. começar ( 115200 );
    enquanto (!Serial); // espera a enumeração do Leonardo, os outros continuam imediatamente


    // inicializa o dispositivo
    Serial. println ( F ( " Inicializando dispositivos I2C... " ));
    mpu. inicializar ();
    pinMode (INTERRUPT_PIN, INPUT);

    // verifica a conexão
    Serial. println ( F ( " Testando conexões de dispositivos... " ));
    Serial. println (mpu. testConnection () ? F ( " Conexão MPU6050 bem-sucedida " ): F ( " Falha na conexão MPU6050 " ));


    // carrega e configura o DMP
    Serial. println ( F ( " Inicializando DMP... " ));
    devStatus = mpu. dmpInitialize ();

    // forneça seus próprios deslocamentos de giroscópio aqui, dimensionados para sensibilidade mínima
    mpu. setXGyroOffset ( 220 );
    mpu. setYGyroOffset ( 76 );
    mpu. setZGyroOffset (-85 ) ;
    mpu. setZAccelOffset ( 1788 ); // 1688 padrão de fábrica para meu chip de teste

    // certifique-se de que funcionou (retorna 0 em caso afirmativo)
    if (devStatus == 0 ) {
        // Calibration Time: gere offsets e calibre nosso MPU6050
        mpu. CalibrateAccel ( 6 );
        mpu. CalibrateGyro ( 6 );
        mpu. ImprimirDeslocamentosAtivos ();
        // liga o DMP, agora que está pronto
        Serial. println ( F ( " Habilitando DMP... " ));
        mpu. setDMPEnabled ( verdadeiro );

      /*
        Serial.print(F("Habilitando detecção de interrupção (interrupção externa do Arduino "));
        Serial.print(digitalPinToInterrupt(INTERRUPT_PIN));
        Serial.println(F(")..."));
        attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), dmpDataReady, RISING);
        mpuIntStatus = mpu.getIntStatus();
       */
        // define nosso sinalizador DMP Ready para que a função loop() principal saiba que não há problema em usá-lo
        Serial. println ( F ( " DMP pronto! Aguardando a primeira interrupção... " ));
        dmpReady = verdadeiro ;

        // obtém o tamanho esperado do pacote DMP para comparação posterior
        tamanho do pacote = mpu. dmpGetFIFOPacketSize ();
    } senão {
        // 1 = falha no carregamento inicial da memória
        // 2 = Falha nas atualizações de configuração DMP
        // (se for quebrar, geralmente o código será 1)
        Serial. print ( F ( " Falha na inicialização do DMP (código " ));
        Serial. imprimir (devStatus);
        Serial. println ( F ( " ) " ));
    }
}



 laço vazio () {
    if (!dmpReady) return ;
    // lê um pacote de FIFO
    if (mpu. dmpGetCurrentFIFOPacket (fifoBuffer)) { // Obtém o pacote mais recente

        # ifdef OUTPUT_READABLE_EULER
            // exibe os ângulos de Euler em graus
            mpu. dmpGetQuaternion (&q, fifoBuffer);
            mpu. dmpGetEuler (euler, &q);
            Serial. print ( " euler \t " );
            Serial. imprimir (euler[ 0 ] * 180 /M_PI);
            Serial. imprima ( " \t " );
            Serial. imprimir (euler[ 1 ] * 180 /M_PI);
            Serial. imprima ( " \t " );
            Serial. println (euler[ 2 ] * 180 /M_PI);
        #endif _


          mpu. dmpGetQuaternion (&q, fifoBuffer);
          mpu. dmpGetGravity (&gravidade, &q);
          mpu. dmpGetYawPitchRoll (ypr, &q, &gravidade);


        ypr_mod = ypr[ 2 ] * 180 /M_PI;

    }
    pressionado = touchRead ();
    SerialBT. println ( " 01/ " + String (ypr_mod)+ ' / ' + String (mediaAccel)+ ' / ' + String (pressionado));
    Serial. println ( " 01/ " + String (ypr_mod)+ ' / ' + String (mediaAccel)+ ' / ' + String (pressionado));
}

int  touchRead ()
{
  int mídia = 0 ;
  mediaAccel = 0 ;
  for ( int i= 0 ; i< 10 ; i++)
  {
    mídia += touchRead (T3);
    mediaAccel += aaReal. z ;

  }
  mídia = mídia/ 100 ;
  mediaAccel = mediaAccel/ 100 ;

  se (média > 60 )
  {
    retornar  1 ;
  }
  outro
  {
    retorna  0 ;
  }

}