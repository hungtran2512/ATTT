#include <SoftwareSerial.h> // Thư viện hỗ trợ giao tiếp UART với các chân tùy chọn
#include <LiquidCrystal_I2C.h> // Thư viện hỗ trợ giao tiếp với màn hình LCD qua I2C

// Khởi tạo giao tiếp UART với module Lora trên chân 2 (RX) và 3 (TX)
SoftwareSerial mySerial(2, 3); 

// Khởi tạo màn hình LCD có địa chỉ I2C 0x27, kích thước 16 cột, 2 hàng
LiquidCrystal_I2C lcd(0x27, 16, 2); 

void setup()
{
  Serial.begin(9600); // Khởi tạo Serial Monitor (giao tiếp với máy tính) với tốc độ 9600 baud
  mySerial.begin(9600); // Khởi tạo giao tiếp UART với Lora ở tốc độ 9600 baud
  lcd.init(); // Khởi tạo màn hình LCD
  lcd.backlight(); // Bật đèn nền của màn hình LCD
  
  // Hiển thị thông báo khởi động trên LCD
  lcd.setCursor(3, 0); // Đặt con trỏ tại cột 3, hàng 0
  lcd.print("DHT11 LORA"); // Hiển thị dòng chữ "DHT11 LORA"
  
  lcd.setCursor(0, 1); // Đặt con trỏ tại cột 0, hàng 1
  lcd.print("LONG AUTOMATION !"); // Hiển thị dòng chữ "LONG AUTOMATION!"
  
  delay(2000); // Dừng chương trình trong 2 giây để người dùng có thể thấy thông điệp trên LCD
}

void loop()
{
  lcd.clear(); // Xóa màn hình LCD
  
  String inputReceive = ""; // Biến lưu trữ dữ liệu nhận được từ Lora
  
  // Kiểm tra nếu có dữ liệu từ Lora gửi đến
  if (mySerial.available() > 0)
  {
    inputReceive = mySerial.readStringUntil('\n'); // Đọc chuỗi dữ liệu từ Lora cho đến khi gặp ký tự xuống dòng ('\n')
    Serial.println(inputReceive); // In dữ liệu nhận được lên Serial Monitor (trên máy tính) để giám sát
  }
  
  // Hiển thị dữ liệu nhiệt độ và độ ẩm lên LCD
  lcd.setCursor(1, 0); // Đặt con trỏ tại cột 1, hàng 0
  lcd.print("Temp and Humi: "); // Hiển thị dòng chữ "Temp and Humi: "
  
  lcd.setCursor(2, 1); // Đặt con trỏ tại cột 2, hàng 1
  lcd.print(inputReceive); // Hiển thị dữ liệu nhận được từ Lora (nhiệt độ và độ ẩm)
  
  delay(1000); // Dừng chương trình trong 1 giây trước khi cập nhật dữ liệu tiếp theo
}
