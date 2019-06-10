/*
  UDPSendReceive.pde:
  This sketch receives UDP message strings, prints them to the serial port
  and sends an "acknowledge" string back to the sender

  A Processing sketch is included at the end of file that can be used to send
  and received messages for testing with a computer.

  created 21 Aug 2010
  by Michael Margolis

  This code is in the public domain.

  adapted from Ethernet library examples
*/

//EL BUENO


#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#ifndef STASSID
#define STASSID "Especial_MCHP"
//#define STASSID "LSEL"
#define STAPSK  "M15SEB304"
#endif


unsigned int localPort = 8080;      // local port to listen on

// buffers for receiving and sending data
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet,

byte mac[6];
WiFiUDP Udp;

void pitido(uint8_t _pin, unsigned int frequency, unsigned long duration) {
  pinMode (_pin, OUTPUT );
  analogWriteFreq(frequency);
  analogWrite(_pin,500);
  delay(duration);
  analogWrite(_pin,0);
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(STASSID, STAPSK);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
  Serial.printf("UDP server on port %d\n", localPort);
  WiFi.macAddress(mac);
  Serial.print("MAC: ");
  Serial.print(mac[5],HEX);
  Serial.print(mac[4],HEX);
  Serial.print(mac[3],HEX);
  Serial.print(mac[2],HEX);
  Serial.print(mac[1],HEX);
  Serial.println(mac[0],HEX);
  Udp.begin(localPort);

}

void loop() {
  //pitido(4,440,5000);
  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    Serial.print("Received packet of size ");
    Serial.println(packetSize);
    Serial.print("From ");
    IPAddress remote = Udp.remoteIP();
    for (int i = 0; i < 4; i++) {
      Serial.print(remote[i], DEC);
      if (i < 3) {
        Serial.print(".");
      }
    }
    Serial.print(", port ");
    Serial.println(Udp.remotePort());

    // read the packet into packetBufffer
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    Serial.println("Contents:");
    Serial.println(packetBuffer);

  if(packetBuffer[0]=='1'){
    pitido(4,880,5000);
  }

  }
  delay(10);

/*if(packetBuffer=="1"){
    pitido(4,440,5000);
}*/

}

/*
  test (shell/netcat):
  --------------------
	  nc -u 192.168.esp.address 8888
*/
