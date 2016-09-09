/*
 ReSpeaker Home Automation Sample using MKR1000
*/

#include <SPI.h>
#include <WiFi101.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

typedef struct {
  char* room;
  int pin;
}PIN;

char ssid[] = "kripa";
char pass[] = "var753ma-/m&=";
int status = WL_IDLE_STATUS;

WiFiClient wifiClient;
PubSubClient client(wifiClient);

PIN pins[] = {
  {"bedroom", 0},
  {"kitchen", 1}
};

void setPinModes(){
  int count = sizeof(pins) / sizeof(PIN);

  for(int index=0; index<count; ++index){
    pinMode(pins[index].pin, OUTPUT);
  }
}

int getPin(const char* room){
  int count = sizeof(pins) / sizeof(PIN);
  int pin = -1;

  for(int index=0; index<count; ++index){
    if(strcmpi(room, pins[index].room) == 0){
      pin = pins[index].pin;

      break;
    }
  }

  return pin;
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i=0;i<length;i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  DynamicJsonBuffer jsonBuffer;
  JsonObject& cmd = jsonBuffer.parseObject((char*)payload);

  const char* op = cmd["cmd"];
  const char* room = cmd["room"];

  Serial.print("Command: ");
  Serial.println(op);
  Serial.print("Room: ");
  Serial.println(room);

  int pin = getPin(room);
  int value = LOW;

  if(strcmp(op, "on") == 0)
    value = HIGH;

  if(-1 != pin){
    Serial.print("Pin: ");
    Serial.println(pin);

    digitalWrite(pin, value);
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("mkr1000Client")) {
      Serial.println("Connectd");

      client.subscribe("respeaker/ha/cmd");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup()
{
  Serial.begin(57600);

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  setPinModes();

  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue:
    while (true);
  }

  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }

  Serial.print("Connected to ");
  Serial.println(ssid);

  client.setServer("iot.eclipse.org", 1883);
  client.setCallback(callback);
}

void loop()
{
  if (!client.connected()) {
    reconnect();
  }

  client.loop();
}
