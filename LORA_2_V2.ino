#include <SoftwareSerial.h>
// Thiết lập giao tiếp UART với module Lora (RX chân 2, TX chân 3)
SoftwareSerial mySerial(2, 3); 

// Định nghĩa chân M0, M1 để điều chỉnh chế độ của Lora (không sử dụng trong đoạn code này)
#define M0 8
#define M1 9

// Định nghĩa chân điều khiển đèn LED
#define LED 13 

void setup()
{
  // Khởi tạo Serial Monitor (giao tiếp với máy tính) và Lora với tốc độ 9600 baud
  Serial.begin(9600);
  mySerial.begin(9600);
  
  // Cấu hình chân LED làm đầu ra, tắt đèn LED khi khởi động
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
}

void loop()
{
  /*
     Đọc dữ liệu từ máy tính thông qua Serial Monitor
     Gửi dữ liệu nhận được từ máy tính qua Lora
  */
  if (Serial.available() > 0) // Kiểm tra nếu có dữ liệu nhập từ máy tính
  {
    String inputSend = ""; 
    inputSend = Serial.readStringUntil('\n'); // Đọc dữ liệu nhập từ Serial Monitor
    mySerial.println(inputSend); // Gửi dữ liệu qua Lora
  }

  /*
     Nhận dữ liệu từ module Lora qua giao tiếp UART
     Hiển thị dữ liệu nhận được trên Serial Monitor
     Điều khiển LED nếu nhận được lệnh "on" hoặc "off"
  */
  if (mySerial.available() > 1) // Kiểm tra nếu có dữ liệu từ Lora
  {
    String inputReceive = mySerial.readStringUntil('\n'); // Đọc dữ liệu từ Lora

    if (inputReceive != "") // Nếu dữ liệu nhận không rỗng
    {
      inputReceive.trim(); // Xóa khoảng trắng thừa nếu có
      Serial.println(inputReceive); // Hiển thị dữ liệu trên Serial Monitor
      
      // Kiểm tra dữ liệu và điều khiển LED
      if (inputReceive == "on") 
      {
        digitalWrite(LED, HIGH); // Bật LED nếu nhận lệnh "on"
      }
      else if (inputReceive == "off")
      {
        digitalWrite(LED, LOW); // Tắt LED
