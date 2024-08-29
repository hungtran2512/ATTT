#include <SoftwareSerial.h>
#include <SD.h>

SoftwareSerial mySerial(2, 3); // RX nối với TX (lora), TX - RX (lora)
#define SCALE_RX 10 // Chân RX nối với cân
#define SCALE_TX 11 // Chân TX nối với cân
#define SD_CS 4 // Chân CS của module thẻ nhớ SD

SoftwareSerial scaleSerial(SCALE_RX, SCALE_TX); // Giao tiếp với cân

File logFile;

void setup()
{
  Serial.begin(9600); // Khởi tạo giao tiếp với máy tính
  mySerial.begin(9600); // Khởi tạo giao tiếp với module LoRa
  scaleSerial.begin(9600); // Khởi tạo giao tiếp với cân

  // Khởi tạo thẻ nhớ SD
  if (!SD.begin(SD_CS)) {
    Serial.println("Lỗi khởi tạo thẻ SD!");
    return;
  }
  
  // Mở file log
  logFile = SD.open("log.txt", FILE_WRITE);
  if (!logFile) {
    Serial.println("Không thể mở file log!");
    return;
  }
}

void loop()
{
  /*
    Đọc dữ liệu từ cân
    Gửi dữ liệu đi bằng UART LoRa
  */
  if (scaleSerial.available() > 0)
  {
    String inputWeight = "";
    inputWeight = scaleSerial.readStringUntil('\n'); // Đọc dữ liệu từ cân cho đến khi gặp ký tự xuống dòng
    if (inputWeight != "")
    {
      inputWeight.trim(); // Loại bỏ khoảng trắng đầu và cuối
      Serial.println(inputWeight); // In dữ liệu ra màn hình Serial Monitor
      mySerial.println(inputWeight); // Gửi dữ liệu qua module LoRa

      // Ghi dữ liệu vào file log
      if (logFile) {
        logFile.println(inputWeight);
        logFile.flush(); // Đảm bảo dữ liệu được ghi ngay lập tức
      }
    }
  }

  /*
    Nhận dữ liệu từ LoRa (UART: RX, TX)
    In ra màn hình Serial
  */
  if (mySerial.available() > 0)
  {
    String inputReceive = mySerial.readStringUntil('\n'); // Đọc dữ liệu từ LoRa

    if (inputReceive != "")
    {
      inputReceive.trim(); // Loại bỏ khoảng trắng đầu và cuối
      Serial.println(inputReceive); // In dữ liệu ra màn hình Serial Monitor
    }
  }
  delay(20); // Đợi 20 mili giây
}
