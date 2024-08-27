#include <SoftwareSerial.h>
SoftwareSerial mySerial(2, 3); //RX nối với TX(lora), TX - RX(lora)

#define M0 8
#define M1 9
#define LED 13
// M0, M1 đấu với gnd: Normal mode

void setup()
{
  Serial.begin(9600);
  mySerial.begin(9600);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
}

void loop()
{
  /*
     Đọc dữ liệu  từ cổng Serial monitor
     Gửi dữ liệu đi bằng uart Lora
  */
  if (Serial.available() > 0)
  {
    String inputSend = "";
    inputSend = Serial.readStringUntil('\n');
    mySerial.println(inputSend);
  }

  /*
     nhận dữ liệu từ lora(uart: rx, tx)
     in ra màn hình Serial
  */
  if (mySerial.available() > 1)
  {
    String inputReceive = mySerial.readStringUntil('\n');

    if (inputReceive != "")
    {
      inputReceive.trim();
      Serial.println(inputReceive);
      if (inputReceive == "on")
      {
        digitalWrite(LED, HIGH);
      }
      else if (inputReceive == "off")
      {
        digitalWrite(LED, LOW);
      }
      inputReceive = "";
    }
  }
  delay(20);
}
