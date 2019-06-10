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


#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
//#include <Packetizer.h>

#ifndef STASSID
#define STASSID "Especial_MCHP"
//#define STASSID "LSEL"
#define STAPSK  "M15SEB304"
#endif


unsigned int localPort = 5000;      // local port to listen on

unsigned int state=0;

// buffers for receiving and sending data
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet,
char  ReplyBuffer[] = "acknowledged\r\n";       // a string to send back

byte mac[6];

WiFiUDP Udp;

//Packetizer::Packer packer;

void setup() {
  pinMode(16,INPUT);
  pinMode(2,OUTPUT);
  
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
  char msg[10];
  sprintf(msg, "%0x%0x1\r\n", mac[1], mac[0]);

  if (digitalRead(16) && state==0){
    state=1;       
    digitalWrite(2,LOW);
    //packer << mac[0] << mac[1] << 1 << Packetizer::endp();
    //Serial.write(packer.data(), packer.size());;
    msg[4] = '1';
    Udp.beginPacket("172.16.3.42", 5000); //direccion depende del ordenador
    Udp.write(msg);
    Serial.write(msg);
    Udp.endPacket();
  }
  else if (!digitalRead(16) && state==1){
    state=0;
    digitalWrite(2,HIGH);
    Udp.beginPacket("172.16.3.42", 5000); //direccion depende del ordenador
    msg[4] = '0';
    Udp.write(msg);
    Serial.write(msg);
    Udp.endPacket();
  }
  delay(1000);
}

/*
  test (shell/netcat):
  --------------------
    nc -u 192.168.esp.address 8888
*/
