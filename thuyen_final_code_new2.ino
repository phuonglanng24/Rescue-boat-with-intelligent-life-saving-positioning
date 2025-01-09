#include "esp_camera.h"
#include <Arduino.h>
#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <iostream>
#include <sstream>
#include <ESP32_Servo.h>
#include <SPIFFS.h>
#include <TinyGPSPlus.h>
#define servo_Pin 13
#define esc_Pin 15

#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27
#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22

#define MIN_PULSE_LENGTH 1000
#define MAX_PULSE_LENGTH 2000

const int PWMLightChannel = 3;
int servo_Pos = 75;
int esc_Pos = 75;

const char* ssid = "Xuong STEM2";
const char* password = "aaaaaaaa";
#define MIN_PULSE_LENGTH 1000 // Minimum pulse length in µs
#define MAX_PULSE_LENGTH 2000 // Maximum pulse length in µsServo //esc;
int i; 
TinyGPSPlus gps;
Servo servo;
Servo servo2;
WiFiServer serverread(23);
AsyncWebServer server(80);
AsyncWebSocket wsCamera("/Camera");
AsyncWebSocket wsCarInput("/CarInput");
/*-----------------------*/
void forward() {
 servo.write(100);
digitalWrite(14, HIGH);
}
void stop() {
  digitalWrite(14, LOW);
}
void turnLeft() { 
  servo.write(10);
}
void turnRight() {
  servo.write(180);
}
/*-----------------------*/
void setupCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_4;
  config.ledc_timer = LEDC_TIMER_2;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  config.frame_size = FRAMESIZE_VGA;
  config.jpeg_quality = 10;
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  if (psramFound()) {
    heap_caps_malloc_extmem_enable(20000);
    Serial.printf("PSRAM initialized. malloc to take memory from psram above this size");
  }
}
HardwareSerial GPS(1);
int dem=0;
int pos;
void test()
{
    for (int i = MIN_PULSE_LENGTH; i <= MAX_PULSE_LENGTH; i += 5) {
        Serial.print("Pulse length = ");
        Serial.println(i);
        
        //esc.writeMicroseconds(i);

        
        delay(200);
    }

    Serial.println("STOP");
    //esc.writeMicroseconds(MIN_PULSE_LENGTH);

}
static void smartDelay(unsigned long ms) {
  unsigned long start = millis();
  do {
    while (GPS.available())
      gps.encode(GPS.read());
  } while (millis() - start < ms);
}
/*-----------------------*/
void reconnect() {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.print("Attempting to reconnect to WiFi...");
        WiFi.disconnect();
        WiFi.begin(ssid, password);
        unsigned long startAttemptTime = millis();

        // Chờ tối đa 5 giây để kết nối lại
        while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < 5000) {
            delay(100);
        }
    }
}
void setup() {
  Serial.begin(115200);
 pinMode(14, OUTPUT);
//  servo.setPeriodHertz(50);  //--> // Standard 50hz servo
//  //esc.setPeriodHertz(50);    //--> // Standard 50hz servo
  servo.attach(servo_Pin);
    servo2.attach(4);
  //esc.attach(15, MIN_PULSE_LENGTH, MAX_PULSE_LENGTH);
  WiFi.begin(ssid, password);
  WiFi.setSleep(false); // Tắt chế độ tiết kiệm năng lượng
 GPS.begin(9600, SERIAL_8N1, 15, 2); //TX = 2, RX=15
 smartDelay(1000);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  IPAddress IP = WiFi.softAPIP();

  Serial.print("AP IP address: ");
  Serial.println(WiFi.localIP());

  if (!SPIFFS.begin(true)) {
    Serial.println("An Error has occurred while mounting SPIFFS");
    return;
  }

  server.on("/image", HTTP_GET, [](AsyncWebServerRequest* request) {
    camera_fb_t* fb = esp_camera_fb_get();
    if (fb) {
      request->send_P(200, "image/jpeg", fb->buf, fb->len);
      esp_camera_fb_return(fb);
    }
  });

  server.begin();
  Serial.println("HTTP server started");

  serverread.begin();

  setupCamera();
}

void loop() {
  WiFiClient client = serverread.available();
   if (WiFi.status() != WL_CONNECTED) {
        reconnect();
    }
  if (client) {
    Serial.print("New Client.");
    Serial.println(serverread.available());
    String currentLine = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();

        // Serial.write(c);

        if (c == 'F') {
   
          Serial.println("Đi thẳng");
          forward();
        } else if (c == 'S') {
          Serial.println("Dừng");
          stop();
        } else if (c == 'L') {
          Serial.println("Trái");
          turnLeft();
        } else if (c == 'R') {
          Serial.println("Phải");
          turnRight();
        }
         else if (c == 'A') {
          Serial.println("mo");
          servo2.write(10);
        }
          else if (c == 'B') {
          Serial.println("dong");
          servo2.write(180);
        }
      }
        dem=dem+1;
  //Serial.println(dem);
  if(dem>=2000)
    {
      if (gps.location.isValid())
  {
        Serial.println("gps.");
    String dataToSend = String(gps.location.lat(), 6)+ "," + String(gps.location.lng(), 6);
  client.println(dataToSend);
  Serial.println("Đã gửi dữ liệu đến server: " + dataToSend);
  dem=0;
  }
  }
    }
  }
}
//void loop()
//{
//  // This sketch displays information every time a new sentence is correctly encoded.
//  while (GPS.available() > 0)
//    if (gps.encode(GPS.read()))
//      displayInfo();
//
//  if (millis() > 5000 && gps.charsProcessed() < 10)
//  {
//    Serial.println(F("No GPS detected: check wiring."));
//    while(true);
//  }
//}
//
//void displayInfo()
//{
//  Serial.print(F("Location: ")); 
//  if (gps.location.isValid())
//  {
//    Serial.print(gps.location.lat(), 6);
//    Serial.print(F(","));
//    Serial.print(gps.location.lng(), 6);
//  }
//  else
//  {
//    Serial.print(F("INVALID"));
//  }
//
//  Serial.print(F("  Date/Time: "));
//  if (gps.date.isValid())
//  {
//    Serial.print(gps.date.month());
//    Serial.print(F("/"));
//    Serial.print(gps.date.day());
//    Serial.print(F("/"));
//    Serial.print(gps.date.year());
//  }
//  else
//  {
//    Serial.print(F("INVALID"));
//  }
//
//  Serial.print(F(" "));
//  if (gps.time.isValid())
//  {
//    if (gps.time.hour() < 10) Serial.print(F("0"));
//    Serial.print(gps.time.hour());
//    Serial.print(F(":"));
//    if (gps.time.minute() < 10) Serial.print(F("0"));
//    Serial.print(gps.time.minute());
//    Serial.print(F(":"));
//    if (gps.time.second() < 10) Serial.print(F("0"));
//    Serial.print(gps.time.second());
//    Serial.print(F("."));
//    if (gps.time.centisecond() < 10) Serial.print(F("0"));
//    Serial.print(gps.time.centisecond());
//  }
//  else
//  {
//    Serial.print(F("INVALID"));
//  }
//
//  Serial.println();
//}
