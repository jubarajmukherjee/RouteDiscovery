#include <WiFi.h>
#include <ThingSpeak.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <MQUnifiedsensor.h>
#define WIFI_SSID "Galaxy M31sF579"
#define WIFI_PASSWORD "xnnt3916"
#define THINGSPEAK_API_KEY "BAD6KM1N2AO5MP3M"
#define DHTPIN 4
#define DHTTYPE DHT11
#define RatioMQ135CleanAir 3.6//RS / R0 = 3.6 ppm  
#define measurePin 39 //adc pin of esp32 can be used for analog input
DHT dht(DHTPIN, DHTTYPE);

#define         Board                   ("ESP-32") // Wemos ESP-32 or other board, whatever have ESP32 core.

//https://www.amazon.com/HiLetgo-ESP-WROOM-32-Development-Microcontroller-Integrated/dp/B0718T232Z (Although Amazon shows ESP-WROOM-32 ESP32 ESP-32S, the board is the ESP-WROOM-32D)
#define         Pin                     (36) //check the esp32-wroom-32d.jpg image on ESP32 folder 

/***********************Software Related Macros************************************/
#define         Type                    ("MQ-135") //MQ2 or other MQ Sensor, if change this verify your a and b values.
#define         Voltage_Resolution      (3.3) // 3V3 <- IMPORTANT. Source: https://randomnerdtutorials.com/esp32-adc-analog-read-arduino-ide/
#define         ADC_Bit_Resolution      (12) // ESP-32 bit resolution. Source: https://randomnerdtutorials.com/esp32-adc-analog-read-arduino-ide/
#define         RatioMQ2CleanAir        (3.6) //RS / R0 = 3.6 ppm
/*****************************Globals***********************************************/
MQUnifiedsensor MQ135(Board, Voltage_Resolution, ADC_Bit_Resolution, Pin, Type);





int THINGSPEAK_CHANNEL_ID=2329603;
WiFiClient client;



float calc_SI1(float CO2)
{
 //Molecular weight of CO2 = 44.01 g/mol;
 //conversion of ppm to µg/m3 -https://teesing.com/en/tools/ppm-mg3-converter
 //calculation of sub -index same as that of NH3 as CO2 is not mentioned in cpcb for calculation of AQI
 float c = (float)(CO2 *  44.01/24.45);

 if(c <=200)
 return c * 50/200;
 else if(c >200 && c<=400)
 return 50+(c-200)*50/200;
 else if(c>400 && c<=800)
 return 100+(c-400)*100/400;
 else if (c >800 && c <=1200)
 return 200+(c-800)*(100/400);
 else if(c>1200 && c <=1800)
 return 300+(c-1200)*(100/600);
 else if(c>1800)
 return 400+(c-1800)*(100/600);

}

float calc_SI2(float CO)
{ //Molecular weight for CO = 28.01 g/mol
    //conversion of ppm to mg/m3 - https://teesing.com/en/tools/ppm-mg3-converter
  //calculation of sub -index reference - https://cpcb.nic.in/National-Air-Quality-Index/


  float c = (float)(CO *  28.01/(24.45*1000));

  //finding Sub - Index for Carbon Monoxide according to the calculation methods used in - https://cpcb.nic.in/National-Air-Quality-Index/

  if(c<=1)
  return c*50/1;
  else if(c>1 && c<=2)
  return 50+(c-1)*50/1;
  else if(c>2 && c<=10)
  return 100+(c-2)*100/8;
  else if(c>10 && c<=17)
  return 200+(c-10)*(100/7);
  else if(c>17 && c<=34)
  return 300+(c-17)*(100/17);
  else if (c>34)
  return 400+(c-34)*(100/17);



}
float calc_SI3(float NH3)
{
  //conversion of ppm to µg/m3 - https://teesing.com/en/tools/ppm-mg3-converter
  //calculation of sub -index reference - https://cpcb.nic.in/National-Air-Quality-Index/
 //Molecular Weight for NH3 = 17.03 g/mol
 float c = (float)( NH3 *  17.03 /24.45); //finding concentration in µg/m3

 //finding Sub - Index for Ammonia according to the calculation methods used in - https://cpcb.nic.in/National-Air-Quality-Index/ 

 if(c <=200)
 return c * 50/200;
 else if(c >200 && c<=400)
 return 50+(c-200)*50/200;
 else if(c>400 && c<=800)
 return 100+(c-400)*100/400;
 else if (c >800 && c <=1200)
 return 200+(c-800)*(100/400);
 else if(c>1200 && c <=1800)
 return 300+(c-1200)*(100/600);
 else if(c>1800)
 return 400+(c-1800)*(100/600);
 

}


void setup() {
Serial.begin(115200);
dht.begin();

MQ135.setRegressionMethod(1); //_PPM =  a*ratio^b
MQ135.setA(110.47); MQ135.setB(-2.862); // Configure the equation to to calculate CO2 concentration

  /*
    Exponential regression:
  GAS      | a      | b
  CO       | 605.18 | -3.937  
  Alcohol  | 77.255 | -3.18 
  CO2      | 110.47 | -2.862
  Toluene  | 44.947 | -3.445
  NH3     | 102.2  | -2.473
  Aceton  | 34.668 | -3.369
  */

MQ135.init(); 
Serial.print("Calibrating please wait.");
  float calcR0 = 0;
  for(int i = 1; i<=10; i ++)
  {
    MQ135.update(); // Update data, the arduino will read the voltage from the analog pin
    calcR0 += MQ135.calibrate(RatioMQ135CleanAir);
    Serial.print(".");
  }
  MQ135.setR0(calcR0/10);
  Serial.println("  done!.");
  
  if(isinf(calcR0)) {Serial.println("Warning: Conection issue, R0 is infinite (Open circuit detected) please check your wiring and supply"); while(1);}
  if(calcR0 == 0){Serial.println("Warning: Conection issue found, R0 is zero (Analog pin shorts to ground) please check your wiring and supply"); while(1);}
  /*****************************  MQ CAlibration ********************************************/ 
  MQ135.serialDebug(true);

WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
while (WiFi.status() != WL_CONNECTED) {
delay(1000);
Serial.println("Connecting to WiFi...");
}
}
void loop() {
float humidity = dht.readHumidity();
float temperature = dht.readTemperature();


if (isnan(humidity) || isnan(temperature)) {
Serial.println("Failed to read from DHT sensor!");
delay(1000);
return;
}

  MQ135.update(); // Update data, the arduino will read the voltage from the analog pin
  
  float CO2 = MQ135.readSensor(); // Sensor will read PPM concentration using the model, a and b values set previously or from the setup
  MQ135.setA(605.18); MQ135.setB(-3.937);
  MQ135.update();
  float CO = MQ135.readSensor();
  MQ135.setA(102.2); MQ135.setB(-2.473);
  MQ135.update();
  float NH3 = MQ135.readSensor();
  float SI3 = calc_SI3(NH3);
  float SI2 = calc_SI2(CO);
  float SI1 = calc_SI1(CO2); 
  float AQI = (SI1 + SI2 + SI3)/3 * 100;
  //according to cpcb, the max sub -index is the AQI of a place but here we are taking the average of the sub-indexes.
  //according to cpcb the following gases are used for AQI calculation 
  //SO2
  //NO2
  //CO
  //O3
  //NH3
  //we can find NH3 and CO only using MQ-135, hence we added CO2 in the AQI calculation also.
  // since we need data real time, we are not calculating the 8 hrs average or the 24 hours average or the 16 hour average.
  // we are calculating the current values only.

  //dust concentration calculation
  double read = analogRead(measurePin);
  double voltage = read * 5.0 / 1024.0;
  double dustDensity = voltage * 170 - 0.1;
     Serial.print(" CO2 = ");
     Serial.println(CO2);
     Serial.print(" NH3 = ");
     Serial.println(NH3);
     Serial.print(" CO = ");
     Serial.println(CO);
     Serial.print(" AQI = ");
     Serial.println(AQI);
     Serial.print(" Temperature = ");
     Serial.println(temperature);
     Serial.print(" Humidity = ");
     Serial.println(humidity);
     Serial.print("Dust Density in micrograms per meter cube= ");
     Serial.println(dustDensity);

ThingSpeak.begin(client);

    ThingSpeak.setField(1,temperature);
    ThingSpeak.setField(2,humidity);
    ThingSpeak.setField(3,CO2);
    ThingSpeak.setField(4,CO);
    ThingSpeak.setField(5,NH3);
    ThingSpeak.setField(6,AQI);
    ThingSpeak.setField(7,((float)dustDensity));
   int x = ThingSpeak.writeFields(THINGSPEAK_CHANNEL_ID,THINGSPEAK_API_KEY);
   if(x == 200)
   {
     Serial.println("Upload successful");
     
   }

delay(10000); // Send data every 10 seconds
}