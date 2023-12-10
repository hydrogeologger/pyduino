/***************************************************************************
* Example sketch for the ICM20948_WE library
*
* This sketch shows how to use the data ready interrupt. Enable the gyroscope with
* myIMU.enableGyr(true) and see the difference. 
*   
* Further information can be found on:
*
* https://wolles-elektronikkiste.de/icm-20948-9-achsensensor-teil-i (German)
* https://wolles-elektronikkiste.de/en/icm-20948-9-axis-sensor-part-i (English)
* 
***************************************************************************/

#include <Wire.h>
#include <ICM20948_WE.h>
#define ICM20948_ADDR 0x68

/* There are several ways to create your ICM20948 object:
 * ICM20948_WE myIMU = ICM20948_WE()              -> uses Wire / I2C Address = 0x68
 * ICM20948_WE myIMU = ICM20948_WE(ICM20948_ADDR) -> uses Wire / ICM20948_ADDR
 * ICM20948_WE myIMU = ICM20948_WE(&wire2)        -> uses the TwoWire object wire2 / ICM20948_ADDR
 * ICM20948_WE myIMU = ICM20948_WE(&wire2, ICM20948_ADDR) -> all together
 * Successfully tested with two I2C busses on an ESP32
 */
ICM20948_WE myIMU = ICM20948_WE(ICM20948_ADDR);

const int intPin = 2;
volatile bool dataReady = false;

void setup() {
  Wire.begin();
  Serial.begin(115200);
  while(!Serial) {}
  
  if(!myIMU.init()){
    Serial.println("ICM20948 does not respond");
  }
  else{
    Serial.println("ICM20948 is connected");
  }

  /*  This is a method to calibrate. You have to determine the minimum and maximum 
   *  raw acceleration values of the axes determined in the range +/- 2 g. 
   *  You call the function as follows: setAccOffsets(xMin,xMax,yMin,yMax,zMin,zMax);
   *  The parameters are floats. 
   *  The calibration changes the slope / ratio of raw acceleration vs g. The zero point is 
   *  set as (min + max)/2.
   */
  myIMU.setAccOffsets(-16330.0, 16450.0, -16600.0, 16180.0, -16520.0, 16690.0);
    
  /*  The starting point, if you position the ICM20948 flat, is not necessarily 0g/0g/1g for x/y/z. 
   *  The autoOffset function measures offset. It assumes your ICM20948 is positioned flat with its 
   *  x,y-plane. The more you deviate from this, the less accurate will be your results.
   *  It overwrites the zero points of setAccOffsets, but keeps the correction of the slope.
   *  The function also measures the offset of the gyroscope data. The gyroscope offset does not   
   *  depend on the positioning.
   *  This function needs to be called after setAccOffsets but before other settings since it will 
   *  overwrite settings!
   */
//  Serial.println("Position your ICM20948 flat and don't move it - calibrating...");
//  delay(1000);
//  myIMU.autoOffsets();
//  Serial.println("Done!"); 
  
  /*  The gyroscope data is not zero, even if you don't move the ICM20948. 
   *  To start at zero, you can apply offset values. These are the gyroscope raw values you obtain
   *  using the +/- 250 degrees/s range. 
   *  Use either autoOffset or setGyrOffsets, not both.
   */
  myIMU.setGyrOffsets(-115.0, 130.0, 105.0);
  
  
  /* enables or disables the acceleration sensor, default: enabled */
  //myIMU.enableAcc(false);

  /*  ICM20948_ACC_RANGE_2G      2 g   (default)
   *  ICM20948_ACC_RANGE_4G      4 g
   *  ICM20948_ACC_RANGE_8G      8 g   
   *  ICM20948_ACC_RANGE_16G    16 g
   */
  myIMU.setAccRange(ICM20948_ACC_RANGE_2G);
  
  /*  Choose a level for the Digital Low Pass Filter or switch it off.  
   *  ICM20948_DLPF_0, ICM20948_DLPF_2, ...... ICM20948_DLPF_7, ICM20948_DLPF_OFF 
   *  
   *  DLPF       3dB Bandwidth [Hz]      Output Rate [Hz]
   *    0              246.0               1125/(1+ASRD) 
   *    1              246.0               1125/(1+ASRD)
   *    2              111.4               1125/(1+ASRD)
   *    3               50.4               1125/(1+ASRD)
   *    4               23.9               1125/(1+ASRD)
   *    5               11.5               1125/(1+ASRD)
   *    6                5.7               1125/(1+ASRD) 
   *    7              473.0               1125/(1+ASRD)
   *    OFF           1209.0               4500
   *    
   *    ASRD = Accelerometer Sample Rate Divider (0...4095)
   *    You achieve lowest noise using level 6  
   */
  myIMU.setAccDLPF(ICM20948_DLPF_1);    
  
  /*  Acceleration sample rate divider divides the output rate of the accelerometer.
   *  Sample rate = Basic sample rate / (1 + divider) 
   *  It can only be applied if the corresponding DLPF is not off!
   *  Divider is a number 0...4095 (different range compared to gyroscope)
   *  If sample rates are set for the accelerometer and the gyroscope, the gyroscope
   *  sample rate has priority.
   */
  myIMU.setAccSampleRateDivider(4095);
  
  /* enables or disables the gyroscope sensor, default: enabled */
  myIMU.enableGyr(false);

  /*  ICM20948_GYRO_RANGE_250       250 degrees per second (default)
   *  ICM20948_GYRO_RANGE_500       500 degrees per second
   *  ICM20948_GYRO_RANGE_1000     1000 degrees per second
   *  ICM20948_GYRO_RANGE_2000     2000 degrees per second
   */
 // myIMU.setGyrRange(ICM20948_GYRO_RANGE_250);
  
  /*  Choose a level for the Digital Low Pass Filter or switch it off. 
   *  ICM20948_DLPF_0, ICM20948_DLPF_2, ...... ICM20948_DLPF_7, ICM20948_DLPF_OFF 
   *  
   *  DLPF       3dB Bandwidth [Hz]      Output Rate [Hz]
   *    0              196.6               1125/(1+GSRD) 
   *    1              151.8               1125/(1+GSRD)
   *    2              119.5               1125/(1+GSRD)
   *    3               51.2               1125/(1+GSRD)
   *    4               23.9               1125/(1+GSRD)
   *    5               11.6               1125/(1+GSRD)
   *    6                5.7               1125/(1+GSRD) 
   *    7              361.4               1125/(1+GSRD)
   *    OFF          12106.0               9000
   *    
   *    GSRD = Gyroscope Sample Rate Divider (0...255)
   *    You achieve lowest noise using level 6  
   */
  myIMU.setGyrDLPF(ICM20948_DLPF_1);  
  
  /*  Gyroscope sample rate divider divides the output rate of the gyroscope.
   *  Sample rate = Basic sample rate / (1 + divider) 
   *  It can only be applied if the corresponding DLPF is not OFF!
   *  Divider is a number 0...255
   *  If sample rates are set for the accelerometer and the gyroscope, the gyroscope
   *  sample rate has priority.
   */
  myIMU.setGyrSampleRateDivider(255);

  /* Set the interrupt pin:
   * ICM20948_ACT_LOW  = active-low
   * ICM20948_ACT_HIGH = active-high (default) 
   */
   //myIMU.setIntPinPolarity(ICM20948_ACT_LOW);

   /*  If latch is enabled the interrupt pin level is held until the interrupt status 
   *  is cleared. If latch is disabled the interrupt pulse is ~50µs (default).
   */
   myIMU.enableIntLatch(true);

  /* The interrupts ICM20948_FSYNC_INT, ICM20948_WOM_INT and ICM20948_DMP_INT can be 
   * cleared by any read or will only be cleared if the interrupt status register is 
   * read (default).
   */
   //myIMU.enableClearIntByAnyRead(true);

  /* Set the FSync interrupt pin:
   *  ICM20948_ACT_LOW  = active-low
   *  ICM20948_ACT_HIGH = active-high (default) 
   */
   //myIMU.setFSyncIntPinPolarity(ICM20948_ACT_LOW);

   /* The following interrupts can be enabled or disabled:
    *  ICM20948_FSYNC_INT        FSYNC pin interrupt, can't propagate to the INT pin  
    *  ICM20948_WOM_INT          Wake on motion
    *  ICM20948_DATA_READY_INT   New data available
    *  ICM20948_FIFO_OVF_INT     FIFO overflow
    */
    myIMU.enableInterrupt(ICM20948_DATA_READY_INT);
    //myIMU.disableInterrupt(ICM20948_DATA_READY_INT);
  
  dataReady = false;
  attachInterrupt(digitalPinToInterrupt(intPin), dataReadyISR, RISING);
  myIMU.readAndClearInterrupts();
  
}

void loop() {
  if(dataReady){
    byte source = myIMU.readAndClearInterrupts();
    if(myIMU.checkInterrupt(source, ICM20948_DATA_READY_INT)){
      Serial.println("Interrupt Type: Data Ready");
      printData();
    }
    dataReady = false;
    myIMU.readAndClearInterrupts(); // if additional interrupts have occured in the meantime
  }
}

void printData(){
  myIMU.readSensor();
  xyzFloat gValue = myIMU.getGValues();
  xyzFloat gyrValue = myIMU.getGyrValues();
      
  Serial.println("g-values (x,y,z):");
  Serial.print(gValue.x);
  Serial.print("   ");
  Serial.print(gValue.y);
  Serial.print("   ");
  Serial.println(gValue.z);

//  Uncomment after you have enabled the gyroscope
//  Serial.println("Gyroscope (x,y,z):");
//  Serial.print(gyrValue.x);
//  Serial.print("   ");
//  Serial.print(gyrValue.y);
//  Serial.print("   ");
//  Serial.println(gyrValue.z);

  Serial.println();
}

void dataReadyISR() {
  dataReady = true;
}
