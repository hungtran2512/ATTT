#include <SoftwareSerial.h>
// Thiết lập giao tiếp UART với module Lora (RX chân 2, TX chân 3)
SoftwareSerial mySerial(2, 3); 

// Định nghĩa chân M0, M1 để điều chỉnh chế độ của module Lora (không sử dụng trong code)
#define M0 8
#define M1 9

// Định nghĩa chân điều khiển đèn LED
#define LED 13 

void setup()
{
  // Khởi tạo Serial Monitor để giao tiếp với máy tính và Lora
  Serial.begin(9600);
  mySerial.begin(9600);

  // Thiết lập chân LED làm đầu ra và tắt đèn LED ban đầu
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
}

void loop()
{
  /*
     Đọc dữ liệu từ Serial Monitor (máy tính) và gửi qua Lora
  */
  if (Serial.available() > 0) // Nếu có dữ liệu nhập từ máy tính
  {
    String inputSend = "";
    inputSend = Serial.readStringUntil('\n'); // Đọc dữ liệu cho đến khi gặp ký tự xuống dòng
    mySerial.println(inputSend); // Gửi dữ liệu qua Lora
  }

  /*
     Nhận dữ liệu từ Lora và in ra Serial Monitor
     Điều khiển đèn LED dựa trên dữ liệu nhận được ("on" hoặc "off")
  */
  if (mySerial.available() > 1) // Nếu có dữ liệu từ Lora
  {
    String inputReceive = mySerial.readStringUntil('\n'); // Đọc chuỗi dữ liệu từ Lora

    if (inputReceive != "") // Nếu nhận được dữ liệu không rỗng
    {
      inputReceive.trim(); // Xóa khoảng trắng
      Serial.println(inputReceive); // In dữ liệu nhận được lên Serial Monitor

      // Bật hoặc tắt đèn LED dựa trên dữ liệu nhận được
      if (inputReceive == "on") 
      {
        digitalWrite(LED, HIGH); // Bật đèn LED
      }
      else if (inputReceive == "off")
      {
        digitalWrite(LED, LOW); // Tắt đèn LED
      }

      inputReceive = ""; // Xóa chuỗi sau khi xử lý
    }
  }

  delay(20); // Dừng 20ms để tránh xử lý quá nhanh
}
