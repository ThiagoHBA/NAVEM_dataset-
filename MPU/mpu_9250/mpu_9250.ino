#include "MPU9250.h"
#include <SoftwareSerial.h>

// an MPU9250 object with the MPU-9250 sensor on I2C bus 0 with address 0x68
MPU9250 IMU(Wire,0x68);
SoftwareSerial mySerial(6, 5); // RX, TX  

int status;
float ax;
float ay;
float az;

float gx;
float gy;
float gz;

float mx;
float my;
float mz;

int success_led = 10; //leds used to confirm if pc get the data.
int fail_led = 12;   // if yes, her blink green, if data are corrupted, her blink red.

float q[4] = {1.0f, 0.0f, 0.0f, 0.0f};

//used to calculate the quaternions:
float GyroMeasError = PI * (40.0f / 180.0f); 
float beta = sqrt(3.0f / 4.0f) * GyroMeasError;
float deltat = 0.0f, sum = 0.0f;

uint32_t lastUpdate = 0, firstUpdate = 0; // used to calculate integration interval
uint32_t Now = 0;
uint32_t Update = 9300; //mean value of times in calcule of quaternions

void setup() {
  Serial.begin(115200);
  mySerial.begin(38400);  
  pinMode(success_led, OUTPUT);
  pinMode(fail_led, OUTPUT);
  
  status = IMU.begin();
/*
  float axB = IMU.getAccelBiasX_mss();
  float ayB = IMU.getAccelBiasY_mss();
  float azB = IMU.getAccelBiasZ_mss();

  IMU.calibrateAccel();*/
}

void loop() {
  if (Serial.available()){ 
    Serial.flush();
    delay(15);

    if(Serial.read() == 'f'){
      digitalWrite(fail_led, HIGH);
      delay(5000); 
      digitalWrite(fail_led, LOW);
    }
    
    else{  
      digitalWrite(success_led,HIGH);
      uint32_t iniFor = micros();   // começo a capturar o tempo que a amostra foi pegue.
      for(int i = 0;i<8; i++){   
        delay(2);
        IMU.readSensor(); 
        ax = IMU.getAccelX_mss();
        ay = IMU.getAccelY_mss();
        az = IMU.getAccelZ_mss();
      
        gx = IMU.getGyroX_rads();
        gy = IMU.getGyroY_rads();
        gz = IMU.getGyroZ_rads();
      
        mx = IMU.getMagX_uT();
        my = IMU.getMagY_uT();
        mz = IMU.getMagZ_uT();
        
        ax = ax + -0.27;
        ay = ay + 0.14;
        az = az + 2.79;  //manual gravity correction.
  
        //MadgwickQuaternionUpdate(ax,ay,az,gx,gy,gz,mx,my,mz);
        
        digitalWrite(success_led, LOW);
        uint32_t MiddleFor = micros(); 
        Now = MiddleFor - iniFor; //subtraio para saber quanto tempo durou para obter as amostras.
        i == 0? deltat = Update/1000000.0 : deltat = (Now - lastUpdate)/ 1000000.0; 
        Update = Now - lastUpdate;
        lastUpdate = Now;
        /*
        de forma que a função micros() retorna 
        o tempo em microssegundos desde o inicio 
        do código, toda primeira amostra antes de 
        de entrar no loop vem com valores maiores.

        Para solucionar isso eu pego sempre o valor 
        passado da variável "Update" e o uso como pri-
        meiro valor.
        */
        
        //Send data to serial port
        Serial.print(Adequar(ax, 8));
        Serial.print(Adequar(ay, 8));
        Serial.print(Adequar(az, 8));
        Serial.print(Adequar(gx, 8));
        Serial.print(Adequar(gy, 8));
        Serial.print(Adequar(gz, 8));
        Serial.print(Adequar(mx,8));
        Serial.print(Adequar(my,8));
        Serial.print(Adequar(mz,8));
        Serial.print(Adequar(deltat,8));
      }
    }
  } 
  digitalWrite(success_led,LOW);
} 


String Adequar(float eixo, int size_char){ //Function to obtain all axis values with the same size of characteres.  
  String adicionais;
  String Decimais = String(abs(eixo),4);
  if(eixo == 0.0)Decimais = String(0.00,4);
  String eixo_string = "";
 
  if(eixo >=0){
    if(eixo >= 1000)eixo = 999.99;  
    
    int adicionais_char = size_char - (Decimais.length() - 1);
    
    for(int i = 0; i < adicionais_char; i++){ 
        adicionais += "0";
        eixo_string += adicionais; 
      }
      eixo_string = String(adicionais + Decimais);
      return eixo_string;
  }
  
  else{
    eixo = abs(eixo);
    if(eixo >= 1000)eixo = 999.99;  
    int adicionais_char = size_char - (Decimais.length() - 1);
    for(int i = 0; i < adicionais_char; i++){ 
        if(i == 0){
          adicionais += "-";
          continue; 
        }
        adicionais += "0";
        eixo_string += adicionais; 
      }
      eixo_string = String(adicionais + Decimais);
      return eixo_string;
   }
}

//quaternions calculation
void MadgwickQuaternionUpdate(float ax, float ay, float az, float gx, float gy, float gz, float mx, float my, float mz)
{
  float q1 = q[0], q2 = q[1], q3 = q[2], q4 = q[3];   // short name local variable for readability
  float norm;
  float hx, hy, _2bx, _2bz;
  float s1, s2, s3, s4;
  float qDot1, qDot2, qDot3, qDot4;

  // adicionaisiliary variables to avoid repeated arithmetic
  float _2q1mx;
  float _2q1my;
  float _2q1mz;
  float _2q2mx;
  float _4bx;
  float _4bz;
  float _2q1 = 2.0f * q1;
  float _2q2 = 2.0f * q2;
  float _2q3 = 2.0f * q3;
  float _2q4 = 2.0f * q4;
  float _2q1q3 = 2.0f * q1 * q3;
  float _2q3q4 = 2.0f * q3 * q4;
  float q1q1 = q1 * q1;
  float q1q2 = q1 * q2;
  float q1q3 = q1 * q3;
  float q1q4 = q1 * q4;
  float q2q2 = q2 * q2;
  float q2q3 = q2 * q3;
  float q2q4 = q2 * q4;
  float q3q3 = q3 * q3;
  float q3q4 = q3 * q4;
  float q4q4 = q4 * q4;

  // Normalise accelerometer measurement
  norm = sqrtf(ax * ax + ay * ay + az * az);
  if (norm == 0.0f) return; // handle NaN
  norm = 1.0f / norm;
  ax *= norm;
  ay *= norm;
  az *= norm;

  // Normalise magnetometer measurement
  norm = sqrtf(mx * mx + my * my + mz * mz);
  if (norm == 0.0f) return; // handle NaN
  norm = 1.0f / norm;
  mx *= norm;
  my *= norm;
  mz *= norm;

  // Reference direction of Earth's magnetic field
  _2q1mx = 2.0f * q1 * mx;
  _2q1my = 2.0f * q1 * my;
  _2q1mz = 2.0f * q1 * mz;
  _2q2mx = 2.0f * q2 * mx;
  hx = mx * q1q1 - _2q1my * q4 + _2q1mz * q3 + mx * q2q2 + _2q2 * my * q3 + _2q2 * mz * q4 - mx * q3q3 - mx * q4q4;
  hy = _2q1mx * q4 + my * q1q1 - _2q1mz * q2 + _2q2mx * q3 - my * q2q2 + my * q3q3 + _2q3 * mz * q4 - my * q4q4;
  _2bx = sqrtf(hx * hx + hy * hy);
  _2bz = -_2q1mx * q3 + _2q1my * q2 + mz * q1q1 + _2q2mx * q4 - mz * q2q2 + _2q3 * my * q4 - mz * q3q3 + mz * q4q4;
  _4bx = 2.0f * _2bx;
  _4bz = 2.0f * _2bz;

  // Gradient decent algorithm corrective step
  s1 = -_2q3 * (2.0f * q2q4 - _2q1q3 - ax) + _2q2 * (2.0f * q1q2 + _2q3q4 - ay) - _2bz * q3 * (_2bx * (0.5f - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q4 + _2bz * q2) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + _2bx * q3 * (_2bx * (q1q3 + q2q4) + _2bz * (0.5f - q2q2 - q3q3) - mz);
  s2 = _2q4 * (2.0f * q2q4 - _2q1q3 - ax) + _2q1 * (2.0f * q1q2 + _2q3q4 - ay) - 4.0f * q2 * (1.0f - 2.0f * q2q2 - 2.0f * q3q3 - az) + _2bz * q4 * (_2bx * (0.5f - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (_2bx * q3 + _2bz * q1) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + (_2bx * q4 - _4bz * q2) * (_2bx * (q1q3 + q2q4) + _2bz * (0.5f - q2q2 - q3q3) - mz);
  s3 = -_2q1 * (2.0f * q2q4 - _2q1q3 - ax) + _2q4 * (2.0f * q1q2 + _2q3q4 - ay) - 4.0f * q3 * (1.0f - 2.0f * q2q2 - 2.0f * q3q3 - az) + (-_4bx * q3 - _2bz * q1) * (_2bx * (0.5f - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (_2bx * q2 + _2bz * q4) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + (_2bx * q1 - _4bz * q3) * (_2bx * (q1q3 + q2q4) + _2bz * (0.5f - q2q2 - q3q3) - mz);
  s4 = _2q2 * (2.0f * q2q4 - _2q1q3 - ax) + _2q3 * (2.0f * q1q2 + _2q3q4 - ay) + (-_4bx * q4 + _2bz * q2) * (_2bx * (0.5f - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q1 + _2bz * q3) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + _2bx * q2 * (_2bx * (q1q3 + q2q4) + _2bz * (0.5f - q2q2 - q3q3) - mz);
  norm = sqrtf(s1 * s1 + s2 * s2 + s3 * s3 + s4 * s4);    // normalise step magnitude
  norm = 1.0f / norm;
  s1 *= norm;
  s2 *= norm;
  s3 *= norm;
  s4 *= norm;

  // Compute rate of change of quaternion
  qDot1 = 0.5f * (-q2 * gx - q3 * gy - q4 * gz) - beta * s1;
  qDot2 = 0.5f * (q1 * gx + q3 * gz - q4 * gy) - beta * s2;
  qDot3 = 0.5f * (q1 * gy - q2 * gz + q4 * gx) - beta * s3;
  qDot4 = 0.5f * (q1 * gz + q2 * gy - q3 * gx) - beta * s4;

  // Integrate to yield quaternion
  q1 += qDot1 * deltat;
  q2 += qDot2 * deltat;
  q3 += qDot3 * deltat;
  q4 += qDot4 * deltat;
  norm = sqrtf(q1 * q1 + q2 * q2 + q3 * q3 + q4 * q4);    // normalise quaternion
  norm = 1.0f / norm;
  q[0] = q1 * norm;
  q[1] = q2 * norm;
  q[2] = q3 * norm;
  q[3] = q4 * norm;

}
