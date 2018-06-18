#include <ESP8266WiFi.h>
#include <TinyGPS.h>
#include <PubSubClient.h>

// declaracao do objeto GPS
TinyGPS gps;

// criando WiFiClient
WiFiClient espClient;

//Criando o clientMQTT com o wificlient
PubSubClient client(espClient);

// parametros WiFI
const char* ssid = "";
const char* password = "";

//Parametros MQTT
const char* mqtt_server = "m11.cloudmqtt.com"; //server MQTT
const int mqtt_port = 10443; //Porta MQTT

// string do json
char json[250];

// variaveis que irao armazenar os dados coletados do GPS
unsigned long chars = 0, date = 0, tempo = 0, id = 0;
unsigned short sentences = 0, failed_checksum = 0;

unsigned int satelites = 0, altitude = 0; 
float direcao = 0.0f, velocidade = 0.0f, latitude = 0.0f, longitude = 0.0f;
char str_latitude[15], str_longitude[15], str_direcao[15], str_velocidade[15];
char UTFTime[32];

void setup()
{
  // inicializa a porta serial
  Serial.begin(9600);
  // inicializa a conexao WiFi
  setup_wifi();
  id = ESP.getChipId();

  client.setServer(mqtt_server, mqtt_port);

  connectMqtt();
}

void connectMqtt() {
  while (!client.connected()) {    
    Serial.print("ConectandoMQTT ...");    
    
    if (client.connect("MACteste","tjyrpcmw","w9GlazqdKUqs")) {
      Serial.println("Conectado");
      
    } else {
      Serial.print("Falha ");      
      Serial.print(client.state());      
      Serial.println(" Tentando novamente em 5 segundos");
      Serial.println(WiFi.localIP());      
      
      delay(5000);
    }
  }
}

void sendMessage(String m){
  // Transformando a String em char para poder publicar no mqtt
  char charpub[m.length() + 1];
  m.toCharArray(charpub, m.length()+1);
  Serial.print(m);
  client.publish("retorno", charpub);  
  Serial.println();
}

void loop() {
  while(Serial.available()) {
    int c = Serial.read(); 
    if(gps.encode(c)) {
      getGPSData();
      sprintf(json, "{\"id\":%ld,\"utf_time\":\"%s\",\"altitude\":%ld,\"direcao\":%s,\"velocidade\":%s,\"satelites\":%d,\"latitude\":%s,\"longitude\":%s}",
              id, UTFTime, altitude, str_direcao, str_velocidade, satelites, str_latitude, str_longitude);
      Serial.println(json);
      sendMessage(json);
      delay(10000);
    }
  }
}

//Método de conexão com rede WIFI
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("connected!");
  Serial.println("ip: ");
  Serial.println(WiFi.localIP());
}

void getGPSData() {
  int year;
  byte month, day, hour, minute, second;
  gps.f_get_position(&latitude, &longitude);
  gps.get_datetime(&date, &tempo);
  gps.stats(&chars, &sentences, &failed_checksum);
  altitude =  gps.f_altitude();
  direcao = gps.f_course();
  velocidade = gps.f_speed_kmph();
  satelites = gps.satellites();
  // converte os dados de ponto-flutuante para string
  dtostrf(direcao, 3, 6, str_direcao);
  dtostrf(velocidade, 3, 6, str_velocidade);
  dtostrf(latitude, 3, 6, str_latitude);
  dtostrf(longitude, 3, 6, str_longitude);
  gps.crack_datetime(&year, &month, &day, &hour, &minute, &second);
  sprintf(UTFTime, "%04d-%02d-%02d %02d:%02d:%02d", year, month, day, hour, minute, second);
}

