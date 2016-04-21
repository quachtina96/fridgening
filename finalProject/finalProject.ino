#include <math.h>
#include <Wire.h>
#include <SPI.h>
#include <ESP8266.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>


// Wifi options, constants, and variables
#define VERBOSE_WIFI true          // Verbose ESP8266 output
#define IOT true
#define IOT_UPDATE_INTERVAL 10000  // How often to send/pull from cloud (ms)
#define SSID "MIT"               // PUT SSID HERE
#define PASSWORD ""         // PUT PASSWORD HERE
//#define SSID "6S08C"               // PUT SSID HERE
//#define PASSWORD "6S086S08"         // PUT PASSWORD HERE
const String KERBEROS = "brendaz";  // PUT KERBEROS HERE
uint32_t tLastIotReq = 0;       // time of last send/pull
uint32_t tLastIotResp = 0;      // time of last response
String MAC = "";
String resp = "";

// Display constants, and variables
#define DISPLAY_UPDATE_INTERVAL 100  // How often to update display (ms)
uint32_t tLastDisplayUpdate = 0;     // time of last display update


void setup() 
{
  // Display setup
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.display();
  delay(250);
  display.clearDisplay();
  display.setCursor(0,0);
  display.setTextSize(1);
  display.setTextColor(WHITE);

  //Serial Monitor
  Serial.begin(115200);

  // Wifi setup
  if (IOT) {
    wifi.begin();
    display.clearDisplay();
    display.setCursor(0,0);
    display.println("Connecting to:");
    display.println(SSID);
    display.display();
    wifi.connectWifi(SSID, PASSWORD);
    while (!wifi.isConnected()); //wait for connection
    MAC = wifi.getMAC();
    display.clearDisplay();
    display.setCursor(0,0);
    display.println("Connected!!");
    display.display();
    delay(1000);
  }
}


void loop() 
{
  
  if (millis() - tLastDisplayUpdate >= DISPLAY_UPDATE_INTERVAL) { //Update OLED periodically
    updateDisplay();
    tLastDisplayUpdate = millis();
  }

  if (IOT && wifi.hasResponse()) {
    resp = wifi.getResponse();
    tLastIotResp = millis();
    if (wifi.isConnected() && !wifi.isBusy()) { //Check if we can send request
      Serial.print("Sending request at t=");
      Serial.println(millis());
      Serial.print("wifi.getResponse()" );
      Serial.println(wifi.getResponse());
      String domain = "iesc-s2.mit.edu";
      int port = 80;
      String path = "/student_code/" + KERBEROS + "/lab05/L05B.py";
      String getParams = "&lat=" + String(GPS.latitudeDegrees,6)
        + "&lon=" + String(GPS.longitudeDegrees,6)
        + "&heading=" + String(compass.heading);

      wifi.sendRequest(GET, domain, port, path, getParams);
      tLastIotReq = millis();
    }
  }

}

void updateDisplay() {  
    display.clearDisplay();
    display.setCursor(0,0);
    display.setTextSize(1);
    display.print("Heading: ");
    display.println(compass.heading);
    display.print("Resp at t=");
    display.println(tLastIotResp);
    int htmlStartIndex = resp.indexOf("<html>");
    int htmlEndIndex = resp.indexOf("</html>", htmlStartIndex);
    if (htmlStartIndex != -1 && htmlEndIndex != -1) {
      display.println(resp.substring(htmlStartIndex+6, htmlEndIndex));
    } else {
      display.println("No response");
    }
    display.display();
}


