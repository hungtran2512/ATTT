#include <SoftwareSerial.h>
#include <LiquidCrystal_I2C.h>

SoftwareSerial mySerial(2, 3); //RX nối với TX(lora), TX - RX(lora)
// M0, M1 đấu với gnd: Normal mode

LiquidCrystal_I2C lcd(0x27, 16, 2); // địa chỉ I2C của LCD và kích thước của LCD


void setup()
{
  Serial.begin(9600);
  mySerial.begin(9600);
  lcd.init(); // Khởi tạo LCD
  lcd.backlight(); // Bật đèn nền LCD
  lcd.setCursor(3, 0);
  lcd.print("DHT11 LORA");
  lcd.setCursor(0, 1);
  lcd.print("LONG AUTOMATION !");
  delay(2000);
}

void loop()
{

  /*
     nhận dữ liệu từ lora(uart: rx, tx)
     in ra màn hình Serial
  */
  lcd.clear(); // Xóa màn hình LCD
  String inputReceive = "";
  if (mySerial.available() > 0)
  {
    inputReceive = mySerial.readStringUntil('\n');
    Serial.println(inputReceive);
    
  }
  //lcd
  lcd.setCursor(1, 0);
  lcd.print("Temp and Humi: ");
  lcd.setCursor(2, 1);
  lcd.print(inputReceive);
  delay(1000);
}
