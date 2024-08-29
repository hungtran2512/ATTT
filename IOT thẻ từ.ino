#include <SPI.h>
#include <MFRC522.h>
#include <LoRa.h>

// Định nghĩa chân kết nối với module RFID
#define SS_PIN 10
#define RST_PIN 9

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Khởi tạo đối tượng RFID

void setup() {
  Serial.begin(9600);   // Khởi động Serial Monitor để kiểm tra
  SPI.begin();          // Khởi động giao tiếp SPI

  // Khởi động module RFID
  mfrc522.PCD_Init();
  Serial.println("Đang chờ thẻ từ...");

  // Khởi động module LoRa tại tần số 433E6 (433 MHz)
  if (!LoRa.begin(433E6)) {
    Serial.println("Khởi động LoRa thất bại!");
    while (1);
  }
  Serial.println("Khởi động LoRa thành công.");
}

void loop() {
  // Kiểm tra xem có thẻ từ nào gần đó không
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    Serial.println("Thẻ từ đã được phát hiện.");

    // Lấy ID của thẻ từ (UID)
    String cardID = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      cardID += String(mfrc522.uid.uidByte[i], HEX);
    }
    Serial.print("UID của thẻ từ: ");
    Serial.println(cardID);

    // Gửi dữ liệu UID qua LoRa
    LoRa.beginPacket();
    LoRa.print(cardID);
    LoRa.endPacket();
    Serial.println("Dữ liệu UID đã được gửi qua LoRa.");

    // Dừng module RFID để tiết kiệm năng lượng (tùy chọn)
    mfrc522.PICC_HaltA();
  }

  delay(1000); // Đợi 1 giây trước khi quét lần tiếp theo
}
