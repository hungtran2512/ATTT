#include <SoftwareSerial.h>
SoftwareSerial mySerial(2, 3); //RX nối với TX(lora), TX - RX(lora)
// M0, M1 đấu với gnd: Normal mode
#include <DHT.h>

#define DHTPIN 4 // chân kết nối của cảm biến DHT11
#define DHTTYPE DHT11 // loại cảm biến
DHT dht(DHTPIN, DHTTYPE);

void setup()
{
  Serial.begin(9600);
  mySerial.begin(9600);
  dht.begin(); // Khởi tạo cảm biến DHT11
}

void loop()
{
  float temperature = dht.readTemperature(); // Đọc nhiệt độ từ DHT11
  float humidity = dht.readHumidity(); // Đọc độ ẩm từ DHT11
  
  Serial.println(String(temperature) + "," + String(humidity));
  mySerial.println(String(temperature) + "," + String(humidity));

  delay(1000);
}
