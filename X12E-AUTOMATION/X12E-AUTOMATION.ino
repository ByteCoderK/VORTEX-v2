#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "SSID";
const char* password = "PASSKEY";
const char* mqtt_server = "mqtt_server";
const int mqtt_port = 8883;
const char* mqtt_user = "mqtt_user";
const char* mqtt_password = "mqtt_password";

WiFiClientSecure espClient;   
PubSubClient client(espClient);

const int relay1 = 5; 
const int relay2 = 4;
const int relay3 = 14;
const int relay4 = 12;

void callback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (unsigned int i=0; i<length; i++) {
    msg += (char)payload[i];
  }
  
  Serial.print("Message received on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  Serial.println(msg);

  if (msg == "1") {
    digitalWrite(relay1, LOW); // Relay ON (LOW triggers relay)
    Serial.println("Relay ON");
  } else if (msg == "2") {
    digitalWrite(relay1, HIGH); 
    Serial.println("Relay OFF");
  }
    else if (msg == "3") {
    digitalWrite(relay2, LOW); 
    Serial.println("Relay OFF");
  } else if (msg == "4") {
    digitalWrite(relay2, HIGH); 
    Serial.println("Relay OFF");
  }
    else if (msg == "5") {
    digitalWrite(relay3, LOW);
    Serial.println("Relay OFF");
  } else if (msg == "6") {
    digitalWrite(relay3, HIGH);
    Serial.println("Relay OFF");
  }
    else if (msg == "7") {
    digitalWrite(relay4, LOW);
    Serial.println("Relay OFF");
  } else if (msg == "8") {
    digitalWrite(relay4, HIGH);
    Serial.println("Relay OFF");
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client", mqtt_user, mqtt_password)) {
      Serial.println("connected");
      client.subscribe("vortex/relay1");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("SetUp Mode...");
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  pinMode(relay3, OUTPUT);
  pinMode(relay4, OUTPUT);
  
  digitalWrite(relay1, LOW); 
  digitalWrite(relay2, LOW); 
  digitalWrite(relay3, LOW); 
  digitalWrite(relay4, LOW);
  delay(1000);  
  digitalWrite(relay1, HIGH);
  digitalWrite(relay2, HIGH);
  digitalWrite(relay3, HIGH);
  digitalWrite(relay4, HIGH);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");

  espClient.setInsecure();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
