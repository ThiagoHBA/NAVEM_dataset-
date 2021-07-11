#include <SPI.h>
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif

MPU6050 mpu;
#define OUTPUT_READABLE_REALACCEL


#define INTERRUPT_PIN 2
#define LED_PIN 13
int led = 4;
bool blinkState = false;

volatile char buff [49];
volatile int pos = 0;
volatile int avail = false; 
volatile int startCalibration = false;
volatile int pacoteMontado = false;
volatile bool active = false;

bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

Quaternion q;
VectorInt16 aa;
VectorInt16 aaReal;
VectorInt16 aaWorld;
VectorFloat gravity;
float euler[3];
float ypr[3];
int accx, accy, accz;
double gravityForce = 9.80665;
int calibration = 5;
int wearing = 6;
int start = 7;

uint8_t teapotPacket[14] = { '$', 0x02, 0, 0, 0, 0, 0, 0, 0, 0, 0x00, 0x00, '\r', '\n' };

volatile bool mpuInterrupt = false;
void dmpDataReady() {
  mpuInterrupt = true;
}

void setup() {
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  Wire.begin();
  Wire.setClock(400000);
#elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
  Fastwire::setup(400, true);
#endif

  Serial.begin(115200);

  pinMode(MISO, OUTPUT);
  pinMode(calibration, OUTPUT);
  pinMode(wearing, OUTPUT);
  pinMode(start, OUTPUT);

  SPCR |= bit(SPE);
  SPCR |= bit(SPIE);

  while (!Serial);
  Serial.println(F("Initializing I2C devices..."));
  mpu.initialize();
  pinMode(INTERRUPT_PIN, INPUT);

  Serial.println(F("Testing device connections..."));
  Serial.println(mpu.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));
  Serial.println(F("Initializing DMP..."));
  devStatus = mpu.dmpInitialize();

  if (devStatus == 0) {
    mpu.PrintActiveOffsets();
    mpu.CalibrateAccel(24);
    mpu.CalibrateGyro(24);
    mpu.PrintActiveOffsets();

    Serial.println(F("Enabling DMP..."));
    mpu.setDMPEnabled(true);

    Serial.print(F("Enabling interrupt detection (Arduino external interrupt "));
    Serial.print(digitalPinToInterrupt(INTERRUPT_PIN));
    Serial.println(F(")..."));
    attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), dmpDataReady, RISING);
    mpuIntStatus = mpu.getIntStatus();

    Serial.println(F("DMP ready! Waiting for first interrupt..."));
    dmpReady = true;

    packetSize = mpu.dmpGetFIFOPacketSize();
  } else {
    Serial.print(F("DMP Initialization failed (code "));
    Serial.print(devStatus);
    Serial.println(F(")"));
  }

  pinMode(led, OUTPUT);
  digitalWrite(led, HIGH);

}

ISR (SPI_STC_vect){
  byte c = SPDR;
  
  if(c == 1){
    avail = true;
    startCalibration = true;
    Serial.println("INICIANDO CALIBRAÇÃO");
  }

  if(c == 2){
    avail = true;
    if(startCalibration){
      Serial.println("AINDA CALIBRANDO\n");
      SPDR = 1;
      return 1;  
    } 
    Serial.println("ACABOU CALIBRAÇÃO\n");
    SPDR = 0;
    return 0;
  }

  if (c == 3) { //Recebe o bit da rasp
    Serial.println("PACOTE LIBERADO");
    avail = true; // Ativa o envio do pacote
    active = true;
    SPDR = 1;
    pos = 0;
    return;
  }

    SPDR = buff [pos]; // O bit enviado para SPI vai ser o valor que tá no buffer.
    pacoteMontado = false;
    
    if (buff [pos] == 0 || ++pos >= sizeof (buff)) { // Para quando o buffer acabar.
      active = false;
      avail = false;
    }
}

int contadorDeDados = 0;
volatile char str_temp_1[6];
volatile char str_temp_2[6];
volatile char str_temp_3[6];
volatile char str_accx[6];
volatile char str_accy[6];
volatile char str_accz[6];

void loop() {
  if (!dmpReady) return;
  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) {
#ifdef OUTPUT_READABLE_REALACCEL

    if (avail) {
      if (startCalibration) {
        digitalWrite(calibration, HIGH);
        mpu.CalibrateAccel(24);
        mpu.CalibrateGyro(24);
        
        startCalibrationData();
        digitalWrite(calibration, LOW);

        digitalWrite(wearing, HIGH);
        delay(15000);
        digitalWrite(wearing, LOW);

        Serial.println("ACABOU DE CALIBRAR");
        startCalibration = false;
        avail = false;
      }else{
           digitalWrite(start, HIGH);
            
            mpu.dmpGetQuaternion(&q, fifoBuffer);
            mpu.dmpGetAccel(&aa, fifoBuffer);
            mpu.dmpGetGravity(&gravity, &q);
            mpu.dmpGetLinearAccel(&aaReal, &aa, &gravity);
            mpu.dmpGetLinearAccelInWorld(&aaWorld, &aaReal, &q);
            mpu.dmpGetEuler(euler, &q);
      
            String str = buff;
            
//            accx = aaReal.x;
//            accy = aaReal.y;
//            accz = aaReal.z;

            accx = aaWorld.x;
            accy = aaWorld.y;
            accz = aaWorld.z;

            dtostrf(euler[0], 4, 2, str_temp_1);
            dtostrf(euler[1], 4, 2, str_temp_2);
            dtostrf(euler[2], 4, 2, str_temp_3);
//            dtostrf(accx, 4, 4, str_accx);
//            dtostrf(accy, 4, 4, str_accy);
//            dtostrf(accz, 4, 4, str_accz);
      
            sprintf(buff, "%d:%d:%d:%s:%s:%s:%lu", accx, accy, accz, str_temp_1, str_temp_2, str_temp_3, micros());
      
            avail = false; 
            str = buff;
            
            Serial.print("Index: ");
            Serial.print(contadorDeDados);
            Serial.print(" Dado: ");
            Serial.println(str);
      
            Serial.flush();
            contadorDeDados++;
            digitalWrite(start, LOW);
          }
      }
#endif
  }
}

void startCalibrationData() {
  Serial.println("Calibrando...");
  delay(1000);
  for (int i = 0; i < 15000 ; i++) {
    mpu.dmpGetQuaternion(&q, fifoBuffer);
    mpu.dmpGetAccel(&aa, fifoBuffer);
    mpu.dmpGetGravity(&gravity, &q);
    mpu.dmpGetLinearAccel(&aaReal, &aa, &gravity);
    mpu.dmpGetEuler(euler, &q);

    String str = buff;
    accx = aaReal.x;
    accy = aaReal.y;
    accz = aaReal.z;
  }
}
