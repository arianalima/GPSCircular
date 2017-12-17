#include <ESP8266WiFi.h>
WiFiClient espClient;
//Parametros Wi-Fi
const char* ssid = "bruna"; //Nome da rede
const char* password = "12345678"; //Senha da Rede
 
//Definindo MQTT
#include <PubSubClient.h>
PubSubClient client(espClient);
//Parametros MQTT
const char* mqtt_server = "m13.cloudmqtt.com"; //server MQTT
const int mqtt_port = 16376; //Porta MQTT

char addr[] = "00:00:00:00:00:00";
 
//Biblioteca para tratar Json
#include <ArduinoJson.h>
 
 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);    // Initialize serial communications
 
  setup_wifi(); // Conecta ao WiFi
 
  client.setServer(mqtt_server, mqtt_port); // definindo server mqtt do client
  
 
}
 
 
//Configurando e Conectando Wi-Fi
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("Endereco IP : ");
  Serial.println(WiFi.localIP());
  }
 
//Conectando a fila do MQTT
void conectMqtt() {
  while (!client.connected()) {    
    Serial.print("ConectandoQTT ...");    
   
    //Parametros são nodeMCUClient, usuárioMQTT, senhaMQTT
    if (client.connect("ESP8266Client","bruna","123")) {
      Serial.println("Conectado");
   
    } else {
      Serial.print("Falha");      
      Serial.print(client.state());      
      Serial.println(" Tentando novamente em 5 segundos");      
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
 
 
 
//Enviando Mensagem ao MQTT
void sendMessage(String msg){
  String mensagem = "{\"mensagem\":\""+msg+"\"}";
 
  // Transformando a String em char para poder publicar no mqtt
  char charpub[mensagem.length() + 1];
  mensagem.toCharArray(charpub, mensagem.length()+1);
  Serial.print(mensagem);
 
  client.publish("topic", charpub);  
 
  Serial.println();
 
  return;
}
 
 
void loop() {
  //Verificando Status do ClientMQTT
  if (!client.connected()) {
    conectMqtt();
  }
  client.loop();

 
  //sendMessage(addr);
  client.publish("topic", addr);
  delay(4000);
 
}
