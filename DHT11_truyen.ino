#include <SoftwareSerial.h> // Thư viện hỗ trợ giao tiếp UART
#include <DHT.h> // Thư viện hỗ trợ cảm biến DHT11

// Khởi tạo giao tiếp UART với module Lora (chân 2 RX, chân 3 TX)
SoftwareSerial mySerial(2, 3); 

// Khai báo chân và loại cảm biến DHT11
#define DHTPIN 4 
#define DHTTYPE DHT11 
DHT dht(DHTPIN, DHTTYPE); // Khởi tạo đối tượng cảm biến DHT11

void setup()
{
  Serial.begin(9600); // Khởi tạo Serial Monitor với tốc độ 9600 baud
  mySerial.begin(9600); // Khởi tạo giao tiếp UART với Lora ở 9600 baud
  dht.begin(); // Khởi động cảm biến DHT11
}

void loop()
{
  float temperature = dht.readTemperature(); // Đọc nhiệt độ từ DHT11
  float humidity = dht.readHumidity(); // Đọc độ ẩm từ DHT11
  
  // In nhiệt độ và độ ẩm lên Serial Monitor
  Serial.println(String(temperature) + "," + String(humidity)); 
  
  // Gửi nhiệt độ và độ ẩm qua Lora
  mySerial.println(String(temperature) + "," + String(humidity)); 
  
  delay(1000
