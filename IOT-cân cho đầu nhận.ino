#include <LoRa.h>
#include <SPI.h>
#include <SD.h>

// Cấu hình chân cho mô-đun thẻ SD
const int chipSelect = 4;  // Chân kết nối với CS của mô-đun thẻ SD

void setup() {
  Serial.begin(9600);  // Khởi động Serial Monitor

  // Khởi động thẻ SD
  if (!SD.begin(chipSelect)) {
    Serial.println("Khởi động thẻ SD thất bại!");
    while (1);  // Dừng chương trình nếu khởi động thẻ SD thất bại
  }
  Serial.println("Khởi động thẻ SD thành công!");

  // Khởi động LoRa
  if (!LoRa.begin(433E6)) {  // Cài đặt tần số là 433 MHz
    Serial.println("Khởi động LoRa thất bại!");
    while (1);  // Dừng chương trình nếu khởi động LoRa thất bại
  }
  Serial.println("Khởi động LoRa thành công!");
}

void loop() {
  // Thử phân tích gói dữ liệu từ LoRa
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // Đọc gói dữ liệu
    String receivedData = "";
    while (LoRa.available()) {
      receivedData += (char)LoRa.read();
    }
    Serial.print("Nhận được dữ liệu: ");
    Serial.println(receivedData);

    // Chuyển đổi dữ liệu nhận được sang kiểu số nguyên (giả sử là giá trị số cân)
    long weight = receivedData.toInt();
    
    // Mở file để ghi dữ liệu
    File dataFile = SD.open("weightData.txt", FILE_WRITE);
    if (dataFile) {
      dataFile.println(weight);  // Ghi trọng lượng vào file
      dataFile.close();  // Đóng file để lưu dữ liệu
      Serial.println("Đã ghi dữ liệu vào file weightData.txt.");
    } else {
      Serial.println("Không thể mở file để ghi dữ liệu.");
    }
  }

  delay(1000);  // Dừng 1 giây trước khi thực hiện lại vòng lặp
}
