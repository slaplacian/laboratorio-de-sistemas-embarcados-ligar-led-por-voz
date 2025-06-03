#include <WiFi.h>
#include <WiFiClient.h>
#include <driver/i2s.h>

#define I2S_WS  25
#define I2S_SD  33
#define I2S_SCK 26
#define LED_PIN 2

const char* ssid = "lphone";
const char* password = "awd34--@@red33";
const char* server_ip = "172.20.10.4";
const uint16_t server_port = 5000;

WiFiClient client;

#define SAMPLE_RATE      128
#define RECORD_SECONDS   1
#define SAMPLE_BUFFER_SIZE (SAMPLE_RATE * RECORD_SECONDS)

int16_t samples[SAMPLE_BUFFER_SIZE];

void setup_wifi() {
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Conectado!");
}

void setup_i2s() {
  i2s_config_t i2s_config = {
    .mode = i2s_mode_t(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = 512,
    .use_apll = false,
    .tx_desc_auto_clear = false,
    .fixed_mclk = 0
  };

  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_SD
  };

  i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pin_config);
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  setup_wifi();
  setup_i2s();

  Serial.println("Conectando ao servidor...");
  while (!client.connect(server_ip, server_port)) {
    Serial.println("Tentando novamente...");
    delay(1000);
  }
  Serial.println("Conectado ao servidor!");
}

void loop() {
  int32_t i2s_data[SAMPLE_BUFFER_SIZE];
  size_t bytesRead;

  i2s_read(I2S_NUM_0, (void*)i2s_data, sizeof(i2s_data), &bytesRead, portMAX_DELAY);

  int num_samples = bytesRead / sizeof(int32_t);
  for (int i = 0; i < num_samples && i < SAMPLE_BUFFER_SIZE; i++) {
    samples[i] = (int16_t)(i2s_data[i] >> 12); // Redução mais suave
  }

  // Envia o buffer inteiro (32.000 bytes) para o servidor
  client.write((uint8_t*)samples, num_samples * sizeof(int16_t));

  if (client.connected() && client.available()) {
    String response = client.readStringUntil('\n');
    response.trim();

    if (response == "ON") {
      digitalWrite(LED_PIN, HIGH);
      Serial.println("LED LIGADO");
    } else if (response == "OFF") {
      digitalWrite(LED_PIN, LOW);
      Serial.println("LED DESLIGADO");
    } else {
      Serial.println("Comando não reconhecido: " + response);
    }
  }

  // Aguarda 1 segundo antes de nova captura
  delay(100);
}