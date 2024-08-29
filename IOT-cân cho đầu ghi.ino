#include <LoRa.h>
#include <HX711.h>

// Pin kết nối với HX711
const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 3;

// Khởi tạo đối tượng HX711
HX711 scale;

// Địa chỉ LoRa
const int loraAddress = 1;

void setup() {
  Serial.begin(9600);  // Khởi động Serial Monitor
  
  // Khởi động HX711
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  
  // Khởi động LoRa
  if (!LoRa.begin(433E6)) {  // Chọn tần số LoRa là 433 MHz
    Serial.println("Khởi động LoRa thất bại!");
    while (1);
  }
  Serial.println("Khởi động LoRa thành công!");
}

void loop() {
  if (scale.is_ready()) {
    long weight = scale.read(); // Đọc giá trị từ Load Cell
    Serial.print("Trọng lượng: ");
    Serial.println(weight);

    // Chuẩn bị truyền dữ liệu qua LoRa
    LoRa.beginPacket();
    LoRa.print(weight);
    LoRa.endPacket();

    Serial.println("Đã truyền dữ liệu qua LoRa.");
  } else {
    Serial.println("HX711 chưa sẵn sàng.");
  }

  delay(1000); // Dừng 1 giây trước khi đo và truyền lại
}
